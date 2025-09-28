#!/usr/bin/env python3
"""
SQLite database manager for storing system design topics.
"""

import sqlite3
import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path


class TopicsDatabase:
    """SQLite database manager for system design topics."""
    
    def __init__(self, db_path: str = None):
        """Initialize the database manager.
        
        Args:
            db_path: Path to SQLite database file
        """
        if db_path is None:
            try:
                from config import DATABASE_PATH
                db_path = DATABASE_PATH
            except ImportError:
                db_path = "topics.db"
        
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database with required tables."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Create topics table
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
                    UNIQUE(id)
                )
            """)
            
            # Create processing_log table for tracking
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS processing_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    batch_id TEXT NOT NULL,
                    topic_id INTEGER NOT NULL,
                    status TEXT NOT NULL,  -- 'success', 'failed', 'skipped'
                    error_message TEXT,
                    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (topic_id) REFERENCES topics (id)
                )
            """)
            
            # Create indexes for better performance
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_topics_category ON topics(category)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_topics_company ON topics(company)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_topics_complexity ON topics(complexity_level)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_topics_difficulty ON topics(difficulty)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_processing_log_batch ON processing_log(batch_id)")
            
            conn.commit()
    
    def save_topic(self, topic: Dict[str, Any], batch_id: str = None) -> bool:
        """Save a single topic to the database.
        
        Args:
            topic: Topic dictionary to save
            batch_id: Optional batch identifier for tracking
            
        Returns:
            True if saved successfully, False otherwise
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Prepare data for insertion
                topic_data = (
                    topic['id'],
                    topic['title'],
                    topic['description'],
                    topic['category'],
                    topic['subcategory'],
                    topic['company'],
                    json.dumps(topic['technologies']),
                    topic['complexity_level'],
                    json.dumps(topic['tags']),
                    json.dumps(topic['related_topics']),
                    json.dumps(topic['metrics']),
                    json.dumps(topic['implementation_details']),
                    json.dumps(topic['learning_objectives']),
                    topic['difficulty'],
                    topic['estimated_read_time'],
                    json.dumps(topic['prerequisites']),
                    topic['created_date'],
                    topic['updated_date']
                )
                
                # Insert or replace topic
                cursor.execute("""
                    INSERT OR REPLACE INTO topics (
                        id, title, description, category, subcategory, company,
                        technologies, complexity_level, tags, related_topics,
                        metrics, implementation_details, learning_objectives,
                        difficulty, estimated_read_time, prerequisites,
                        created_date, updated_date
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, topic_data)
                
                # Log the processing
                if batch_id:
                    cursor.execute("""
                        INSERT INTO processing_log (batch_id, topic_id, status)
                        VALUES (?, ?, 'success')
                    """, (batch_id, topic['id']))
                
                conn.commit()
                return True
                
        except Exception as e:
            # Log the error
            if batch_id:
                try:
                    with sqlite3.connect(self.db_path) as conn:
                        cursor = conn.cursor()
                        cursor.execute("""
                            INSERT INTO processing_log (batch_id, topic_id, status, error_message)
                            VALUES (?, ?, 'failed', ?)
                        """, (batch_id, topic.get('id', 0), str(e)))
                        conn.commit()
                except:
                    pass  # If we can't even log the error, just continue
            
            print(f"Error saving topic {topic.get('id', 'unknown')}: {e}")
            return False
    
    def save_topics_batch(self, topics: List[Dict[str, Any]], batch_id: str = None) -> Dict[str, int]:
        """Save multiple topics to the database.
        
        Args:
            topics: List of topic dictionaries
            batch_id: Optional batch identifier for tracking
            
        Returns:
            Dictionary with success/failure counts
        """
        if not batch_id:
            batch_id = f"batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        results = {'success': 0, 'failed': 0, 'skipped': 0}
        
        for topic in topics:
            if self.save_topic(topic, batch_id):
                results['success'] += 1
            else:
                results['failed'] += 1
        
        return results
    
    def get_topic(self, topic_id: int) -> Optional[Dict[str, Any]]:
        """Retrieve a single topic by ID.
        
        Args:
            topic_id: ID of the topic to retrieve
            
        Returns:
            Topic dictionary or None if not found
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM topics WHERE id = ?", (topic_id,))
                row = cursor.fetchone()
                
                if row:
                    return self._row_to_topic_dict(row)
                return None
                
        except Exception as e:
            print(f"Error retrieving topic {topic_id}: {e}")
            return None
    
    def delete_topic(self, topic_id: int) -> bool:
        """Delete a topic by ID.
        
        Args:
            topic_id: ID of the topic to delete
            
        Returns:
            True if deleted successfully, False if not found
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Check if topic exists
                cursor.execute("SELECT id FROM topics WHERE id = ?", (topic_id,))
                if not cursor.fetchone():
                    return False
                
                # Delete from all related tables
                cursor.execute("DELETE FROM topics WHERE id = ?", (topic_id,))
                cursor.execute("DELETE FROM processing_log WHERE topic_id = ?", (topic_id,))
                cursor.execute("DELETE FROM topic_status WHERE id = ?", (topic_id,))
                
                conn.commit()
                return True
                
        except Exception as e:
            print(f"Error deleting topic {topic_id}: {e}")
            return False
    
    def get_topics_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Retrieve topics by category.
        
        Args:
            category: Category to filter by
            
        Returns:
            List of topic dictionaries
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM topics WHERE category = ? ORDER BY id", (category,))
                rows = cursor.fetchall()
                
                return [self._row_to_topic_dict(row) for row in rows]
                
        except Exception as e:
            print(f"Error retrieving topics by category {category}: {e}")
            return []
    
    def get_all_topics(self, limit: int = None) -> List[Dict[str, Any]]:
        """Retrieve all topics.
        
        Args:
            limit: Optional limit on number of topics
            
        Returns:
            List of topic dictionaries
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                query = "SELECT * FROM topics ORDER BY id"
                if limit:
                    query += f" LIMIT {limit}"
                
                cursor.execute(query)
                rows = cursor.fetchall()
                
                return [self._row_to_topic_dict(row) for row in rows]
                
        except Exception as e:
            print(f"Error retrieving all topics: {e}")
            return []
    
    def get_topics_stats(self) -> Dict[str, Any]:
        """Get statistics about stored topics.
        
        Returns:
            Dictionary with various statistics
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Total topics
                cursor.execute("SELECT COUNT(*) FROM topics")
                total_topics = cursor.fetchone()[0]
                
                # Topics by category
                cursor.execute("""
                    SELECT category, COUNT(*) 
                    FROM topics 
                    GROUP BY category 
                    ORDER BY COUNT(*) DESC
                """)
                by_category = dict(cursor.fetchall())
                
                # Topics by complexity
                cursor.execute("""
                    SELECT complexity_level, COUNT(*) 
                    FROM topics 
                    GROUP BY complexity_level 
                    ORDER BY COUNT(*) DESC
                """)
                by_complexity = dict(cursor.fetchall())
                
                # Recent processing
                cursor.execute("""
                    SELECT COUNT(*) 
                    FROM processing_log 
                    WHERE processed_at >= datetime('now', '-24 hours')
                """)
                recent_processing = cursor.fetchone()[0]
                
                return {
                    'total_topics': total_topics,
                    'by_category': by_category,
                    'by_complexity': by_complexity,
                    'recent_processing_24h': recent_processing
                }
                
        except Exception as e:
            print(f"Error getting stats: {e}")
            return {}
    
    def _row_to_topic_dict(self, row) -> Dict[str, Any]:
        """Convert database row to topic dictionary."""
        return {
            'id': row[0],
            'title': row[1],
            'description': row[2],
            'category': row[3],
            'subcategory': row[4],
            'company': row[5],
            'technologies': json.loads(row[6]),
            'complexity_level': row[7],
            'tags': json.loads(row[8]),
            'related_topics': json.loads(row[9]),
            'metrics': json.loads(row[10]),
            'implementation_details': json.loads(row[11]),
            'learning_objectives': json.loads(row[12]),
            'difficulty': row[13],
            'estimated_read_time': row[14],
            'prerequisites': json.loads(row[15]),
            'created_date': row[16],
            'updated_date': row[17],
            'generated_at': row[18]
        }
    
    def export_to_json(self, output_file: str = None) -> str:
        """Export all topics to a JSON file.
        
        Args:
            output_file: Output file path (defaults to topics_export.json)
            
        Returns:
            Path to the exported file
        """
        if not output_file:
            output_file = f"topics_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        topics = self.get_all_topics()
        
        with open(output_file, 'w') as f:
            json.dump(topics, f, indent=2)
        
        return output_file
    
    def save_topic_status(self, topic_id: int, title: str, status: str, error_message: str = None) -> bool:
        """Save topic processing status.
        
        Args:
            topic_id: Topic ID
            title: Topic title
            status: Processing status (pending, completed, failed)
            error_message: Error message if failed
            
        Returns:
            True if saved successfully
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Create topic_status table if it doesn't exist
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS topic_status (
                        id INTEGER PRIMARY KEY,
                        title TEXT NOT NULL,
                        status TEXT NOT NULL,
                        error_message TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Insert or update status
                cursor.execute("""
                    INSERT OR REPLACE INTO topic_status (id, title, status, error_message, updated_at)
                    VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
                """, (topic_id, title, status, error_message))
                
                conn.commit()
                return True
                
        except Exception as e:
            print(f"Error saving topic status: {e}")
            return False
    
    def get_topic_status(self, topic_id: int) -> Optional[Dict[str, Any]]:
        """Get topic processing status.
        
        Args:
            topic_id: Topic ID
            
        Returns:
            Status dictionary or None
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM topic_status WHERE id = ?", (topic_id,))
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
            print(f"Error getting topic status: {e}")
            return None
    
    def get_topics_paginated(self, offset: int = 0, limit: int = 20, 
                            search: str = '', category: str = '', status: str = '', 
                            complexity: str = '', company: str = '', 
                            sort_by: str = 'created_date', sort_order: str = 'desc') -> List[Dict[str, Any]]:
        """Get topics with pagination, search, and filtering.
        
        Args:
            offset: Number of topics to skip
            limit: Maximum number of topics to return
            search: Search term for title
            category: Filter by category
            status: Filter by processing status
            complexity: Filter by complexity level
            company: Filter by company
            sort_by: Field to sort by (created_date, title, difficulty, company)
            sort_order: Sort order (asc, desc)
            
        Returns:
            List of topic dictionaries
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Build WHERE clause
                where_conditions = []
                params = []
                
                if search:
                    where_conditions.append("t.title LIKE ?")
                    params.append(f"%{search}%")
                
                if category:
                    where_conditions.append("t.category = ?")
                    params.append(category)
                
                if complexity:
                    where_conditions.append("t.complexity_level = ?")
                    params.append(complexity)
                
                if company:
                    where_conditions.append("t.company = ?")
                    params.append(company)
                
                if status:
                    if status == 'completed':
                        where_conditions.append("(ts.status = 'completed' OR ts.status IS NULL)")
                    elif status == 'pending':
                        where_conditions.append("ts.status = 'pending'")
                    elif status == 'failed':
                        where_conditions.append("ts.status = 'failed'")
                
                where_clause = ""
                if where_conditions:
                    where_clause = "WHERE " + " AND ".join(where_conditions)
                
                # Build ORDER BY clause
                valid_sort_fields = {
                    'created_date': 't.created_date',
                    'title': 't.title',
                    'difficulty': 't.difficulty',
                    'company': 't.company'
                }
                sort_field = valid_sort_fields.get(sort_by, 't.created_date')
                sort_direction = 'ASC' if sort_order.lower() == 'asc' else 'DESC'
                
                query = f"""
                    SELECT t.*, ts.status as processing_status, ts.error_message
                    FROM topics t
                    LEFT JOIN topic_status ts ON t.id = ts.id
                    {where_clause}
                    ORDER BY {sort_field} {sort_direction}
                    LIMIT ? OFFSET ?
                """
                
                params.extend([limit, offset])
                cursor.execute(query, params)
                rows = cursor.fetchall()
                
                topics = []
                for row in rows:
                    topic = self._row_to_topic_dict(row[:19])  # First 19 columns are topic data
                    topic['processing_status'] = row[19] if row[19] else 'completed'
                    topic['error_message'] = row[20] if row[20] else None
                    topics.append(topic)
                
                return topics
                
        except Exception as e:
            print(f"Error getting paginated topics: {e}")
            return []
    
    def get_total_topics_count(self) -> int:
        """Get total number of topics."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM topics")
                return cursor.fetchone()[0]
        except Exception as e:
            print(f"Error getting total topics count: {e}")
            return 0
    
    def get_topics_count(self, search: str = '', category: str = '', status: str = '', 
                        complexity: str = '', company: str = '') -> int:
        """Get count of topics with search and filtering.
        
        Args:
            search: Search term for title
            category: Filter by category
            status: Filter by processing status
            complexity: Filter by complexity level
            company: Filter by company
            
        Returns:
            Count of matching topics
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Build WHERE clause (same logic as get_topics_paginated)
                where_conditions = []
                params = []
                
                if search:
                    where_conditions.append("t.title LIKE ?")
                    params.append(f"%{search}%")
                
                if category:
                    where_conditions.append("t.category = ?")
                    params.append(category)
                
                if complexity:
                    where_conditions.append("t.complexity_level = ?")
                    params.append(complexity)
                
                if company:
                    where_conditions.append("t.company = ?")
                    params.append(company)
                
                if status:
                    if status == 'completed':
                        where_conditions.append("(ts.status = 'completed' OR ts.status IS NULL)")
                    elif status == 'pending':
                        where_conditions.append("ts.status = 'pending'")
                    elif status == 'failed':
                        where_conditions.append("ts.status = 'failed'")
                
                where_clause = ""
                if where_conditions:
                    where_clause = "WHERE " + " AND ".join(where_conditions)
                
                query = f"""
                    SELECT COUNT(*)
                    FROM topics t
                    LEFT JOIN topic_status ts ON t.id = ts.id
                    {where_clause}
                """
                
                cursor.execute(query, params)
                return cursor.fetchone()[0]
        except Exception as e:
            print(f"Error getting topics count: {e}")
            return 0
    
    def topic_exists_and_completed(self, title: str) -> bool:
        """Check if a topic with the given title already exists and is completed.
        
        Args:
            title: Topic title to check
            
        Returns:
            True if topic exists and is completed, False otherwise
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Check if topic exists in topics table AND has completed status
                cursor.execute("""
                    SELECT t.id, ts.status 
                    FROM topics t
                    LEFT JOIN topic_status ts ON t.id = ts.id
                    WHERE t.title = ?
                """, (title.strip(),))
                
                result = cursor.fetchone()
                
                if not result:
                    return False
                
                topic_id, status = result
                
                # Only return True if status is explicitly 'completed'
                # If status is None, 'pending', or 'failed', return False
                return status == 'completed'
                
        except Exception as e:
            print(f"Error checking topic existence: {e}")
            return False
    
    def get_existing_topic_by_title(self, title: str) -> Optional[Dict[str, Any]]:
        """Get an existing topic by title.
        
        Args:
            title: Topic title to search for
            
        Returns:
            Topic dictionary if found, None otherwise
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM topics WHERE title = ?", (title.strip(),))
                row = cursor.fetchone()
                
                if row:
                    return self._row_to_topic_dict(row)
                return None
                
        except Exception as e:
            print(f"Error getting topic by title: {e}")
            return None
    
    def cleanup_failed_topics(self) -> int:
        """Remove failed topics from the database to allow retry.
        
        Returns:
            Number of failed topics removed
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Get all failed topic IDs
                cursor.execute("SELECT id FROM topic_status WHERE status = 'failed'")
                failed_ids = [row[0] for row in cursor.fetchall()]
                
                if not failed_ids:
                    return 0
                
                # Remove from topics table
                placeholders = ','.join(['?' for _ in failed_ids])
                cursor.execute(f"DELETE FROM topics WHERE id IN ({placeholders})", failed_ids)
                
                # Remove from topic_status table
                cursor.execute(f"DELETE FROM topic_status WHERE id IN ({placeholders})", failed_ids)
                
                # Remove from processing_log table
                cursor.execute(f"DELETE FROM processing_log WHERE topic_id IN ({placeholders})", failed_ids)
                
                conn.commit()
                
                print(f"Cleaned up {len(failed_ids)} failed topics")
                return len(failed_ids)
                
        except Exception as e:
            print(f"Error cleaning up failed topics: {e}")
            return 0
    
    def get_topic_status_summary(self) -> Dict[str, int]:
        """Get a summary of topic statuses.
        
        Returns:
            Dictionary with status counts
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Get status counts
                cursor.execute("""
                    SELECT 
                        COALESCE(ts.status, 'no_status') as status,
                        COUNT(*) as count
                    FROM topics t
                    LEFT JOIN topic_status ts ON t.id = ts.id
                    GROUP BY COALESCE(ts.status, 'no_status')
                """)
                
                results = cursor.fetchall()
                return {status: count for status, count in results}
                
        except Exception as e:
            print(f"Error getting topic status summary: {e}")
            return {}
    
    def get_next_available_id(self) -> int:
        """Get the next available ID for new topics.
        
        Returns:
            Next available ID
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Get the maximum ID from topics table
                cursor.execute("SELECT COALESCE(MAX(id), 0) FROM topics")
                max_id = cursor.fetchone()[0]
                
                # Return next available ID (max + 1)
                return max_id + 1
                
        except Exception as e:
            print(f"Error getting next available ID: {e}")
            return 1000  # Fallback to 1000 if error
    
    def topic_exists(self, title: str) -> bool:
        """Check if a topic with the given title already exists (regardless of status).
        
        Args:
            title: Topic title to check
            
        Returns:
            True if topic exists, False otherwise
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id FROM topics WHERE title = ?", (title.strip(),))
                return cursor.fetchone() is not None
                
        except Exception as e:
            print(f"Error checking topic existence: {e}")
            return False
    
    def get_topic_by_title(self, title: str) -> Optional[Dict[str, Any]]:
        """Get a topic by title with its status.
        
        Args:
            title: Topic title to search for
            
        Returns:
            Dictionary with topic data and status, or None if not found
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Get topic with status
                cursor.execute("""
                    SELECT t.*, ts.status, ts.error_message, ts.created_at
                    FROM topics t
                    LEFT JOIN topic_status ts ON t.id = ts.id
                    WHERE t.title = ?
                """, (title.strip(),))
                
                row = cursor.fetchone()
                if row:
                    columns = [description[0] for description in cursor.description]
                    return dict(zip(columns, row))
                return None
                
        except Exception as e:
            print(f"Error getting topic by title: {e}")
            return None

    def get_detailed_stats(self) -> Dict[str, Any]:
        """Get detailed statistics for analytics."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Basic stats
                cursor.execute("SELECT COUNT(*) FROM topics")
                total_topics = cursor.fetchone()[0]
                
                # Status breakdown
                cursor.execute("""
                    SELECT 
                        COALESCE(ts.status, 'completed') as status,
                        COUNT(*) as count
                    FROM topics t
                    LEFT JOIN topic_status ts ON t.id = ts.id
                    GROUP BY COALESCE(ts.status, 'completed')
                """)
                status_breakdown = dict(cursor.fetchall())
                
                # Category breakdown
                cursor.execute("""
                    SELECT category, COUNT(*) 
                    FROM topics 
                    GROUP BY category 
                    ORDER BY COUNT(*) DESC
                """)
                category_breakdown = dict(cursor.fetchall())
                
                # Complexity breakdown
                cursor.execute("""
                    SELECT complexity_level, COUNT(*) 
                    FROM topics 
                    GROUP BY complexity_level 
                    ORDER BY COUNT(*) DESC
                """)
                complexity_breakdown = dict(cursor.fetchall())
                
                # Daily processing stats
                cursor.execute("""
                    SELECT DATE(generated_at) as date, COUNT(*) as count
                    FROM topics
                    WHERE generated_at >= datetime('now', '-30 days')
                    GROUP BY DATE(generated_at)
                    ORDER BY date DESC
                """)
                daily_stats = cursor.fetchall()
                
                # Company breakdown
                cursor.execute("""
                    SELECT company, COUNT(*) 
                    FROM topics 
                    GROUP BY company 
                    ORDER BY COUNT(*) DESC
                    LIMIT 10
                """)
                company_breakdown = dict(cursor.fetchall())
                
                return {
                    'total_topics': total_topics,
                    'status_breakdown': status_breakdown,
                    'category_breakdown': category_breakdown,
                    'complexity_breakdown': complexity_breakdown,
                    'daily_stats': daily_stats,
                    'company_breakdown': company_breakdown
                }
                
        except Exception as e:
            print(f"Error getting detailed stats: {e}")
            return {}


def main():
    """Example usage of the TopicsDatabase."""
    db = TopicsDatabase()
    
    # Get stats
    stats = db.get_topics_stats()
    print("Database Statistics:")
    print(f"Total topics: {stats.get('total_topics', 0)}")
    print(f"By category: {stats.get('by_category', {})}")
    print(f"By complexity: {stats.get('by_complexity', {})}")
    
    # Export to JSON
    export_file = db.export_to_json()
    print(f"Exported to: {export_file}")


if __name__ == "__main__":
    main()
