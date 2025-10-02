#!/usr/bin/env python3
"""
Improved Unified Database Manager with proper consistency handling.
Fixes the ID tracking and update issues.
"""

import sqlite3
import json
import os
import hashlib
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path


class ImprovedUnifiedDatabase:
    """Improved unified SQLite database manager with proper consistency."""
    
    def __init__(self, db_path: str = "unified.db"):
        """Initialize the improved unified database manager."""
        self.db_path = db_path
        self.cache_dir = Path("./data/cache")
        self.cache_dir.mkdir(exist_ok=True)
        self._init_database()
    
    def _init_database(self):
        """Initialize the database with improved schema."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Improved topic_status table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS topic_status (
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
        
        # Improved topics table with foreign key
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS topics (
                id INTEGER PRIMARY KEY,
                topic_status_id INTEGER,
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
                FOREIGN KEY (topic_status_id) REFERENCES topic_status (id),
                UNIQUE(id)
            )
        """)
        
        # Other existing tables (jobs, tasks, results, prompts)
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
        
        # Create indexes
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_topic_status_original_title ON topic_status(original_title)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_topic_status_status ON topic_status(status)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_topics_status_id ON topics(topic_status_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_jobs_status ON jobs(status)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_tasks_job_id ON tasks(job_id)")
        
        conn.commit()
        conn.close()
    
    def get_connection(self):
        """Get database connection."""
        return sqlite3.connect(self.db_path)
    
    # ===== IMPROVED TOPIC STATUS MANAGEMENT =====
    
    def add_topic_for_processing(self, original_title: str) -> int:
        """Add a new topic for processing and return its ID."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO topic_status (original_title, status)
                VALUES (?, 'pending')
            """, (original_title,))
            conn.commit()
            
            # Get the inserted ID
            topic_status_id = cursor.lastrowid
            return topic_status_id
            
        except Exception as e:
            print(f"Error adding topic for processing: {e}")
            return None
        finally:
            conn.close()
    
    def update_topic_status_by_id(self, topic_status_id: int, status: str, 
                                 current_title: str = None, error_message: str = None) -> bool:
        """Update topic status by ID instead of title."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Build dynamic update query
            update_fields = ["status = ?", "updated_at = CURRENT_TIMESTAMP"]
            params = [status]
            
            if current_title:
                update_fields.append("current_title = ?")
                params.append(current_title)
            
            if error_message:
                update_fields.append("error_message = ?")
                params.append(error_message)
            
            if status == 'processing':
                update_fields.append("processing_started_at = CURRENT_TIMESTAMP")
            elif status in ['completed', 'failed']:
                update_fields.append("processing_completed_at = CURRENT_TIMESTAMP")
            
            params.append(topic_status_id)
            
            query = f"""
                UPDATE topic_status 
                SET {', '.join(update_fields)}
                WHERE id = ?
            """
            
            cursor.execute(query, params)
            conn.commit()
            
            return cursor.rowcount > 0
            
        except Exception as e:
            print(f"Error updating topic status: {e}")
            return False
        finally:
            conn.close()
    
    def get_pending_topics_with_ids(self) -> List[Tuple[int, str]]:
        """Get all pending topics with their IDs."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT id, original_title 
                FROM topic_status 
                WHERE status = 'pending'
                ORDER BY created_at ASC
            """)
            return cursor.fetchall()
        finally:
            conn.close()
    
    def save_generated_topic_with_status_id(self, topic_data: Dict[str, Any], topic_status_id: int) -> bool:
        """Save generated topic with reference to topic_status ID."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Serialize JSON fields
            def serialize_json_field(field_value):
                if isinstance(field_value, (list, dict)):
                    return json.dumps(field_value, ensure_ascii=False)
                elif isinstance(field_value, str):
                    try:
                        # Try to parse as JSON to validate
                        json.loads(field_value)
                        return field_value
                    except:
                        # If it's not valid JSON, wrap it as a single-item array
                        return json.dumps([field_value], ensure_ascii=False)
                else:
                    return json.dumps(field_value, ensure_ascii=False)
            
            cursor.execute("""
                INSERT OR REPLACE INTO topics (
                    id, topic_status_id, title, description, category, subcategory, company,
                    technologies, complexity_level, tags, related_topics, metrics,
                    implementation_details, learning_objectives, difficulty,
                    estimated_read_time, prerequisites, created_date, updated_date, source
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                topic_data.get('id'),
                topic_status_id,
                topic_data.get('title', ''),
                topic_data.get('description', ''),
                topic_data.get('category', ''),
                topic_data.get('subcategory', ''),
                topic_data.get('company', ''),
                serialize_json_field(topic_data.get('technologies', [])),
                topic_data.get('complexity_level', ''),
                serialize_json_field(topic_data.get('tags', [])),
                serialize_json_field(topic_data.get('related_topics', [])),
                serialize_json_field(topic_data.get('metrics', {})),
                serialize_json_field(topic_data.get('implementation_details', {})),
                serialize_json_field(topic_data.get('learning_objectives', [])),
                topic_data.get('difficulty', 0),
                topic_data.get('estimated_read_time', ''),
                serialize_json_field(topic_data.get('prerequisites', [])),
                topic_data.get('created_date', ''),
                topic_data.get('updated_date', ''),
                topic_data.get('source', 'web_batch')
            ))
            
            conn.commit()
            return True
            
        except Exception as e:
            print(f"Error saving generated topic: {e}")
            return False
        finally:
            conn.close()
    
    def get_topic_with_status(self, topic_status_id: int) -> Optional[Dict[str, Any]]:
        """Get topic with its status information."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT 
                    ts.id as status_id,
                    ts.original_title,
                    ts.current_title,
                    ts.status,
                    ts.error_message,
                    ts.processing_started_at,
                    ts.processing_completed_at,
                    ts.created_at as status_created_at,
                    ts.updated_at as status_updated_at,
                    t.id as topic_id,
                    t.title as final_title,
                    t.description,
                    t.category,
                    t.generated_at
                FROM topic_status ts
                LEFT JOIN topics t ON ts.id = t.topic_status_id
                WHERE ts.id = ?
            """, (topic_status_id,))
            
            row = cursor.fetchone()
            if row:
                columns = [desc[0] for desc in cursor.description]
                return dict(zip(columns, row))
            return None
            
        finally:
            conn.close()
    
    def get_processing_statistics(self) -> Dict[str, Any]:
        """Get comprehensive processing statistics."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Status counts
            cursor.execute("""
                SELECT status, COUNT(*) 
                FROM topic_status 
                GROUP BY status
            """)
            status_counts = dict(cursor.fetchall())
            
            # Completion rate
            cursor.execute("""
                SELECT 
                    COUNT(*) as total,
                    SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed,
                    SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END) as failed,
                    SUM(CASE WHEN status = 'processing' THEN 1 ELSE 0 END) as processing
                FROM topic_status
            """)
            stats = cursor.fetchone()
            
            total, completed, failed, processing = stats
            completion_rate = (completed / total * 100) if total > 0 else 0
            
            return {
                'status_counts': status_counts,
                'total_topics': total,
                'completed': completed,
                'failed': failed,
                'processing': processing,
                'pending': total - completed - failed - processing,
                'completion_rate': round(completion_rate, 2)
            }
            
        finally:
            conn.close()


# Create global instance
improved_unified_db = ImprovedUnifiedDatabase()
