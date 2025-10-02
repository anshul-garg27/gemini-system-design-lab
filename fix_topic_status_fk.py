#!/usr/bin/env python3
"""
Fix topic_status table foreign key constraint.
The FK constraint on id->topics(id) is causing issues because we create
topic_status entries BEFORE the topic is generated and saved to topics table.
"""

import sqlite3
import sys

def fix_foreign_key():
    """Remove the problematic foreign key from topic_status table."""
    
    db_path = "unified.db"
    print(f"Fixing foreign key constraint in {db_path}...")
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        # Get current data
        print("Backing up existing data...")
        cursor.execute("SELECT * FROM topic_status")
        existing_data = cursor.fetchall()
        print(f"Found {len(existing_data)} existing records")
        
        # Drop the old table
        print("Dropping old table...")
        cursor.execute("DROP TABLE IF EXISTS topic_status")
        
        # Create new table WITHOUT the foreign key constraint
        print("Creating new table without foreign key...")
        cursor.execute("""
            CREATE TABLE topic_status (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                original_title TEXT NOT NULL UNIQUE,
                current_title TEXT,
                status TEXT NOT NULL,
                error_message TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Re-insert data
        if existing_data:
            print(f"Restoring {len(existing_data)} records...")
            for row in existing_data:
                cursor.execute("""
                    INSERT INTO topic_status 
                    (id, original_title, current_title, status, error_message, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    row['id'],
                    row['original_title'],
                    row['current_title'],
                    row['status'],
                    row['error_message'],
                    row['created_at'],
                    row['updated_at']
                ))
        
        conn.commit()
        print("✅ Successfully fixed foreign key constraint")
        print("\nNew schema:")
        cursor.execute("SELECT sql FROM sqlite_master WHERE name='topic_status'")
        print(cursor.fetchone()[0])
        
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        conn.rollback()
        return False
    finally:
        conn.close()
    
    return True

if __name__ == "__main__":
    success = fix_foreign_key()
    sys.exit(0 if success else 1)
