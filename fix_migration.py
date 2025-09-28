#!/usr/bin/env python3
"""
Fix migration script to properly copy data from topics.db to unified.db
"""

import sqlite3
from pathlib import Path


def fix_migration():
    """Copy data directly from topics.db to unified.db using SQL."""
    print("🔧 Fixing migration with direct SQL copy...")
    
    # Connect to both databases
    old_conn = sqlite3.connect("topics.db")
    new_conn = sqlite3.connect("unified.db")
    
    old_cursor = old_conn.cursor()
    new_cursor = new_conn.cursor()
    
    try:
        # Drop existing topics table in unified.db
        new_cursor.execute("DROP TABLE IF EXISTS topics")
        
        # Create the correct topics table schema
        new_cursor.execute("""
            CREATE TABLE topics (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                category TEXT NOT NULL,
                subcategory TEXT NOT NULL,
                company TEXT NOT NULL,
                technologies TEXT NOT NULL,  -- JSON array
                complexity_level TEXT NOT NULL,
                tags TEXT NOT NULL,  -- JSON array
                related_topics TEXT NOT NULL,  -- JSON array
                metrics TEXT NOT NULL,  -- JSON object
                implementation_details TEXT NOT NULL,  -- JSON object
                learning_objectives TEXT NOT NULL,  -- JSON array
                difficulty INTEGER NOT NULL,
                estimated_read_time TEXT NOT NULL,
                prerequisites TEXT NOT NULL,  -- JSON array
                created_date TEXT NOT NULL,
                updated_date TEXT NOT NULL,
                generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                source TEXT DEFAULT 'migrated',
                UNIQUE(id)
            )
        """)
        
        # Create indexes
        new_cursor.execute("CREATE INDEX idx_topics_category ON topics(category)")
        new_cursor.execute("CREATE INDEX idx_topics_company ON topics(company)")
        new_cursor.execute("CREATE INDEX idx_topics_complexity ON topics(complexity_level)")
        new_cursor.execute("CREATE INDEX idx_topics_difficulty ON topics(difficulty)")
        
        # Copy all data from old to new
        old_cursor.execute("SELECT * FROM topics")
        topics = old_cursor.fetchall()
        
        print(f"📊 Copying {len(topics)} topics...")
        
        for topic in topics:
            # Add 'migrated' as source
            topic_with_source = topic + ('migrated',)
            
            new_cursor.execute("""
                INSERT INTO topics 
                (id, title, description, category, subcategory, company, technologies,
                 complexity_level, tags, related_topics, metrics, implementation_details,
                 learning_objectives, difficulty, estimated_read_time, prerequisites,
                 created_date, updated_date, generated_at, source)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, topic_with_source)
        
        # Copy topic_status data
        old_cursor.execute("SELECT * FROM topic_status")
        statuses = old_cursor.fetchall()
        
        print(f"📊 Copying {len(statuses)} topic statuses...")
        
        for status in statuses:
            # topic_status table has: id, title, status, error_message, created_at, updated_at
            # But our unified schema expects: id, topic_id, title, status, error_message, created_at, updated_at
            # So we need to add a topic_id (we'll use the id as topic_id for now)
            status_with_topic_id = (status[0], status[0], status[1], status[2], status[3], status[4], status[5])
            
            new_cursor.execute("""
                INSERT OR REPLACE INTO topic_status 
                (id, topic_id, title, status, error_message, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, status_with_topic_id)
        
        new_conn.commit()
        print("✅ Migration fixed successfully!")
        
        # Show final stats
        new_cursor.execute("SELECT COUNT(*) FROM topics")
        topic_count = new_cursor.fetchone()[0]
        
        new_cursor.execute("SELECT COUNT(*) FROM topic_status")
        status_count = new_cursor.fetchone()[0]
        
        print(f"📈 Final Stats:")
        print(f"   Topics: {topic_count}")
        print(f"   Statuses: {status_count}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        old_conn.close()
        new_conn.close()


if __name__ == "__main__":
    fix_migration()
