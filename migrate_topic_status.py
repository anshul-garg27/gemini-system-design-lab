#!/usr/bin/env python3
"""
Migration script to update topic_status table with new columns for worker-based processing.
"""
import sqlite3
import os
import sys

def migrate_database(db_path="unified.db"):
    """Migrate the topic_status table to add new columns."""
    
    if not os.path.exists(db_path):
        print(f"Database {db_path} not found")
        return False
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check current schema
        cursor.execute("PRAGMA table_info(topic_status)")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]
        
        print("Current columns:", column_names)
        
        # Add missing columns if they don't exist
        columns_to_add = [
            ("worker_id", "TEXT"),
            ("started_at", "TIMESTAMP"),
            ("finished_at", "TIMESTAMP"), 
            ("retry_count", "INTEGER DEFAULT 0"),
            ("payload", "TEXT")
        ]
        
        for column_name, column_type in columns_to_add:
            if column_name not in column_names:
                try:
                    alter_query = f"ALTER TABLE topic_status ADD COLUMN {column_name} {column_type}"
                    cursor.execute(alter_query)
                    print(f"Added column: {column_name}")
                except sqlite3.OperationalError as e:
                    print(f"Column {column_name} might already exist or error: {e}")
        
        # Check if title column has UNIQUE constraint
        cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='topic_status'")
        table_sql = cursor.fetchone()[0]
        
        if "UNIQUE" not in table_sql.upper() or "title TEXT NOT NULL UNIQUE" not in table_sql:
            print("\nWARNING: title column doesn't have UNIQUE constraint.")
            print("To add it, you'll need to recreate the table. Current table structure:")
            print(table_sql)
            print("\nConsider backing up and recreating the table with:")
            print("""
CREATE TABLE topic_status_new (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL,
    error_message TEXT,
    worker_id TEXT,
    started_at TIMESTAMP,
    finished_at TIMESTAMP,
    retry_count INTEGER DEFAULT 0,
    payload TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO topic_status_new (title, status, error_message, created_at, updated_at)
SELECT title, status, error_message, created_at, updated_at FROM topic_status;

DROP TABLE topic_status;
ALTER TABLE topic_status_new RENAME TO topic_status;
            """)
        
        conn.commit()
        
        # Verify the migration
        cursor.execute("PRAGMA table_info(topic_status)")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]
        
        print("\nColumns after migration:", column_names)
        
        # Check for pending topics
        cursor.execute("SELECT COUNT(*) FROM topic_status WHERE status = 'pending'")
        pending_count = cursor.fetchone()[0]
        print(f"\nPending topics in database: {pending_count}")
        
        print("\nMigration completed successfully!")
        return True
        
    except Exception as e:
        print(f"Migration failed: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

if __name__ == "__main__":
    db_path = sys.argv[1] if len(sys.argv) > 1 else "unified.db"
    success = migrate_database(db_path)
    sys.exit(0 if success else 1)
