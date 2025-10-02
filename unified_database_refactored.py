#!/usr/bin/env python3
"""
Refactored Unified SQLite database manager with:
- Thread-local connection pooling
- Proper logging instead of print()
- Decorator pattern to eliminate code duplication
- Transaction management
"""

import sqlite3
import json
import os
import hashlib
import logging
import threading
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path
from contextlib import contextmanager
from functools import wraps

# Configure logging
logger = logging.getLogger(__name__)


def db_operation(commit=True):
    """
    Decorator for database operations to eliminate code duplication.
    
    Args:
        commit: Whether to commit the transaction (default: True)
    
    Usage:
        @db_operation()
        def my_method(self, cursor, param1, param2):
            cursor.execute("SELECT * FROM table WHERE id = ?", (param1,))
            return cursor.fetchone()
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            conn = self._get_connection()
            cursor = conn.cursor()
            try:
                result = func(self, cursor, *args, **kwargs)
                if commit:
                    conn.commit()
                return result
            except Exception as e:
                if commit:
                    conn.rollback()
                logger.error(f"Database error in {func.__name__}: {e}", exc_info=True)
                raise
        return wrapper
    return decorator


class UnifiedDatabase:
    """
    Refactored unified SQLite database manager with improved performance and maintainability.
    """
    
    def __init__(self, db_path: str = "unified.db"):
        """
        Initialize the unified database manager.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.cache_dir = Path("./data/cache")
        self.cache_dir.mkdir(exist_ok=True, parents=True)
        
        # Thread-local storage for connections
        self._local = threading.local()
        
        self._init_database()
        logger.info(f"Initialized UnifiedDatabase at {db_path}")
    
    def _get_connection(self):
        """
        Get or create thread-local connection.
        This implements connection pooling per thread for better performance.
        """
        if not hasattr(self._local, 'conn'):
            self._local.conn = sqlite3.connect(
                self.db_path,
                check_same_thread=False,
                timeout=30.0
            )
            self._local.conn.row_factory = sqlite3.Row
            # Enable foreign keys
            self._local.conn.execute("PRAGMA foreign_keys = ON")
            logger.debug(f"Created new database connection for thread {threading.current_thread().name}")
        return self._local.conn
    
    @contextmanager
    def transaction(self):
        """
        Context manager for explicit transaction management.
        
        Usage:
            with db.transaction() as cursor:
                cursor.execute("INSERT INTO ...")
                cursor.execute("UPDATE ...")
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            yield cursor
            conn.commit()
            logger.debug("Transaction committed successfully")
        except Exception as e:
            conn.rollback()
            logger.error(f"Transaction rolled back due to error: {e}", exc_info=True)
            raise
    
    def close_connections(self):
        """Close thread-local connection if it exists."""
        if hasattr(self._local, 'conn'):
            self._local.conn.close()
            delattr(self._local, 'conn')
            logger.debug("Closed database connection")
    
    def _init_database(self):
        """Initialize the database with all required tables."""
        logger.info("Initializing database schema")
        
        with self.transaction() as cursor:
            # Topics table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS topics (
                    id INTEGER PRIMARY KEY,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL,
                    category TEXT NOT NULL,
                    subcategory TEXT NOT NULL,
                    company TEXT NOT NULL,
                    technologies TEXT NOT NULL,
                    complexity_level TEXT NOT NULL,
                    tags TEXT NOT NULL,
                    related_topics TEXT NOT NULL,
                    metrics TEXT NOT NULL,
                    implementation_details TEXT NOT NULL,
                    learning_objectives TEXT NOT NULL,
                    difficulty INTEGER NOT NULL,
                    estimated_read_time TEXT NOT NULL,
                    prerequisites TEXT NOT NULL,
                    created_date TEXT NOT NULL,
                    updated_date TEXT NOT NULL,
                    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    source TEXT DEFAULT 'web_batch',
                    UNIQUE(id)
                )
            """)
            
            # Topic status table (check if exists first)
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='topic_status'")
            table_exists = cursor.fetchone()
            
            if table_exists:
                cursor.execute("PRAGMA table_info(topic_status)")
                columns = {row[1] for row in cursor.fetchall()}
                
                if 'title' in columns and 'original_title' not in columns:
                    logger.info("Using legacy topic_status schema")
                elif 'original_title' not in columns:
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS topic_status (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            original_title TEXT NOT NULL,
                            current_title TEXT,
                            status TEXT NOT NULL,
                            error_message TEXT,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        )
                    """)
                    logger.info("Created new topic_status schema")
            else:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS topic_status (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        original_title TEXT NOT NULL,
                        current_title TEXT,
                        status TEXT NOT NULL,
                        error_message TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                logger.info("Created topic_status table")
            
            # Jobs table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS jobs (
                    id TEXT PRIMARY KEY,
                    topic_id TEXT,
                    topic_name TEXT,
                    status TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Tasks table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id TEXT PRIMARY KEY,
                    job_id TEXT NOT NULL,
                    platform TEXT NOT NULL,
                    format TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'pending',
                    result TEXT,
                    error TEXT,
                    started_at TIMESTAMP,
                    finished_at TIMESTAMP,
                    cached BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (job_id) REFERENCES jobs (id)
                )
            """)
            
            # Results table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS results (
                    id TEXT PRIMARY KEY,
                    job_id TEXT NOT NULL,
                    platform TEXT NOT NULL,
                    format TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (job_id) REFERENCES jobs (id)
                )
            """)
            
            # Prompts table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS prompts (
                    id TEXT PRIMARY KEY,
                    job_id TEXT NOT NULL,
                    platform TEXT NOT NULL,
                    format TEXT NOT NULL,
                    prompt_text TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (job_id) REFERENCES jobs (id)
                )
            """)
            
            # Create indexes for better performance
            indexes = [
                "CREATE INDEX IF NOT EXISTS idx_topics_category ON topics(category)",
                "CREATE INDEX IF NOT EXISTS idx_topics_company ON topics(company)",
                "CREATE INDEX IF NOT EXISTS idx_topics_complexity ON topics(complexity_level)",
                "CREATE INDEX IF NOT EXISTS idx_topics_difficulty ON topics(difficulty)",
                "CREATE INDEX IF NOT EXISTS idx_topic_status_status ON topic_status(status)",
                "CREATE INDEX IF NOT EXISTS idx_jobs_status ON jobs(status)",
                "CREATE INDEX IF NOT EXISTS idx_tasks_job_id ON tasks(job_id)",
                "CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status)",
                "CREATE INDEX IF NOT EXISTS idx_results_job_id ON results(job_id)",
            ]
            
            # Check for schema-specific indexes
            cursor.execute("PRAGMA table_info(topic_status)")
            topic_status_columns = {row[1] for row in cursor.fetchall()}
            
            if 'title' in topic_status_columns:
                indexes.append("CREATE INDEX IF NOT EXISTS idx_topic_status_title ON topic_status(title)")
            if 'original_title' in topic_status_columns:
                indexes.append("CREATE INDEX IF NOT EXISTS idx_topic_status_original_title ON topic_status(original_title)")
            if 'current_title' in topic_status_columns:
                indexes.append("CREATE INDEX IF NOT EXISTS idx_topic_status_current_title ON topic_status(current_title)")
            
            for index in indexes:
                cursor.execute(index)
            
            logger.info("Database schema initialization complete")
    
    # ===== TOPIC MANAGEMENT METHODS =====
    
    def _serialize_json_field(self, field_value):
        """Helper to serialize JSON fields consistently."""
        if isinstance(field_value, (list, dict)):
            return json.dumps(field_value)
        elif isinstance(field_value, str):
            try:
                json.loads(field_value)
                return field_value
            except (json.JSONDecodeError, TypeError):
                return field_value
        else:
            return field_value or ""
    
    @db_operation()
    def save_topic(self, cursor, topic: Dict[str, Any], source: str = "web_batch") -> bool:
        """Save a topic to the database."""
        cursor.execute("""
            INSERT OR REPLACE INTO topics 
            (id, title, description, category, subcategory, company, technologies,
             complexity_level, tags, related_topics, metrics, implementation_details,
             learning_objectives, difficulty, estimated_read_time, prerequisites,
             created_date, updated_date, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            topic.get('id'),
            topic.get('title', ''),
            topic.get('description', ''),
            topic.get('category', ''),
            topic.get('subcategory', ''),
            topic.get('company', ''),
            self._serialize_json_field(topic.get('technologies', [])),
            topic.get('complexity_level', ''),
            self._serialize_json_field(topic.get('tags', [])),
            self._serialize_json_field(topic.get('related_topics', [])),
            self._serialize_json_field(topic.get('metrics', {})),
            self._serialize_json_field(topic.get('implementation_details', {})),
            self._serialize_json_field(topic.get('learning_objectives', [])),
            topic.get('difficulty', 5),
            topic.get('estimated_read_time', ''),
            self._serialize_json_field(topic.get('prerequisites', [])),
            topic.get('created_date', datetime.now().strftime("%Y-%m-%d")),
            topic.get('updated_date', datetime.now().strftime("%Y-%m-%d")),
            source
        ))
        logger.info(f"Saved topic {topic.get('id')}: {topic.get('title')}")
        return True
    
    @db_operation()
    def get_topic_by_id(self, cursor, topic_id: int) -> Optional[Dict[str, Any]]:
        """Get a topic by ID."""
        cursor.execute("SELECT * FROM topics WHERE id = ?", (topic_id,))
        row = cursor.fetchone()
        
        if row:
            topic_dict = dict(row)
            
            # Parse JSON fields
            json_fields = ['technologies', 'tags', 'related_topics', 'metrics', 
                          'implementation_details', 'learning_objectives', 'prerequisites']
            for field in json_fields:
                if field in topic_dict and topic_dict[field]:
                    try:
                        topic_dict[field] = json.loads(topic_dict[field])
                    except (json.JSONDecodeError, TypeError):
                        topic_dict[field] = []
            
            logger.debug(f"Retrieved topic {topic_id}")
            return topic_dict
        
        logger.debug(f"Topic {topic_id} not found")
        return None
    
    @db_operation()
    def get_topic_by_title(self, cursor, title: str) -> Optional[Dict[str, Any]]:
        """Get a topic by title with its status."""
        # Check schema first
        cursor.execute("PRAGMA table_info(topic_status)")
        columns = {row[1] for row in cursor.fetchall()}
        
        if 'original_title' in columns:
            cursor.execute("""
                SELECT t.*, ts.status, ts.error_message, ts.created_at as status_created_at
                FROM topics t
                LEFT JOIN topic_status ts ON (t.title = ts.original_title OR t.title = ts.current_title)
                WHERE t.title = ?
            """, (title.strip(),))
        else:
            cursor.execute("""
                SELECT t.*, ts.status, ts.error_message, ts.created_at as status_created_at
                FROM topics t
                LEFT JOIN topic_status ts ON t.title = ts.title
                WHERE t.title = ?
            """, (title.strip(),))
        
        row = cursor.fetchone()
        if row:
            logger.debug(f"Retrieved topic by title: {title}")
            return dict(row)
        
        logger.debug(f"Topic not found: {title}")
        return None
    
    @db_operation()
    def delete_topic(self, cursor, topic_id: int) -> bool:
        """Delete a topic by ID."""
        cursor.execute("SELECT id FROM topics WHERE id = ?", (topic_id,))
        if not cursor.fetchone():
            logger.warning(f"Topic {topic_id} not found for deletion")
            return False
        
        cursor.execute("DELETE FROM topics WHERE id = ?", (topic_id,))
        cursor.execute("DELETE FROM topic_status WHERE title IN (SELECT title FROM topics WHERE id = ?)", (topic_id,))
        
        logger.info(f"Deleted topic {topic_id}")
        return True
    
    @db_operation()
    def get_next_available_id(self, cursor) -> int:
        """Get the next available ID for a new topic."""
        cursor.execute("SELECT MAX(id) FROM topics")
        result = cursor.fetchone()
        max_id = result[0] if result[0] is not None else 0
        return max_id + 1
    
    # ===== TOPIC STATUS METHODS =====
    
    @db_operation()
    def add_topic_for_processing(self, cursor, original_title: str) -> int:
        """Add a new topic for processing and return its status ID."""
        # Check schema
        cursor.execute("PRAGMA table_info(topic_status)")
        columns = {row[1] for row in cursor.fetchall()}
        
        if 'original_title' in columns:
            cursor.execute("""
                INSERT INTO topic_status (original_title, status)
                VALUES (?, 'pending')
            """, (original_title,))
        else:
            cursor.execute("""
                INSERT INTO topic_status (title, status)
                VALUES (?, 'pending')
            """, (original_title,))
        
        topic_status_id = cursor.lastrowid
        logger.info(f"Added topic for processing: {original_title} (ID: {topic_status_id})")
        return topic_status_id
    
    @db_operation()
    def update_topic_status_by_id(self, cursor, topic_status_id: int, status: str, 
                                  error_message: str = None, current_title: str = None) -> bool:
        """Update topic status by ID."""
        # Check schema
        cursor.execute("PRAGMA table_info(topic_status)")
        columns = {row[1] for row in cursor.fetchall()}
        
        has_current_title = 'current_title' in columns
        
        if has_current_title and current_title:
            if error_message:
                cursor.execute("""
                    UPDATE topic_status 
                    SET status = ?, current_title = ?, error_message = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                """, (status, current_title, error_message, topic_status_id))
            else:
                cursor.execute("""
                    UPDATE topic_status 
                    SET status = ?, current_title = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                """, (status, current_title, topic_status_id))
        else:
            if error_message:
                cursor.execute("""
                    UPDATE topic_status 
                    SET status = ?, error_message = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                """, (status, error_message, topic_status_id))
            else:
                cursor.execute("""
                    UPDATE topic_status 
                    SET status = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                """, (status, topic_status_id))
        
        success = cursor.rowcount > 0
        if success:
            logger.info(f"Updated topic status {topic_status_id} to {status}")
        else:
            logger.warning(f"No topic status found with ID {topic_status_id}")
        
        return success
    
    @db_operation(commit=False)
    def get_topic_status_by_title(self, cursor, title: str) -> Optional[Dict[str, Any]]:
        """Get topic_status record by title."""
        # Check schema
        cursor.execute("PRAGMA table_info(topic_status)")
        columns = {row[1] for row in cursor.fetchall()}
        
        if 'original_title' in columns:
            cursor.execute("""
                SELECT id, original_title, current_title, status, error_message, created_at, updated_at
                FROM topic_status
                WHERE original_title = ? OR current_title = ?
                ORDER BY created_at DESC
                LIMIT 1
            """, (title, title))
            
            row = cursor.fetchone()
            if row:
                return dict(row)
        else:
            cursor.execute("""
                SELECT id, title, status, error_message, created_at, updated_at
                FROM topic_status
                WHERE title = ?
                ORDER BY created_at DESC
                LIMIT 1
            """, (title,))
            
            row = cursor.fetchone()
            if row:
                return dict(row)
        
        logger.debug(f"No topic status found for: {title}")
        return None
    
    @db_operation(commit=False)
    def get_topic_status_summary(self, cursor) -> Dict[str, Any]:
        """Get summary of topic statuses."""
        cursor.execute("""
            SELECT status, COUNT(*) as count
            FROM topic_status
            GROUP BY status
        """)
        
        rows = cursor.fetchall()
        summary = {row['status']: row['count'] for row in rows}
        
        logger.debug(f"Topic status summary: {summary}")
        return {'summary': summary}
    
    @db_operation()
    def cleanup_failed_topics(self, cursor) -> Dict[str, Any]:
        """Clean up failed topics from the database."""
        cursor.execute("SELECT COUNT(*) as count FROM topic_status WHERE status = 'failed'")
        failed_count = cursor.fetchone()['count']
        
        if failed_count > 0:
            cursor.execute("DELETE FROM topic_status WHERE status = 'failed'")
            logger.info(f"Cleaned up {failed_count} failed topics")
            return {
                'success': True,
                'message': f'Cleaned up {failed_count} failed topics',
                'count': failed_count
            }
        else:
            logger.info("No failed topics to clean up")
            return {
                'success': True,
                'message': 'No failed topics to clean up',
                'count': 0
            }
    
    # ===== STATISTICS METHODS =====
    
    @db_operation(commit=False)
    def get_stats(self, cursor) -> Dict[str, Any]:
        """Get database statistics."""
        cursor.execute("SELECT COUNT(*) as count FROM topics")
        total_topics = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(*) as count FROM topic_status WHERE status = 'completed'")
        completed_topics = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(*) as count FROM topic_status WHERE status = 'failed'")
        failed_topics = cursor.fetchone()['count']
        
        success_rate = (completed_topics / total_topics * 100) if total_topics > 0 else 0
        
        cursor.execute("SELECT AVG(difficulty) as avg_diff FROM topics WHERE difficulty IS NOT NULL")
        avg_difficulty = cursor.fetchone()['avg_diff'] or 0
        
        cursor.execute("SELECT COUNT(DISTINCT category) as count FROM topics WHERE category IS NOT NULL")
        category_count = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(DISTINCT company) as count FROM topics WHERE company IS NOT NULL")
        company_count = cursor.fetchone()['count']
        
        stats = {
            'total_topics': total_topics,
            'completed_topics': completed_topics,
            'failed_topics': failed_topics,
            'success_rate': round(success_rate, 2),
            'average_difficulty': round(avg_difficulty, 2),
            'category_count': category_count,
            'company_count': company_count
        }
        
        logger.debug(f"Database stats: {stats}")
        return stats
    
    @db_operation(commit=False)
    def get_all_topic_ids(self, cursor) -> List[int]:
        """Get all topic IDs for cross-linking."""
        cursor.execute("SELECT id FROM topics ORDER BY id")
        return [row['id'] for row in cursor.fetchall()]
    
    # ===== CONTENT GENERATION METHODS (FastAPI backend) =====
    
    @db_operation()
    def create_job(self, cursor, job_id: str, topic_id: str, topic_name: str, status: str):
        """Create a new content generation job."""
        cursor.execute("""
            INSERT INTO jobs (id, topic_id, topic_name, status)
            VALUES (?, ?, ?, ?)
        """, (job_id, topic_id, topic_name, status))
        logger.info(f"Created job {job_id} for topic {topic_id}")
    
    @db_operation()
    def update_job_status(self, cursor, job_id: str, status: str):
        """Update job status."""
        cursor.execute("""
            UPDATE jobs SET status = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (status, job_id))
        logger.info(f"Updated job {job_id} status to {status}")
    
    @db_operation()
    def create_task(self, cursor, task_id: str, job_id: str, platform: str, format: str, status: str):
        """Create a new task."""
        cursor.execute("""
            INSERT INTO tasks (id, job_id, platform, format, status)
            VALUES (?, ?, ?, ?, ?)
        """, (task_id, job_id, platform, format, status))
        logger.debug(f"Created task {task_id} for job {job_id}")
    
    @db_operation()
    def update_task_status(self, cursor, task_id: str, status: str, result: str = None, error: str = None):
        """Update task status."""
        cursor.execute("""
            UPDATE tasks SET status = ?, result = ?, error = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (status, result, error, task_id))
        logger.debug(f"Updated task {task_id} status to {status}")
    
    @db_operation()
    def save_result(self, cursor, result_id: str, job_id: str, platform: str, format: str, content: str):
        """Save content generation result."""
        cursor.execute("""
            INSERT INTO results (id, job_id, platform, format, content)
            VALUES (?, ?, ?, ?, ?)
        """, (result_id, job_id, platform, format, content))
        logger.info(f"Saved result {result_id} for job {job_id}")
    
    @db_operation()
    def save_prompt(self, cursor, prompt_id: str, job_id: str, platform: str, format: str, prompt_text: str):
        """Save prompt used for generation."""
        cursor.execute("""
            INSERT INTO prompts (id, job_id, platform, format, prompt_text)
            VALUES (?, ?, ?, ?, ?)
        """, (prompt_id, job_id, platform, format, prompt_text))
        logger.debug(f"Saved prompt {prompt_id} for job {job_id}")
    
    @db_operation(commit=False)
    def get_job_status(self, cursor, job_id: str) -> Optional[Dict[str, Any]]:
        """Get job status and progress."""
        cursor.execute("SELECT * FROM jobs WHERE id = ?", (job_id,))
        job_row = cursor.fetchone()
        
        if not job_row:
            logger.debug(f"Job {job_id} not found")
            return None
        
        cursor.execute("SELECT COUNT(*) as count FROM tasks WHERE job_id = ?", (job_id,))
        total_tasks = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(*) as count FROM tasks WHERE job_id = ? AND status = 'completed'", (job_id,))
        completed_tasks = cursor.fetchone()['count']
        
        return {
            'jobId': job_id,
            'status': job_row['status'],
            'progress': {
                'total': total_tasks,
                'done': completed_tasks
            }
        }
    
    # ===== CACHE METHODS =====
    
    def get_cache_path(self, key: str) -> Path:
        """Get cache file path for a given key."""
        return self.cache_dir / f"{key}.json"
    
    def get_cache(self, key: str) -> Optional[Dict[str, Any]]:
        """Get cached content."""
        cache_path = self.get_cache_path(key)
        if cache_path.exists():
            try:
                with open(cache_path, 'r') as f:
                    logger.debug(f"Cache hit for key {key}")
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error reading cache for key {key}: {e}")
                return None
        logger.debug(f"Cache miss for key {key}")
        return None
    
    def set_cache(self, key: str, content: Dict[str, Any]):
        """Cache content."""
        cache_path = self.get_cache_path(key)
        try:
            with open(cache_path, 'w') as f:
                json.dump(content, f, indent=2)
            logger.debug(f"Cached content for key {key}")
        except Exception as e:
            logger.error(f"Error caching content for key {key}: {e}")
    
    def generate_cache_key(self, topic_title: str, platform: str, format: str, prompt_version: str = "v1") -> str:
        """Generate cache key for content."""
        content = f"{topic_title}|{platform}|{format}|{prompt_version}"
        return hashlib.sha256(content.encode()).hexdigest()
    
    # ===== ADDITIONAL TOPIC METHODS =====
    
    @db_operation(commit=False)
    def get_topics_paginated(self, cursor, limit: int = 20, offset: int = 0, 
                           search: str = None, category: str = None, 
                           subcategory: str = None, status: str = None, 
                           complexity: str = None, company: str = None, 
                           sort_by: str = "created_date", 
                           sort_order: str = "desc") -> List[Dict[str, Any]]:
        """Get topics with pagination and filtering."""
        # Check schema to determine JOIN condition
        cursor.execute("PRAGMA table_info(topic_status)")
        columns = {row[1] for row in cursor.fetchall()}
        has_original_title = 'original_title' in columns
        
        # Build WHERE clause
        where_conditions = []
        params = []
        
        if search:
            where_conditions.append("(topics.title LIKE ? OR topics.description LIKE ?)")
            params.extend([f"%{search}%", f"%{search}%"])
        
        if category:
            where_conditions.append("topics.category = ?")
            params.append(category)
        
        if subcategory:
            where_conditions.append("topics.subcategory = ?")
            params.append(subcategory)
        
        if complexity:
            where_conditions.append("topics.complexity_level = ?")
            params.append(complexity)
        
        if company:
            where_conditions.append("topics.company = ?")
            params.append(company)
        
        if status:
            where_conditions.append("topic_status.status = ?")
            params.append(status)
        
        where_clause = ""
        if where_conditions:
            where_clause = "WHERE " + " AND ".join(where_conditions)
        
        # Build ORDER BY clause
        valid_sort_fields = ["title", "created_date", "updated_date", "complexity_level", "company"]
        if sort_by not in valid_sort_fields:
            sort_by = "created_date"
        
        sort_direction = "ASC" if sort_order.lower() == "asc" else "DESC"
        order_clause = f"ORDER BY topics.{sort_by} {sort_direction}"
        
        # Build query with correct JOIN based on schema
        if has_original_title:
            join_condition = "LEFT JOIN topic_status ON (topics.title = topic_status.original_title OR topics.title = topic_status.current_title)"
        else:
            join_condition = "LEFT JOIN topic_status ON topics.title = topic_status.title"
        
        query = f"""
            SELECT topics.*, topic_status.status, topic_status.error_message
            FROM topics
            {join_condition}
            {where_clause}
            {order_clause}
            LIMIT ? OFFSET ?
        """
        params.extend([limit, offset])
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        topics = [dict(row) for row in rows]
        logger.debug(f"Retrieved {len(topics)} topics with pagination")
        return topics
    
    @db_operation(commit=False)
    def get_topics_count(self, cursor, search: str = None, category: str = None, 
                        subcategory: str = None, status: str = None, 
                        complexity: str = None, company: str = None) -> int:
        """Get total count of topics matching filters."""
        # Check schema to determine JOIN condition
        cursor.execute("PRAGMA table_info(topic_status)")
        columns = {row[1] for row in cursor.fetchall()}
        has_original_title = 'original_title' in columns
        
        where_conditions = []
        params = []
        
        if search:
            where_conditions.append("(topics.title LIKE ? OR topics.description LIKE ?)")
            params.extend([f"%{search}%", f"%{search}%"])
        
        if category:
            where_conditions.append("topics.category = ?")
            params.append(category)
        
        if subcategory:
            where_conditions.append("topics.subcategory = ?")
            params.append(subcategory)
        
        if complexity:
            where_conditions.append("topics.complexity_level = ?")
            params.append(complexity)
        
        if company:
            where_conditions.append("topics.company = ?")
            params.append(company)
        
        if status:
            where_conditions.append("topic_status.status = ?")
            params.append(status)
        
        where_clause = ""
        if where_conditions:
            where_clause = "WHERE " + " AND ".join(where_conditions)
        
        # Build query with correct JOIN based on schema
        if has_original_title:
            join_condition = "LEFT JOIN topic_status ON (topics.title = topic_status.original_title OR topics.title = topic_status.current_title)"
        else:
            join_condition = "LEFT JOIN topic_status ON topics.title = topic_status.title"
        
        query = f"""
            SELECT COUNT(*)
            FROM topics
            {join_condition}
            {where_clause}
        """
        
        cursor.execute(query, params)
        count = cursor.fetchone()[0]
        return count
    
    @db_operation(commit=False)
    def topic_exists_and_completed(self, cursor, title: str) -> bool:
        """Check if topic exists and is completed."""
        cursor.execute("""
            SELECT COUNT(*) FROM topic_status 
            WHERE title = ? AND status = 'completed'
        """, (title,))
        count = cursor.fetchone()[0]
        return count > 0
    
    @db_operation()
    def save_topic_status(self, cursor, title: str, status: str, error_message: str = None) -> bool:
        """
        Save topic processing status.
        DEPRECATED: Use add_topic_for_processing() and update_topic_status_by_id() instead.
        This is kept for backward compatibility.
        """
        # Check schema first
        cursor.execute("PRAGMA table_info(topic_status)")
        columns = {row[1] for row in cursor.fetchall()}
        
        if 'original_title' in columns:
            # New schema - check if exists first
            cursor.execute("SELECT id FROM topic_status WHERE original_title = ?", (title,))
            existing = cursor.fetchone()
            
            if existing:
                cursor.execute("""
                    UPDATE topic_status 
                    SET status = ?, error_message = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                """, (status, error_message, existing[0]))
            else:
                cursor.execute("""
                    INSERT INTO topic_status 
                    (original_title, status, error_message, updated_at)
                    VALUES (?, ?, ?, CURRENT_TIMESTAMP)
                """, (title, status, error_message))
        else:
            # Old schema
            cursor.execute("""
                INSERT OR REPLACE INTO topic_status 
                (title, status, error_message, updated_at)
                VALUES (?, ?, ?, CURRENT_TIMESTAMP)
            """, (title, status, error_message))
        
        logger.info(f"Saved topic status for '{title}': {status}")
        return True
    
    @db_operation(commit=False)
    def get_topic_status(self, cursor, topic_id: int) -> Optional[Dict[str, Any]]:
        """Get topic status by ID."""
        cursor.execute("SELECT * FROM topic_status WHERE id = ?", (topic_id,))
        row = cursor.fetchone()
        if not row:
            return None
        
        return dict(row)
    
    @db_operation(commit=False)
    def get_topics_stats(self, cursor) -> Dict[str, Any]:
        """Get comprehensive topic statistics."""
        # Total topics
        cursor.execute("SELECT COUNT(*) as count FROM topics")
        total_topics = cursor.fetchone()['count']
        
        # Status breakdown
        cursor.execute("""
            SELECT 
                COALESCE(ts.status, 'completed') as status,
                COUNT(*) as count
            FROM topics t
            LEFT JOIN topic_status ts ON t.title = ts.title
            GROUP BY COALESCE(ts.status, 'completed')
        """)
        status_breakdown = {row['status']: row['count'] for row in cursor.fetchall()}
        
        # Category breakdown
        cursor.execute("""
            SELECT category, COUNT(*) as count
            FROM topics 
            WHERE category IS NOT NULL AND category != ''
            GROUP BY category 
            ORDER BY COUNT(*) DESC
        """)
        category_breakdown = {row['category']: row['count'] for row in cursor.fetchall()}
        
        # Complexity breakdown
        cursor.execute("""
            SELECT complexity_level, COUNT(*) as count
            FROM topics 
            WHERE complexity_level IS NOT NULL AND complexity_level != ''
            GROUP BY complexity_level 
            ORDER BY COUNT(*) DESC
        """)
        complexity_breakdown = {row['complexity_level']: row['count'] for row in cursor.fetchall()}
        
        # Company breakdown
        cursor.execute("""
            SELECT company, COUNT(*) as count
            FROM topics 
            WHERE company IS NOT NULL AND company != ''
            GROUP BY company 
            ORDER BY COUNT(*) DESC
            LIMIT 10
        """)
        company_breakdown = {row['company']: row['count'] for row in cursor.fetchall()}
        
        # Average difficulty
        cursor.execute("SELECT AVG(difficulty) as avg FROM topics WHERE difficulty IS NOT NULL")
        avg_difficulty = cursor.fetchone()['avg'] or 0
        
        # Daily stats (last 7 days)
        cursor.execute("""
            SELECT DATE(generated_at) as date, COUNT(*) as count
            FROM topics
            WHERE generated_at >= datetime('now', '-7 days')
            GROUP BY DATE(generated_at)
            ORDER BY date DESC
        """)
        daily_stats = [{'date': row['date'], 'count': row['count']} for row in cursor.fetchall()]
        
        return {
            'total_topics': total_topics,
            'status_breakdown': status_breakdown,
            'category_breakdown': category_breakdown,
            'complexity_breakdown': complexity_breakdown,
            'company_breakdown': company_breakdown,
            'average_difficulty': round(avg_difficulty, 2),
            'daily_stats': daily_stats
        }
    
    @db_operation(commit=False)
    def get_topics_by_status(self, cursor, status: str, limit: int = None) -> List[Dict[str, Any]]:
        """Get topics by their processing status with topic_status_id."""
        # Check schema
        cursor.execute("PRAGMA table_info(topic_status)")
        columns = {row[1] for row in cursor.fetchall()}
        
        if 'original_title' in columns:
            query = """
                SELECT 
                    ts.id as topic_status_id,
                    ts.original_title,
                    ts.current_title,
                    ts.status,
                    ts.error_message,
                    ts.created_at,
                    ts.updated_at,
                    t.id as topic_id
                FROM topic_status ts
                LEFT JOIN topics t ON (ts.original_title = t.title OR ts.current_title = t.title)
                WHERE ts.status = ?
                ORDER BY ts.created_at ASC
            """
        else:
            query = """
                SELECT 
                    ts.id as topic_status_id,
                    ts.title,
                    ts.status,
                    ts.error_message,
                    ts.created_at,
                    ts.updated_at,
                    t.id as topic_id
                FROM topic_status ts
                LEFT JOIN topics t ON ts.title = t.title
                WHERE ts.status = ?
                ORDER BY ts.created_at ASC
            """
        
        if limit:
            query += f" LIMIT {limit}"
        
        cursor.execute(query, (status,))
        rows = cursor.fetchall()
        
        topics = []
        for row in rows:
            topic_dict = dict(row)
            
            # Add 'title' key for backward compatibility
            if 'original_title' in columns:
                # Use current_title if available, otherwise original_title
                topic_dict['title'] = topic_dict.get('current_title') or topic_dict.get('original_title')
            # else: 'title' key already exists from the query
            
            # If topic doesn't have an ID yet, assign next available
            if not topic_dict.get('topic_id'):
                cursor.execute("SELECT COALESCE(MAX(id), 0) + 1 FROM topics")
                topic_dict['id'] = cursor.fetchone()[0] + len(topics)
            else:
                topic_dict['id'] = topic_dict['topic_id']
            
            topics.append(topic_dict)
        
        logger.debug(f"Retrieved {len(topics)} topics with status '{status}'")
        return topics
    
    @db_operation(commit=False)
    def get_pending_topics_count(self, cursor) -> int:
        """Get count of pending topics."""
        cursor.execute("SELECT COUNT(*) as count FROM topic_status WHERE status = 'pending'")
        return cursor.fetchone()['count']
    
    @db_operation(commit=False)
    def get_processing_summary(self, cursor) -> Dict[str, Any]:
        """Get summary of processing status across all topics."""
        cursor.execute("""
            SELECT status, COUNT(*) as count 
            FROM topic_status 
            GROUP BY status
        """)
        
        summary = {
            'pending': 0,
            'processing': 0,
            'completed': 0,
            'failed': 0
        }
        
        for row in cursor.fetchall():
            if row['status'] in summary:
                summary[row['status']] = row['count']
        
        # Get recent failed topics with details
        cursor.execute("PRAGMA table_info(topic_status)")
        columns = {row[1] for row in cursor.fetchall()}
        
        if 'original_title' in columns:
            cursor.execute("""
                SELECT COALESCE(original_title, current_title) as title, error_message, created_at
                FROM topic_status
                WHERE status = 'failed'
                ORDER BY created_at DESC
                LIMIT 10
            """)
        else:
            cursor.execute("""
                SELECT title, error_message, created_at
                FROM topic_status
                WHERE status = 'failed'
                ORDER BY created_at DESC
                LIMIT 10
            """)
        
        failed_topics = []
        for row in cursor.fetchall():
            failed_topics.append(dict(row))
        
        summary['recent_failures'] = failed_topics
        summary['total'] = sum(summary[k] for k in ['pending', 'processing', 'completed', 'failed'])
        
        logger.debug(f"Processing summary: {summary['total']} total topics")
        return summary
    
    # ===== ASYNC METHODS FOR CONTENT GENERATION =====
    
    async def get_job_results(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Get job results."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            # Get job info
            cursor.execute("SELECT * FROM jobs WHERE id = ?", (job_id,))
            job_row = cursor.fetchone()
            
            if not job_row:
                return None
            
            # Get results
            cursor.execute("SELECT * FROM results WHERE job_id = ?", (job_id,))
            result_rows = cursor.fetchall()
            
            results = []
            for row in result_rows:
                try:
                    content = json.loads(row['content'])
                    results.append({
                        'platform': row['platform'],
                        'format': row['format'],
                        'envelope': {
                            'content': content
                        }
                    })
                except json.JSONDecodeError:
                    logger.warning(f"Failed to parse result content for job {job_id}")
                    continue
            
            return {
                'jobId': job_id,
                'status': job_row['status'],
                'results': results
            }
        except Exception as e:
            logger.error(f"Error getting job results: {e}", exc_info=True)
            return {
                'jobId': job_id,
                'status': 'error',
                'results': [],
                'errors': [str(e)]
            }
    
    async def get_results_by_topic(self, topic_id: str) -> List[Dict[str, Any]]:
        """Get all job results for a specific topic."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            # Get all jobs for this topic
            cursor.execute("SELECT id FROM jobs WHERE topic_id = ?", (topic_id,))
            job_rows = cursor.fetchall()
            
            all_results = []
            for job_row in job_rows:
                job_id = job_row['id']
                
                # Get results for this job
                cursor.execute("SELECT * FROM results WHERE job_id = ?", (job_id,))
                result_rows = cursor.fetchall()
                
                for row in result_rows:
                    try:
                        content = json.loads(row['content'])
                        all_results.append({
                            'job_id': job_id,
                            'platform': row['platform'],
                            'format': row['format'],
                            'topic_id': int(topic_id),
                            'envelope': {
                                'content': content
                            }
                        })
                    except (json.JSONDecodeError, ValueError) as e:
                        logger.warning(f"Failed to parse result: {e}")
                        continue
            
            logger.debug(f"Retrieved {len(all_results)} results for topic {topic_id}")
            return all_results
        except Exception as e:
            logger.error(f"Error getting results by topic: {e}", exc_info=True)
            return []


# Global instance for backward compatibility
unified_db = UnifiedDatabase()
