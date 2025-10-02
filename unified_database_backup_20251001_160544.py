#!/usr/bin/env python3
"""
Unified SQLite database manager for both topic generation and content generation.
Combines functionality from both Flask and FastAPI backends.
"""

import sqlite3
import json
import os
import hashlib
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path


class UnifiedDatabase:
    """Unified SQLite database manager for system design topics and content generation."""
    
    def __init__(self, db_path: str = "unified.db"):
        """Initialize the unified database manager.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.cache_dir = Path("./data/cache")
        self.cache_dir.mkdir(exist_ok=True)
        self._init_database()
    
    def _init_database(self):
        """Initialize the database with all required tables."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Topics table (comprehensive schema matching original topics.db)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS topics (
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
                source TEXT DEFAULT 'web_batch',
                UNIQUE(id)
            )
        """)
        
        # Topic status table (enhanced schema with original_title/current_title)
        # Check if table exists and has old schema
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='topic_status'")
        table_exists = cursor.fetchone()
        
        if table_exists:
            # Check current schema
            cursor.execute("PRAGMA table_info(topic_status)")
            columns = {row[1] for row in cursor.fetchall()}
            
            # If old schema (has 'title'), keep it for backward compatibility
            if 'title' in columns and 'original_title' not in columns:
                # Old schema exists, don't recreate
                pass
            elif 'original_title' not in columns:
                # Neither old nor new schema, create new
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
        else:
            # Table doesn't exist, create with new schema
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
        
        # Jobs table (from FastAPI backend)
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
        
        # Tasks table (from FastAPI backend)
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
        
        # Results table (from FastAPI backend)
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
        
        # Prompts table (from FastAPI backend)
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
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_topics_category ON topics(category)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_topics_company ON topics(company)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_topics_complexity ON topics(complexity_level)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_topics_difficulty ON topics(difficulty)")
        
        # Check topic_status schema for correct index
        cursor.execute("PRAGMA table_info(topic_status)")
        topic_status_columns = {row[1] for row in cursor.fetchall()}
        
        if 'title' in topic_status_columns:
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_topic_status_title ON topic_status(title)")
        if 'original_title' in topic_status_columns:
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_topic_status_original_title ON topic_status(original_title)")
        if 'current_title' in topic_status_columns:
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_topic_status_current_title ON topic_status(current_title)")
        
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_topic_status_status ON topic_status(status)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_jobs_status ON jobs(status)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_tasks_job_id ON tasks(job_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_results_job_id ON results(job_id)")
        
        conn.commit()
        conn.close()
    
    def get_connection(self):
        """Get database connection."""
        return sqlite3.connect(self.db_path)
    
    # ===== TOPIC MANAGEMENT (from Flask backend) =====
    
    def save_topic(self, topic: Dict[str, Any], source: str = "web_batch") -> bool:
        """Save a topic to the database with comprehensive schema."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Handle JSON serialization for array/object fields
            def serialize_json_field(field_value):
                if isinstance(field_value, (list, dict)):
                    return json.dumps(field_value)
                elif isinstance(field_value, str):
                    # If it's already a JSON string, return as is
                    try:
                        json.loads(field_value)
                        return field_value
                    except (json.JSONDecodeError, TypeError):
                        # If it's not valid JSON, treat as regular string
                        return field_value
                else:
                    return field_value or ""
            
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
                serialize_json_field(topic.get('technologies', [])),
                topic.get('complexity_level', ''),
                serialize_json_field(topic.get('tags', [])),
                serialize_json_field(topic.get('related_topics', [])),
                serialize_json_field(topic.get('metrics', {})),
                serialize_json_field(topic.get('implementation_details', {})),
                serialize_json_field(topic.get('learning_objectives', [])),
                topic.get('difficulty', 5),
                topic.get('estimated_read_time', ''),
                serialize_json_field(topic.get('prerequisites', [])),
                topic.get('created_date', datetime.now().strftime("%Y-%m-%d")),
                topic.get('updated_date', datetime.now().strftime("%Y-%m-%d")),
                source
            ))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error saving topic: {e}")
            return False
        finally:
            conn.close()
    
    def save_topic_status(self, title: str, status: str, error_message: str = None) -> bool:
        """
        Save topic processing status.
        DEPRECATED: Use add_topic_for_processing() and update_topic_status_by_id() instead.
        This is kept for backward compatibility.
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Check schema first
            cursor.execute("PRAGMA table_info(topic_status)")
            columns = {row[1] for row in cursor.fetchall()}
            
            if 'original_title' in columns:
                # New schema - check if exists first
                cursor.execute("SELECT id FROM topic_status WHERE original_title = ?", (title,))
                existing = cursor.fetchone()
                
                if existing:
                    # Update existing
                    cursor.execute("""
                        UPDATE topic_status 
                        SET status = ?, error_message = ?, updated_at = CURRENT_TIMESTAMP
                        WHERE id = ?
                    """, (status, error_message, existing[0]))
                else:
                    # Insert new
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
            
            conn.commit()
            return True
        except Exception as e:
            print(f"Error saving topic status: {e}")
            return False
        finally:
            conn.close()
    
    def get_next_available_id(self) -> int:
        """Get the next available ID for a new topic."""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT MAX(id) FROM topics")
            result = cursor.fetchone()
            max_id = result[0] if result[0] is not None else 0
            return max_id + 1
        finally:
            conn.close()
    
    def get_topics_paginated(self, limit: int = 20, offset: int = 0, 
                           search: str = None, category: str = None, 
                           subcategory: str = None, status: str = None, 
                           complexity: str = None, company: str = None, 
                           sort_by: str = "created_date", 
                           sort_order: str = "desc") -> List[Dict[str, Any]]:
        """Get topics with pagination and filtering."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
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
        
        # Build query
        if status:
            query = f"""
                SELECT topics.*, topic_status.status, topic_status.error_message
                FROM topics
                LEFT JOIN topic_status ON topics.title = topic_status.title
                {where_clause}
                {order_clause}
                LIMIT ? OFFSET ?
            """
            params.extend([limit, offset])
        else:
            query = f"""
                SELECT topics.*, topic_status.status, topic_status.error_message
                FROM topics
                LEFT JOIN topic_status ON topics.title = topic_status.title
                {where_clause}
                {order_clause}
                LIMIT ? OFFSET ?
            """
            params.extend([limit, offset])
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        # Convert to list of dictionaries
        columns = [description[0] for description in cursor.description]
        topics = []
        for row in rows:
            topic = dict(zip(columns, row))
            topics.append(topic)
        
        conn.close()
        return topics
    
    def get_topics_count(self, search: str = None, category: str = None, 
                        subcategory: str = None, status: str = None, 
                        complexity: str = None, company: str = None) -> int:
        """Get total count of topics matching filters."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Build WHERE clause (same logic as get_topics_paginated)
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
        
        if status:
            query = f"""
                SELECT COUNT(*)
                FROM topics
                LEFT JOIN topic_status ON topics.title = topic_status.title
                {where_clause}
            """
        else:
            query = f"""
                SELECT COUNT(*)
                FROM topics
                LEFT JOIN topic_status ON topics.title = topic_status.title
                {where_clause}
            """
        
        cursor.execute(query, params)
        count = cursor.fetchone()[0]
        conn.close()
        return count
    
    def topic_exists_and_completed(self, title: str) -> bool:
        """Check if topic exists and is completed."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT COUNT(*) FROM topic_status 
            WHERE title = ? AND status = 'completed'
        """, (title,))
        
        count = cursor.fetchone()[0]
        conn.close()
        return count > 0
    
    def get_next_available_id(self) -> int:
        """Get the next available topic ID."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COALESCE(MAX(id), 0) + 1 FROM topics")
        next_id = cursor.fetchone()[0]
        conn.close()
        return next_id
    
    # ===== IMPROVED CONSISTENCY METHODS =====
    
    def add_topic_for_processing(self, original_title: str) -> int:
        """
        Add a new topic for processing and return its status ID.
        This ensures we have a unique ID to track throughout processing.
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Check schema to use correct column
            cursor.execute("PRAGMA table_info(topic_status)")
            columns = {row[1] for row in cursor.fetchall()}
            
            if 'original_title' in columns:
                # New schema with original_title/current_title
                cursor.execute("""
                    INSERT INTO topic_status (original_title, status)
                    VALUES (?, 'pending')
                """, (original_title,))
            else:
                # Old schema with just title
                cursor.execute("""
                    INSERT INTO topic_status (title, status)
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
                                 error_message: str = None, current_title: str = None) -> bool:
        """
        Update topic status by ID instead of title.
        This prevents duplicate entries and ensures consistency.
        
        Args:
            topic_status_id: The ID of the topic_status record
            status: New status (pending/processing/completed/failed)
            error_message: Error message if status is 'failed'
            current_title: Cleaned title from Gemini (updates current_title column)
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Check schema to know which columns are available
            cursor.execute("PRAGMA table_info(topic_status)")
            columns = {row[1] for row in cursor.fetchall()}
            
            has_current_title = 'current_title' in columns
            
            # Build UPDATE query based on available columns and parameters
            if has_current_title and current_title:
                # Update status, current_title, and optionally error_message
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
                # Update only status and optionally error_message
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
            
            conn.commit()
            return cursor.rowcount > 0
            
        except Exception as e:
            print(f"Error updating topic status: {e}")
            return False
        finally:
            conn.close()
    
    def get_pending_topics_with_ids(self, limit: int = None) -> List[tuple]:
        """
        Get all pending topics with their IDs.
        Returns list of (id, title) tuples instead of just titles.
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            if limit:
                cursor.execute("""
                    SELECT id, title 
                    FROM topic_status 
                    WHERE status = 'pending'
                    ORDER BY created_at ASC
                    LIMIT ?
                """, (limit,))
            else:
                cursor.execute("""
                    SELECT id, title 
                    FROM topic_status 
                    WHERE status = 'pending'
                    ORDER BY created_at ASC
                """)
            
            return cursor.fetchall()
        finally:
            conn.close()
    
    def get_topic_status_by_title(self, title: str) -> Optional[Dict[str, Any]]:
        """
        Get topic_status record by title.
        Returns the topic_status_id and other details.
        Works with both old (title) and new (original_title/current_title) schemas.
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Check schema
            cursor.execute("PRAGMA table_info(topic_status)")
            columns = {row[1] for row in cursor.fetchall()}
            
            if 'original_title' in columns:
                # New schema - check both original_title and current_title
                cursor.execute("""
                    SELECT id, original_title, current_title, status, error_message, created_at, updated_at
                    FROM topic_status
                    WHERE original_title = ? OR current_title = ?
                    ORDER BY created_at DESC
                    LIMIT 1
                """, (title, title))
                
                row = cursor.fetchone()
                if row:
                    return {
                        'id': row[0],
                        'title': row[1] or row[2],  # Use original_title or current_title
                        'original_title': row[1],
                        'current_title': row[2],
                        'status': row[3],
                        'error_message': row[4],
                        'created_at': row[5],
                        'updated_at': row[6]
                    }
            else:
                # Old schema with just title
                cursor.execute("""
                    SELECT id, title, status, error_message, created_at, updated_at
                    FROM topic_status
                    WHERE title = ?
                    ORDER BY created_at DESC
                    LIMIT 1
                """, (title,))
                
                row = cursor.fetchone()
                if row:
                    return {
                        'id': row[0],
                        'title': row[1],
                        'status': row[2],
                        'error_message': row[3],
                        'created_at': row[4],
                        'updated_at': row[5]
                    }
            
            return None
        except Exception as e:
            print(f"Error getting topic status by title: {e}")
            return None
        finally:
            conn.close()
    
    def cleanup_failed_topics(self) -> Dict[str, Any]:
        """Clean up failed topics from the database."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Count failed topics
            cursor.execute("SELECT COUNT(*) FROM topic_status WHERE status = 'failed'")
            failed_count = cursor.fetchone()[0]
            
            if failed_count > 0:
                # Delete failed topics
                cursor.execute("DELETE FROM topic_status WHERE status = 'failed'")
                conn.commit()
                
                return {
                    'success': True,
                    'message': f'Cleaned up {failed_count} failed topics',
                    'count': failed_count
                }
            else:
                return {
                    'success': True,
                    'message': 'No failed topics to clean up',
                    'count': 0
                }
        except Exception as e:
            return {
                'success': False,
                'message': f'Error cleaning up topics: {str(e)}',
                'count': 0
            }
        finally:
            conn.close()
    
    def get_topic_status(self, topic_id: int) -> Optional[Dict[str, Any]]:
        """Get topic status by ID."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT * FROM topic_status WHERE id = ?", (topic_id,))
            row = cursor.fetchone()
            if not row:
                return None
            
            return {
                'id': row[0],
                'title': row[1],
                'status': row[2],
                'error_message': row[3],
                'created_at': row[4],
                'updated_at': row[5]
            }
        except Exception as e:
            print(f"Error getting topic status: {e}")
            return None
        finally:
            conn.close()
    
    def get_topic_status_summary(self) -> Dict[str, Any]:
        """Get summary of topic statuses."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT status, COUNT(*) as count
            FROM topic_status
            GROUP BY status
        """)
        
        rows = cursor.fetchall()
        summary = {}
        for row in rows:
            summary[row[0]] = row[1]
        
        conn.close()
        return {'summary': summary}
    
    def get_all_topic_ids(self) -> List[int]:
        """Get all topic IDs for cross-linking."""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id FROM topics ORDER BY id")
            return [row[0] for row in cursor.fetchall()]
        finally:
            conn.close()

    def get_stats(self) -> Dict[str, Any]:
        """Get database statistics."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Total topics
        cursor.execute("SELECT COUNT(*) FROM topics")
        total_topics = cursor.fetchone()[0]
        
        # Completed topics
        cursor.execute("SELECT COUNT(*) FROM topic_status WHERE status = 'completed'")
        completed_topics = cursor.fetchone()[0]
        
        # Failed topics
        cursor.execute("SELECT COUNT(*) FROM topic_status WHERE status = 'failed'")
        failed_topics = cursor.fetchone()[0]
        
        # Success rate
        success_rate = (completed_topics / total_topics * 100) if total_topics > 0 else 0
        
        # Average difficulty (using difficulty field instead of complexity_level)
        cursor.execute("SELECT AVG(difficulty) FROM topics WHERE difficulty IS NOT NULL")
        avg_difficulty = cursor.fetchone()[0] or 0
        
        # Category count
        cursor.execute("SELECT COUNT(DISTINCT category) FROM topics WHERE category IS NOT NULL")
        category_count = cursor.fetchone()[0]
        
        # Company count
        cursor.execute("SELECT COUNT(DISTINCT company) FROM topics WHERE company IS NOT NULL")
        company_count = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total_topics': total_topics,
            'completed_topics': completed_topics,
            'failed_topics': failed_topics,
            'success_rate': round(success_rate, 2),
            'average_difficulty': round(avg_difficulty, 2),
            'category_count': category_count,
            'company_count': company_count
        }
    
    def get_topic_by_title(self, title: str) -> Optional[Dict[str, Any]]:
        """Get a topic by title with its status."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Check schema first
            cursor.execute("PRAGMA table_info(topic_status)")
            columns = {row[1] for row in cursor.fetchall()}
            
            # Get topic with status
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
                col_names = [description[0] for description in cursor.description]
                return dict(zip(col_names, row))
            return None
                
        except Exception as e:
            print(f"Error getting topic by title: {e}")
            return None
        finally:
            conn.close()
    
    def get_topic_by_id(self, topic_id: int) -> Optional[Dict[str, Any]]:
        """Get a topic by ID."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT * FROM topics WHERE id = ?", (topic_id,))
            row = cursor.fetchone()
            
            if row:
                columns = [description[0] for description in cursor.description]
                topic_dict = dict(zip(columns, row))
                
                # Parse JSON fields
                json_fields = ['technologies', 'tags', 'related_topics', 'metrics', 
                              'implementation_details', 'learning_objectives', 'prerequisites']
                for field in json_fields:
                    if field in topic_dict and topic_dict[field]:
                        try:
                            topic_dict[field] = json.loads(topic_dict[field])
                        except (json.JSONDecodeError, TypeError):
                            topic_dict[field] = []
                
                return topic_dict
            return None
                
        except Exception as e:
            print(f"Error getting topic by ID: {e}")
            return None
        finally:
            conn.close()
    
    def delete_topic(self, topic_id: int) -> bool:
        """Delete a topic by ID."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Check if topic exists
            cursor.execute("SELECT id FROM topics WHERE id = ?", (topic_id,))
            if not cursor.fetchone():
                return False
            
            # Delete from all related tables
            cursor.execute("DELETE FROM topics WHERE id = ?", (topic_id,))
            cursor.execute("DELETE FROM topic_status WHERE title IN (SELECT title FROM topics WHERE id = ?)", (topic_id,))
            
            conn.commit()
            return True
                
        except Exception as e:
            print(f"Error deleting topic {topic_id}: {e}")
            return False
        finally:
            conn.close()
    
    def get_topics_stats(self) -> Dict[str, Any]:
        """Get comprehensive topic statistics."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Total topics
            cursor.execute("SELECT COUNT(*) FROM topics")
            total_topics = cursor.fetchone()[0]
            
            # Status breakdown
            cursor.execute("""
                SELECT 
                    COALESCE(ts.status, 'completed') as status,
                    COUNT(*) as count
                FROM topics t
                LEFT JOIN topic_status ts ON t.title = ts.title
                GROUP BY COALESCE(ts.status, 'completed')
            """)
            status_breakdown = dict(cursor.fetchall())
            
            # Category breakdown
            cursor.execute("""
                SELECT category, COUNT(*) 
                FROM topics 
                WHERE category IS NOT NULL AND category != ''
                GROUP BY category 
                ORDER BY COUNT(*) DESC
            """)
            category_breakdown = dict(cursor.fetchall())
            
            # Complexity breakdown
            cursor.execute("""
                SELECT complexity_level, COUNT(*) 
                FROM topics 
                WHERE complexity_level IS NOT NULL AND complexity_level != ''
                GROUP BY complexity_level 
                ORDER BY COUNT(*) DESC
            """)
            complexity_breakdown = dict(cursor.fetchall())
            
            # Company breakdown
            cursor.execute("""
                SELECT company, COUNT(*) 
                FROM topics 
                WHERE company IS NOT NULL AND company != ''
                GROUP BY company 
                ORDER BY COUNT(*) DESC
                LIMIT 10
            """)
            company_breakdown = dict(cursor.fetchall())
            
            # Average difficulty
            cursor.execute("SELECT AVG(difficulty) FROM topics WHERE difficulty IS NOT NULL")
            avg_difficulty = cursor.fetchone()[0] or 0
            
            # Daily stats (last 7 days)
            cursor.execute("""
                SELECT DATE(generated_at) as date, COUNT(*) as count
                FROM topics
                WHERE generated_at >= datetime('now', '-7 days')
                GROUP BY DATE(generated_at)
                ORDER BY date DESC
            """)
            daily_stats = [{'date': row[0], 'count': row[1]} for row in cursor.fetchall()]
            
            return {
                'total_topics': total_topics,
                'status_breakdown': status_breakdown,
                'category_breakdown': category_breakdown,
                'complexity_breakdown': complexity_breakdown,
                'company_breakdown': company_breakdown,
                'average_difficulty': round(avg_difficulty, 2),
                'daily_stats': daily_stats
            }
                
        except Exception as e:
            print(f"Error getting topic stats: {e}")
            return {
                'total_topics': 0,
                'status_breakdown': {},
                'category_breakdown': {},
                'complexity_breakdown': {},
                'company_breakdown': {},
                'average_difficulty': 0,
                'daily_stats': []
            }
        finally:
            conn.close()
    
    # ===== CONTENT GENERATION (from FastAPI backend) =====
    
    async def create_job(self, job_id: str, topic_id: str, topic_name: str, status: str):
        """Create a new content generation job."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO jobs (id, topic_id, topic_name, status)
            VALUES (?, ?, ?, ?)
        """, (job_id, topic_id, topic_name, status))
        
        conn.commit()
        conn.close()
    
    async def update_job_status(self, job_id: str, status: str):
        """Update job status."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE jobs SET status = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (status, job_id))
        
        conn.commit()
        conn.close()
    
    async def create_task(self, task_id: str, job_id: str, platform: str, format: str, status: str):
        """Create a new task."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO tasks (id, job_id, platform, format, status)
            VALUES (?, ?, ?, ?, ?)
        """, (task_id, job_id, platform, format, status))
        
        conn.commit()
        conn.close()
    
    async def update_task_status(self, task_id: str, status: str, result: str = None, error: str = None):
        """Update task status."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE tasks SET status = ?, result = ?, error = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (status, result, error, task_id))
        
        conn.commit()
        conn.close()
    
    async def save_result(self, result_id: str, job_id: str, platform: str, format: str, content: str):
        """Save content generation result."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO results (id, job_id, platform, format, content)
            VALUES (?, ?, ?, ?, ?)
        """, (result_id, job_id, platform, format, content))
        
        conn.commit()
        conn.close()
    
    async def save_prompt(self, prompt_id: str, job_id: str, platform: str, format: str, prompt_text: str):
        """Save prompt used for generation."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO prompts (id, job_id, platform, format, prompt_text)
            VALUES (?, ?, ?, ?, ?)
        """, (prompt_id, job_id, platform, format, prompt_text))
        
        conn.commit()
        conn.close()
    
    async def get_job_status(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Get job status and progress."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM jobs WHERE id = ?", (job_id,))
        job_row = cursor.fetchone()
        
        if not job_row:
            conn.close()
            return None
        
        # Get task counts
        cursor.execute("SELECT COUNT(*) FROM tasks WHERE job_id = ?", (job_id,))
        total_tasks = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM tasks WHERE job_id = ? AND status = 'completed'", (job_id,))
        completed_tasks = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'jobId': job_id,
            'status': job_row[3],  # status column
            'progress': {
                'total': total_tasks,
                'done': completed_tasks
            }
        }

    async def update_job_status(self, job_id: str, status: str):
        """Update job status."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE jobs SET status = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (status, job_id))
        
        conn.commit()
        conn.close()

    async def create_task(self, task_id: str, job_id: str, platform: str, format: str, status: str):
        """Create a new task."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO tasks (id, job_id, platform, format, status)
            VALUES (?, ?, ?, ?, ?)
        """, (task_id, job_id, platform, format, status))
        
        conn.commit()
        conn.close()

    async def update_task_status(self, task_id: str, status: str, result: str = None, error: str = None):
        """Update task status."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE tasks SET status = ?, result = ?, error = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (status, result, error, task_id))
        
        conn.commit()
        conn.close()

    async def save_result(self, result_id: str, job_id: str, platform: str, format: str, content: str):
        """Save content generation result."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO results (id, job_id, platform, format, content)
            VALUES (?, ?, ?, ?, ?)
        """, (result_id, job_id, platform, format, content))
        
        conn.commit()
        conn.close()

    async def save_prompt(self, prompt_id: str, job_id: str, platform: str, format: str, prompt_text: str):
        """Save prompt used for generation."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO prompts (id, job_id, platform, format, prompt_text)
            VALUES (?, ?, ?, ?, ?)
        """, (prompt_id, job_id, platform, format, prompt_text))
        
        conn.commit()
        conn.close()

    async def get_job_status(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Get job status and progress."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM jobs WHERE id = ?", (job_id,))
        job_row = cursor.fetchone()
        
        if not job_row:
            conn.close()
            return None
        
        # Get task counts
        cursor.execute("SELECT COUNT(*) FROM tasks WHERE job_id = ?", (job_id,))
        total_tasks = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM tasks WHERE job_id = ? AND status = 'completed'", (job_id,))
        completed_tasks = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'jobId': job_id,
            'status': job_row[3],  # status column
            'progress': {
                'total': total_tasks,
                'done': completed_tasks
            }
        }

    async def get_job_results(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Get job results."""
        conn = self.get_connection()
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
                    content = json.loads(row[4])  # content column
                    results.append({
                        'platform': row[2],  # platform
                        'format': row[3],    # format
                        'envelope': {
                            'content': content
                        }
                    })
                except json.JSONDecodeError:
                    continue
            
            return {
                'jobId': job_id,
                'status': job_row[3],  # status column
                'results': results
            }
        
        finally:
            conn.close()
        
        return {
            'jobId': job_id,
            'status': 'error',
            'results': [],
            'errors': []
        }

    async def get_results_by_topic(self, topic_id: str) -> List[Dict[str, Any]]:
        """Get all job results for a specific topic."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Get all jobs for this topic
            cursor.execute("SELECT id FROM jobs WHERE topic_id = ?", (topic_id,))
            job_rows = cursor.fetchall()
            
            all_results = []
            for job_row in job_rows:
                job_id = job_row[0]
                
                # Get results for this job
                cursor.execute("SELECT * FROM results WHERE job_id = ?", (job_id,))
                result_rows = cursor.fetchall()
                
                for row in result_rows:
                    try:
                        content = json.loads(row[4])  # content column
                        all_results.append({
                            'job_id': job_id,
                            'platform': row[2],  # platform
                            'format': row[3],    # format
                            'topic_id': int(topic_id),
                            'envelope': {
                                'content': content
                            }
                        })
                    except (json.JSONDecodeError, ValueError):
                        continue
            
            return all_results
        
        finally:
            conn.close()

    def get_cache(self, key: str) -> Optional[Dict[str, Any]]:
        """Get cached content."""
        cache_path = self.get_cache_path(key)
        if cache_path.exists():
            try:
                with open(cache_path, 'r') as f:
                    return json.load(f)
            except Exception:
                return None
        return None
    
    def set_cache(self, key: str, content: Dict[str, Any]):
        """Cache content."""
        cache_path = self.get_cache_path(key)
        try:
            with open(cache_path, 'w') as f:
                json.dump(content, f, indent=2)
        except Exception as e:
            print(f"Error caching content: {e}")
    
    def generate_cache_key(self, topic_title: str, platform: str, format: str, prompt_version: str = "v1") -> str:
        """Generate cache key for content."""
        content = f"{topic_title}|{platform}|{format}|{prompt_version}"
        return hashlib.sha256(content.encode()).hexdigest()
    
    def get_topics_by_status(self, status: str, limit: int = None) -> List[Dict[str, Any]]:
        """Get topics by their processing status with topic_status_id."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Check schema
            cursor.execute("PRAGMA table_info(topic_status)")
            columns = {row[1] for row in cursor.fetchall()}
            
            if 'original_title' in columns:
                # New schema with original_title/current_title
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
                # Old schema with just title
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
                if 'original_title' in columns:
                    topic_dict = {
                        'topic_status_id': row[0],
                        'title': row[1] or row[2],  # Use original_title or current_title
                        'original_title': row[1],
                        'current_title': row[2],
                        'status': row[3],
                        'error_message': row[4],
                        'created_at': row[5],
                        'updated_at': row[6],
                        'id': row[7]  # topic_id from topics table (may be None)
                    }
                else:
                    topic_dict = {
                        'topic_status_id': row[0],
                        'title': row[1],
                        'status': row[2],
                        'error_message': row[3],
                        'created_at': row[4],
                        'updated_at': row[5],
                        'id': row[6]  # topic_id from topics table (may be None)
                    }
                
                # If topic doesn't have an ID yet (not fully processed), assign a temporary one
                if not topic_dict.get('id'):
                    # Get next available ID
                    topic_dict['id'] = self.get_next_available_id() + len(topics)
                
                topics.append(topic_dict)
            
            return topics
        except Exception as e:
            print(f"Error getting topics by status: {e}")
            return []
        finally:
            conn.close()
    
    def get_all_topic_ids(self) -> List[int]:
        """Get all topic IDs from the database."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT id FROM topics ORDER BY id")
            rows = cursor.fetchall()
            return [row[0] for row in rows]
        except Exception as e:
            print(f"Error getting all topic IDs: {e}")
            return []
        finally:
            conn.close()
    
    def get_pending_topics_count(self) -> int:
        """Get count of pending topics."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT COUNT(*) FROM topic_status WHERE status = 'pending'")
            return cursor.fetchone()[0]
        except Exception as e:
            print(f"Error getting pending topics count: {e}")
            return 0
        finally:
            conn.close()
    
    def get_processing_summary(self) -> Dict[str, Any]:
        """Get summary of processing status across all topics."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
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
                if row[0] in summary:
                    summary[row[0]] = row[1]
            
            # Get recent failed topics with details
            # Check schema first
            cursor.execute("PRAGMA table_info(topic_status)")
            columns = {row[1] for row in cursor.fetchall()}
            
            if 'original_title' in columns:
                cursor.execute("""
                    SELECT COALESCE(original_title, current_title), error_message, created_at
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
                failed_topics.append({
                    'title': row[0],
                    'error_message': row[1],
                    'created_at': row[2]
                })
            
            summary['recent_failures'] = failed_topics
            summary['total'] = sum(summary[k] for k in ['pending', 'processing', 'completed', 'failed'])
            
            return summary
        except Exception as e:
            print(f"Error getting processing summary: {e}")
            return {
                'pending': 0,
                'processing': 0,
                'completed': 0,
                'failed': 0,
                'recent_failures': [],
                'total': 0
            }
        finally:
            conn.close()


# Global instance for easy access
unified_db = UnifiedDatabase()
