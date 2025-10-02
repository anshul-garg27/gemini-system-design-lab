#!/usr/bin/env python3
"""
API Key Manager
Manages API keys stored in the database with status transitions, rotation, and metrics.
"""
import sqlite3
import threading
from contextlib import contextmanager
from datetime import datetime, timedelta
from typing import Optional, Tuple
import random

DEFAULT_RATE_LIMIT_COOLDOWN_BASE = 60  # seconds
MAX_RATE_LIMIT_COOLDOWN = 1800  # 30 min
TEMP_DISABLED_COOLDOWN = 300  # 5 min
CONSECUTIVE_FAILURE_THRESHOLD = 3

STATUS_ACTIVE = "ACTIVE"
STATUS_RATE_LIMITED = "RATE_LIMITED"
STATUS_TEMP_DISABLED = "TEMP_DISABLED"
STATUS_DISABLED = "DISABLED"
STATUS_INVALID = "INVALID"
STATUS_EXPIRED = "EXPIRED"

class NoActiveAPIKeyError(Exception):
    pass

class APIKeyManager:
    def __init__(self, db_path: str = "unified.db"):
        self.db_path = db_path
        self._lock = threading.Lock()
        self._ensure_table()  # ensure table exists
        self._seed_from_config_if_empty()
        self._cleanup_and_reactivate()

    def _ensure_table(self):
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute(
            """CREATE TABLE IF NOT EXISTS api_keys (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT UNIQUE NOT NULL,
                status TEXT NOT NULL DEFAULT 'ACTIVE',
                last_used_at TIMESTAMP,
                last_error TEXT,
                last_error_code INTEGER,
                success_count INTEGER DEFAULT 0,
                failure_count INTEGER DEFAULT 0,
                consecutive_failures INTEGER DEFAULT 0,
                rate_limit_reset_at TIMESTAMP,
                disabled_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )"""
        )
        cur.execute("CREATE INDEX IF NOT EXISTS idx_api_keys_status ON api_keys(status)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_api_keys_rate_reset ON api_keys(rate_limit_reset_at)")
        conn.commit()
        conn.close()

    def _get_conn(self):
        return sqlite3.connect(self.db_path)

    def _seed_from_config_if_empty(self):
        from config import API_KEYS
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM api_keys")
        count = cur.fetchone()[0]
        if count == 0:
            for k in API_KEYS:
                try:
                    cur.execute("INSERT OR IGNORE INTO api_keys(key,status) VALUES(?,?)", (k.strip(), STATUS_ACTIVE))
                except Exception:
                    continue
            conn.commit()
        conn.close()

    def _cleanup_and_reactivate(self):
        conn = self._get_conn()
        cur = conn.cursor()
        # Reactivate keys whose rate limit cooldown passed
        cur.execute(
            """UPDATE api_keys
                SET status = ?, rate_limit_reset_at=NULL, consecutive_failures=0, updated_at=CURRENT_TIMESTAMP
                WHERE status = ? AND (rate_limit_reset_at IS NULL OR rate_limit_reset_at <= CURRENT_TIMESTAMP)""",
            (STATUS_ACTIVE, STATUS_RATE_LIMITED)
        )
        # Reactivate TEMP_DISABLED if enough time passed (reuse rate_limit_reset_at as cooldown marker)
        cur.execute(
            """UPDATE api_keys
                SET status = ?, rate_limit_reset_at=NULL, consecutive_failures=0, updated_at=CURRENT_TIMESTAMP
                WHERE status = ? AND (rate_limit_reset_at IS NULL OR rate_limit_reset_at <= CURRENT_TIMESTAMP)""",
            (STATUS_ACTIVE, STATUS_TEMP_DISABLED)
        )
        conn.commit()
        conn.close()

    def _compute_rate_limit_backoff(self, consecutive_failures: int) -> int:
        base = DEFAULT_RATE_LIMIT_COOLDOWN_BASE
        cooldown = base * max(1, consecutive_failures)
        return min(cooldown, MAX_RATE_LIMIT_COOLDOWN)

    def get_status_counts(self):
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute("SELECT status, COUNT(*) FROM api_keys GROUP BY status")
        data = dict(cur.fetchall())
        conn.close()
        return data

    def list_active_keys(self):
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute("SELECT key FROM api_keys WHERE status=?", (STATUS_ACTIVE,))
        keys = [r[0] for r in cur.fetchall()]
        conn.close()
        return keys

    def _select_active_key_row(self) -> Optional[Tuple[int,str,int]]:
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute(
            """SELECT id, key, success_count FROM api_keys
                WHERE status=?
                ORDER BY COALESCE(last_used_at,'1970-01-01'), success_count ASC, id ASC
                LIMIT 5""",
            (STATUS_ACTIVE,)
        )
        rows = cur.fetchall()
        if not rows:
            conn.close()
            return None
        # Add some randomization among the first few to distribute
        choice = random.choice(rows)
        # Update last_used_at immediately
        cur.execute("UPDATE api_keys SET last_used_at=CURRENT_TIMESTAMP, updated_at=CURRENT_TIMESTAMP WHERE id=?", (choice[0],))
        conn.commit()
        conn.close()
        return choice

    @contextmanager
    def acquire_key(self):
        with self._lock:
            self._cleanup_and_reactivate()
            row = self._select_active_key_row()
            if not row:
                raise NoActiveAPIKeyError("No ACTIVE API key available")
        key_id, key_value, _ = row
        try:
            yield key_id, key_value
        except Exception:
            raise

    def record_success(self, key_id: int):
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute(
            """UPDATE api_keys SET success_count=success_count+1, consecutive_failures=0, updated_at=CURRENT_TIMESTAMP
                WHERE id=?""",
            (key_id,)
        )
        conn.commit()
        conn.close()

    def record_failure(self, key_id: int, http_status: Optional[int], error_text: Optional[str]):
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute("SELECT consecutive_failures FROM api_keys WHERE id=?", (key_id,))
        row = cur.fetchone()
        consecutive = (row[0] if row else 0) + 1
        new_status = None
        rate_limit_reset_at = None

        if http_status == 429:
            new_status = STATUS_RATE_LIMITED
            cooldown = self._compute_rate_limit_backoff(consecutive)
            rate_limit_reset_at = datetime.utcnow() + timedelta(seconds=cooldown)
        elif http_status in (401,403):
            new_status = STATUS_INVALID
        elif http_status and 500 <= http_status < 600:
            if consecutive >= CONSECUTIVE_FAILURE_THRESHOLD:
                new_status = STATUS_TEMP_DISABLED
                rate_limit_reset_at = datetime.utcnow() + timedelta(seconds=TEMP_DISABLED_COOLDOWN)
        # network errors (http_status None) treat similar to 5xx for threshold logic
        elif http_status is None:
            if consecutive >= CONSECUTIVE_FAILURE_THRESHOLD:
                new_status = STATUS_TEMP_DISABLED
                rate_limit_reset_at = datetime.utcnow() + timedelta(seconds=TEMP_DISABLED_COOLDOWN)

        params = {
            'id': key_id,
            'error_text': (error_text or '')[:500],
            'http_status': http_status,
            'rate_reset': rate_limit_reset_at.isoformat() if rate_limit_reset_at else None
        }

        if new_status:
            cur.execute(
                """UPDATE api_keys
                    SET failure_count=failure_count+1,
                        consecutive_failures=?,
                        status=?,
                        last_error=?,
                        last_error_code=?,
                        rate_limit_reset_at=?,
                        updated_at=CURRENT_TIMESTAMP,
                        disabled_at=CASE WHEN ? IN ('INVALID') THEN CURRENT_TIMESTAMP ELSE disabled_at END
                    WHERE id=?""",
                (consecutive, new_status, params['error_text'], params['http_status'], params['rate_reset'], new_status, key_id)
            )
        else:
            cur.execute(
                """UPDATE api_keys
                    SET failure_count=failure_count+1,
                        consecutive_failures=?,
                        last_error=?,
                        last_error_code=?,
                        updated_at=CURRENT_TIMESTAMP
                    WHERE id=?""",
                (consecutive, params['error_text'], params['http_status'], key_id)
            )
        conn.commit()
        conn.close()

    def manually_set_status(self, key_value: str, status: str):
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute("UPDATE api_keys SET status=?, updated_at=CURRENT_TIMESTAMP WHERE key=?", (status, key_value))
        conn.commit()
        conn.close()

    def add_key(self, key_value: str, status: str = STATUS_ACTIVE):
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute("INSERT OR IGNORE INTO api_keys(key,status) VALUES(?,?)", (key_value.strip(), status))
        conn.commit()
        conn.close()

    def get_all(self):
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute("SELECT id,key,status,success_count,failure_count,consecutive_failures,last_used_at,rate_limit_reset_at FROM api_keys ORDER BY id")
        rows = cur.fetchall()
        conn.close()
        return rows

if __name__ == "__main__":
    m = APIKeyManager()
    print("Status counts:", m.get_status_counts())
    try:
        with m.acquire_key() as (kid, key):
            print("Acquired key", kid)
            m.record_success(kid)
    except NoActiveAPIKeyError as e:
        print("No key:", e)
