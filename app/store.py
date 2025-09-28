"""
Database and cache storage utilities.
"""
import sqlite3
import json
import hashlib
import uuid
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime


class Store:
    """Storage manager for jobs, tasks, and cache."""
    
    def __init__(self):
        # Use unified database instead of separate app.db
        from unified_database import unified_db
        self.db = unified_db
        self.cache_dir = Path("./data/cache")
        self.cache_dir.mkdir(exist_ok=True)
    
    def get_topics_paginated(self, limit: int = 50, offset: int = 0):
        """Get topics with pagination."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT id, title, description, category, subcategory, company, 
                       technologies, complexity_level, tags, related_topics, 
                       metrics, implementation_details, learning_objectives, 
                       difficulty, estimated_read_time, prerequisites, 
                       created_date, updated_date, generated_at, source
                FROM topics 
                ORDER BY id DESC 
                LIMIT ? OFFSET ?
            """, (limit, offset))
            
            topics = []
            for row in cursor.fetchall():
                topic = {
                    'id': row[0],
                    'title': row[1],
                    'description': row[2],
                    'category': row[3],
                    'subcategory': row[4],
                    'company': row[5],
                    'technologies': row[6],
                    'complexity_level': row[7],
                    'tags': row[8],
                    'related_topics': row[9],
                    'metrics': row[10],
                    'implementation_details': row[11],
                    'learning_objectives': row[12],
                    'difficulty': row[13],
                    'estimated_read_time': row[14],
                    'prerequisites': row[15],
                    'created_date': row[16],
                    'updated_date': row[17],
                    'generated_at': row[18],
                    'source': row[19]
                }
                topics.append(topic)
            
            # Get total count
            cursor.execute("SELECT COUNT(*) FROM topics")
            total_count = cursor.fetchone()[0]
            
            return {
                'topics': topics,
                'total_count': total_count,
                'limit': limit,
                'offset': offset
            }
        finally:
            conn.close()

    def get_connection(self):
        """Get database connection."""
        return self.db.get_connection()
    
    async def create_job(self, job_id: str, topic_id: str, topic_name: str, status: str):
        """Create a new job."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO jobs (id, topic_id, topic_name, status)
            VALUES (?, ?, ?, ?)
        """, (job_id, topic_id, topic_name, status))
        
        conn.commit()
        conn.close()
    
    async def create_task(
        self, 
        task_id: str, 
        job_id: str, 
        platform: str, 
        format_name: str, 
        status: str
    ):
        """Create a new task."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO tasks (id, job_id, platform, format, status)
            VALUES (?, ?, ?, ?, ?)
        """, (task_id, job_id, platform, format_name, status))
        
        conn.commit()
        conn.close()
    
    async def update_task_status(
        self, 
        task_id: str, 
        status: str, 
        started_at: Optional[datetime] = None,
        finished_at: Optional[datetime] = None,
        error: Optional[str] = None
    ):
        """Update task status."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            update_fields = []
            params = []
            
            if status:
                update_fields.append("status = ?")
                params.append(status)
            
            if started_at:
                update_fields.append("started_at = ?")
                params.append(started_at)
            
            if finished_at:
                update_fields.append("finished_at = ?")
                params.append(finished_at)
            
            if error:
                update_fields.append("error = ?")
                params.append(error)
            
            params.append(task_id)
            
            cursor.execute(f"""
                UPDATE tasks 
                SET {', '.join(update_fields)}
                WHERE id = ?
            """, params)
            
            conn.commit()
        except Exception as e:
            print(f"Error updating task status: {e}")
        finally:
            conn.close()
            
    
    async def save_task_result(self, task_id: str, raw_response: str, normalized_json: str):
        """Save task result."""
        # Get task info first
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT job_id, platform, format FROM tasks WHERE id = ?", (task_id,))
            task_row = cursor.fetchone()
            if task_row:
                job_id, platform, format_name = task_row
                result_id = str(uuid.uuid4())
                await self.db.save_result(result_id, job_id, platform, format_name, normalized_json)
        finally:
            conn.close()
    
    async def update_job_status(self, job_id: str, status: str):
        """Update job status."""
        await self.db.update_job_status(job_id, status)

    async def get_job_status(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Get job status from database."""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT * FROM jobs WHERE id = ?", (job_id,))
            row = cursor.fetchone()
            
            if not row:
                return None
                
            return {
                'id': row[0],
                'topic_id': row[1],
                'topic_name': row[2],
                'status': row[3],
                'created_at': row[4],
                'updated_at': row[5]
            }
        finally:
            conn.close()

    async def get_job_results(self, job_id: str) -> List[Dict[str, Any]]:
        """Get all results for a job."""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT r.*, t.platform, t.format 
                FROM results r
                JOIN tasks t ON r.task_id = t.id
                WHERE t.job_id = ?
            """, (job_id,))
            
            results = []
            for row in cursor.fetchall():
                result = {
                    'id': row[0],
                    'task_id': row[1],
                    'platform': row[6],
                    'format': row[7],
                    'content': row[2],
                    'created_at': row[3],
                    'updated_at': row[4]
                }
                results.append(result)
            
            return results
        finally:
            conn.close()

    async def get_job_tasks(self, job_id: str) -> List[Dict[str, Any]]:
        """Get all tasks for a job."""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM tasks WHERE job_id = ?", (job_id,))
            rows = cursor.fetchall()
            tasks = []
            for row in rows:
                tasks.append({
                    "id": row[0],
                    "job_id": row[1], 
                    "platform": row[2],
                    "format": row[3],
                    "status": row[4],
                    "error": row[7] if len(row) > 7 else None
                })
            return tasks
        finally:
            conn.close()
    
    async def get_task_result(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get task result."""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT raw_response, normalized_json
            FROM results
            WHERE task_id = ?
        """, (task_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                "raw_response": row[0],
                "normalized_json": row[1]
            }
        return None
    
    def generate_cache_key(self, topic_title: str, platform: str, format_name: str, prompt_version: str) -> str:
        """Generate cache key."""
        key_string = f"{topic_title}|{platform}|{format_name}|{prompt_version}"
        return hashlib.sha256(key_string.encode()).hexdigest()
    
    def get_cached_result(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """Get cached result."""
        cache_file = self.cache_dir / f"{cache_key}.json"
        
        if cache_file.exists():
            try:
                with open(cache_file, "r") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return None
        
        return None
    
    def save_cached_result(self, cache_key: str, result: Dict[str, Any]):
        """Save result to cache."""
        cache_file = self.cache_dir / f"{cache_key}.json"
        
        try:
            with open(cache_file, "w") as f:
                json.dump(result, f, indent=2)
        except IOError as e:
            print(f"Failed to save cache: {e}")


# Global store instance
store = Store()


# Public functions for routes
async def create_job(job_id: str, topic_id: str, topic_name: str, status: str):
    """Create a new job."""
    await store.create_job(job_id, topic_id, topic_name, status)


async def create_task(task_id: str, job_id: str, platform: str, format_name: str, status: str):
    """Create a new task."""
    await store.create_task(task_id, job_id, platform, format_name, status)


async def update_task_status(
    task_id: str, 
    status: str, 
    started_at: Optional[datetime] = None,
    finished_at: Optional[datetime] = None,
    error: Optional[str] = None
):
    """Update task status."""
    await store.update_task_status(task_id, status, started_at, finished_at, error)


async def save_task_result(task_id: str, raw_response: str, normalized_json: str):
    """Save task result."""
    await store.save_task_result(task_id, raw_response, normalized_json)


async def get_job_tasks(job_id: str) -> List[Dict[str, Any]]:
    """Get all tasks for a job."""
    return await store.get_job_tasks(job_id)


async def get_task_result(task_id: str) -> Optional[Dict[str, Any]]:
    """Get task result."""
    return await store.get_task_result(task_id)
