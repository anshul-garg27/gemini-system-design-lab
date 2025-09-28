#!/usr/bin/env python3
"""
Test script for content generation workflow debugging.
"""
import asyncio
import json
import logging
from datetime import datetime
from app.service_tasks import get_task_service, get_job_status, get_job_results
from app.schemas import GenerateAllRequest, Audience, Locale
from app.store import Store
from unified_database import unified_db

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

async def test_job_lookup(job_id: str):
    """Test looking up a specific job."""
    print(f"\n🔍 Testing job lookup for: {job_id}")
    
    # Test database connection
    try:
        conn = unified_db.get_connection()
        cursor = conn.cursor()
        
        # Check if job exists
        cursor.execute("SELECT * FROM jobs WHERE id = ?", (job_id,))
        job_row = cursor.fetchone()
        
        if job_row:
            print(f"✅ Job found in database: {job_row}")
            
            # Get tasks for this job
            cursor.execute("SELECT * FROM tasks WHERE job_id = ?", (job_id,))
            task_rows = cursor.fetchall()
            print(f"📋 Found {len(task_rows)} tasks:")
            for task in task_rows:
                print(f"   - Task {task[0]}: {task[2]}/{task[3]} - Status: {task[4]}")
                if len(task) > 7 and task[7]:  # error column
                    print(f"     Error: {task[7]}")
            
            # Get results
            cursor.execute("SELECT * FROM results WHERE job_id = ?", (job_id,))
            result_rows = cursor.fetchall()
            print(f"📊 Found {len(result_rows)} results")
            
        else:
            print(f"❌ Job {job_id} not found in database")
            
        conn.close()
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        
    # Test service layer
    try:
        status = await get_job_status(job_id)
        if status:
            print(f"✅ Service layer status: {status}")
        else:
            print(f"❌ Service layer returned None for job {job_id}")
            
        results = await get_job_results(job_id)
        if results:
            print(f"✅ Service layer results: {results}")
        else:
            print(f"❌ Service layer returned None for results {job_id}")
            
    except Exception as e:
        print(f"❌ Service layer error: {e}")
        import traceback
        traceback.print_exc()

async def test_simple_generation():
    """Test a simple content generation."""
    print("\n🧪 Testing simple content generation...")
    
    # Create a test request
    request = GenerateAllRequest(
        topicId="1",
        topicName="Load Balancer Design",
        topicDescription="Design a distributed load balancer system",
        audience=Audience.INTERMEDIATE,
        tone="technical",
        locale=Locale.EN,
        primaryUrl="https://example.com",
        brand={
            "siteUrl": "https://example.com",
            "handles": {"linkedin": "@example"},
            "utmBase": "utm_source=test"
        },
        targetPlatforms=["instagram:carousel"],
        options={
            "include_images": True,
            "max_length_levels": "standard",
            "force": False,
            "length_hint": 500
        }
    )
    
    # Test task service
    try:
        task_service = get_task_service()
        
        # Test prompt building
        prompt = task_service.build_prompt("instagram", "carousel", request)
        print(f"✅ Generated prompt (first 200 chars): {prompt[:200]}...")
        
        # Test Gemini client
        print("🤖 Testing Gemini API call...")
        try:
            response = await task_service.gemini_client.generate_content(prompt)
            print(f"✅ Gemini response received (first 200 chars): {response[:200]}...")
            
            # Test validation
            validated = task_service.validate_response("instagram", "carousel", response)
            print(f"✅ Response validated: {type(validated)}")
            
        except Exception as e:
            print(f"❌ Gemini API error: {e}")
            
    except Exception as e:
        print(f"❌ Task service error: {e}")
        import traceback
        traceback.print_exc()

async def check_database_schema():
    """Check database schema and tables."""
    print("\n📋 Checking database schema...")
    
    try:
        conn = unified_db.get_connection()
        cursor = conn.cursor()
        
        # Check tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"📊 Found tables: {[t[0] for t in tables]}")
        
        # Check jobs table schema
        cursor.execute("PRAGMA table_info(jobs)")
        jobs_schema = cursor.fetchall()
        print(f"🏗️ Jobs table schema: {jobs_schema}")
        
        # Check tasks table schema
        cursor.execute("PRAGMA table_info(tasks)")
        tasks_schema = cursor.fetchall()
        print(f"🏗️ Tasks table schema: {tasks_schema}")
        
        # Check recent jobs
        cursor.execute("SELECT id, topic_name, status, created_at FROM jobs ORDER BY created_at DESC LIMIT 5")
        recent_jobs = cursor.fetchall()
        print(f"📈 Recent jobs: {recent_jobs}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Schema check error: {e}")

async def main():
    """Main test function."""
    print("🚀 Starting content generation debugging...")
    
    await check_database_schema()
    await test_simple_generation()
    
    # Test the specific failing job if provided
    failing_job_id = "b3eef645-76ee-4fcb-9192-289740e37dd0"
    await test_job_lookup(failing_job_id)
    
    print("\n✅ Debugging complete!")

if __name__ == "__main__":
    asyncio.run(main())
