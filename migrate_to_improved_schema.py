#!/usr/bin/env python3
"""
Migration script to upgrade existing database to improved schema.
Handles data migration from old topic_status table to new structure.
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path


def migrate_database(db_path: str = "unified.db"):
    """Migrate existing database to improved schema."""
    
    backup_path = f"{db_path}.backup_{int(datetime.now().timestamp())}"
    
    print(f"🔄 Starting database migration...")
    print(f"📦 Creating backup: {backup_path}")
    
    # Create backup
    try:
        import shutil
        shutil.copy2(db_path, backup_path)
        print(f"✅ Backup created successfully")
    except Exception as e:
        print(f"❌ Failed to create backup: {e}")
        return False
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if migration is needed
        cursor.execute("PRAGMA table_info(topic_status)")
        columns = [row[1] for row in cursor.fetchall()]
        
        if 'original_title' in columns:
            print("✅ Database already uses improved schema")
            return True
        
        print("🔧 Migrating to improved schema...")
        
        # Step 1: Create new topic_status table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS topic_status_new (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                original_title TEXT NOT NULL,
                current_title TEXT,
                status TEXT NOT NULL DEFAULT 'pending',
                error_message TEXT,
                processing_started_at TIMESTAMP,
                processing_completed_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Step 2: Migrate existing data
        cursor.execute("SELECT * FROM topic_status")
        old_records = cursor.fetchall()
        
        # Get column names from old table
        cursor.execute("PRAGMA table_info(topic_status)")
        old_columns = [row[1] for row in cursor.fetchall()]
        
        print(f"📊 Migrating {len(old_records)} existing records...")
        
        migrated_count = 0
        for record in old_records:
            record_dict = dict(zip(old_columns, record))
            
            # Extract data from old record
            old_id = record_dict.get('id')
            title = record_dict.get('title', '')
            status = record_dict.get('status', 'pending')
            error_message = record_dict.get('error_message')
            created_at = record_dict.get('created_at')
            updated_at = record_dict.get('updated_at')
            
            # Insert into new table
            cursor.execute("""
                INSERT INTO topic_status_new 
                (original_title, current_title, status, error_message, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (title, title, status, error_message, created_at, updated_at))
            
            migrated_count += 1
        
        print(f"✅ Migrated {migrated_count} records to new schema")
        
        # Step 3: Replace old table with new one
        cursor.execute("DROP TABLE topic_status")
        cursor.execute("ALTER TABLE topic_status_new RENAME TO topic_status")
        
        # Step 4: Update topics table to add foreign key column (if it exists)
        cursor.execute("PRAGMA table_info(topics)")
        topics_columns = [row[1] for row in cursor.fetchall()]
        
        if 'topic_status_id' not in topics_columns:
            print("🔧 Adding topic_status_id column to topics table...")
            cursor.execute("ALTER TABLE topics ADD COLUMN topic_status_id INTEGER")
            
            # Try to link existing topics with topic_status based on title
            cursor.execute("""
                UPDATE topics 
                SET topic_status_id = (
                    SELECT ts.id 
                    FROM topic_status ts 
                    WHERE ts.original_title = topics.title 
                       OR ts.current_title = topics.title
                    LIMIT 1
                )
                WHERE topic_status_id IS NULL
            """)
            
            linked_count = cursor.rowcount
            print(f"🔗 Linked {linked_count} existing topics with their status records")
        
        # Step 5: Create indexes
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_topic_status_original_title ON topic_status(original_title)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_topic_status_status ON topic_status(status)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_topics_status_id ON topics(topic_status_id)")
        
        conn.commit()
        print("✅ Database migration completed successfully!")
        
        # Step 6: Verify migration
        cursor.execute("SELECT COUNT(*) FROM topic_status")
        new_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM topics WHERE topic_status_id IS NOT NULL")
        linked_topics = cursor.fetchone()[0]
        
        print(f"📊 Migration Summary:")
        print(f"   - Topic Status Records: {new_count}")
        print(f"   - Linked Topics: {linked_topics}")
        
        return True
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        conn.rollback()
        
        # Restore from backup
        try:
            conn.close()
            import shutil
            shutil.copy2(backup_path, db_path)
            print(f"🔄 Database restored from backup")
        except:
            print(f"⚠️ Failed to restore backup. Manual restore may be needed from: {backup_path}")
        
        return False
    
    finally:
        conn.close()


def verify_migration(db_path: str = "unified.db"):
    """Verify that migration was successful."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check new schema
        cursor.execute("PRAGMA table_info(topic_status)")
        columns = [row[1] for row in cursor.fetchall()]
        
        required_columns = ['original_title', 'current_title', 'status', 'error_message']
        missing_columns = [col for col in required_columns if col not in columns]
        
        if missing_columns:
            print(f"❌ Missing columns: {missing_columns}")
            return False
        
        # Check data integrity
        cursor.execute("SELECT COUNT(*) FROM topic_status")
        status_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM topics")
        topics_count = cursor.fetchone()[0]
        
        print(f"✅ Schema verification passed")
        print(f"📊 Records: {status_count} topic_status, {topics_count} topics")
        
        return True
        
    finally:
        conn.close()


def main():
    """Main migration script."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Migrate database to improved schema')
    parser.add_argument('--db-path', default='unified.db', help='Path to database file')
    parser.add_argument('--verify-only', action='store_true', help='Only verify migration')
    
    args = parser.parse_args()
    
    if args.verify_only:
        success = verify_migration(args.db_path)
        exit(0 if success else 1)
    
    success = migrate_database(args.db_path)
    
    if success:
        verify_migration(args.db_path)
        print("\n🎉 Migration completed successfully!")
        print("You can now use the improved batch processor with proper ID tracking.")
    else:
        print("\n❌ Migration failed. Check the error messages above.")
        exit(1)


if __name__ == "__main__":
    main()
