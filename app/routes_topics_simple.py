"""
Simplified topic management routes for the unified FastAPI application.
"""
from fastapi import APIRouter, HTTPException, Query, BackgroundTasks
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
import asyncio
import threading
import time
import json
from datetime import datetime

from unified_database import unified_db
from gemini_client import GeminiClient
from batch_processor import TopicBatchProcessor

router = APIRouter()

# Initialize database
db = unified_db

# Global processing status
processing_status = {
    "is_processing": False,
    "current_batch": 0,
    "total_batches": 0,
    "processed_topics": 0,
    "failed_topics": 0,
    "skipped_topics": 0,
    "skipped_titles": [],
    "current_topic": None,
    "errors": []
}

# Pydantic models for request/response
class CreateTopicsRequest(BaseModel):
    topics: List[str]
    batch_size: int = 5


class TopicResponse(BaseModel):
    id: int
    title: str
    description: str
    category: str
    subcategory: str
    company: str
    technologies: List[str]
    complexity_level: str
    tags: List[str]
    related_topics: List[int]
    metrics: Dict[str, str]
    implementation_details: Dict[str, str]
    learning_objectives: List[str]
    difficulty: int
    estimated_read_time: str
    prerequisites: List[str]
    created_date: str
    updated_date: str
    generated_at: str
    source: str


class TopicsResponse(BaseModel):
    topics: List[TopicResponse]
    total_count: int
    limit: int
    offset: int


class ProcessingStatusResponse(BaseModel):
    is_processing: bool
    current_batch: int
    total_batches: int
    processed_topics: int
    failed_topics: int
    skipped_topics: int
    skipped_titles: List[str]
    current_topic: Optional[str]
    errors: List[str]


class StatsResponse(BaseModel):
    total_topics: int
    completed_topics: int
    failed_topics: int
    success_rate: float
    average_difficulty: float
    category_count: int
    company_count: int


# Helper functions
def process_topics_background(topic_titles: List[str], batch_size: int):
    """Process topics in background thread."""
    global processing_status
    
    try:
        # Initialize processing status
        processing_status.update({
            "is_processing": True,
            "current_batch": 0,
            "total_batches": (len(topic_titles) + batch_size - 1) // batch_size,
            "processed_topics": 0,
            "failed_topics": 0,
            "skipped_topics": 0,
            "skipped_titles": [],
            "current_topic": None,
            "errors": []
        })
        
        # Initialize Gemini client with API keys from config
        try:
            from config import API_KEYS
            if not API_KEYS:
                processing_status["is_processing"] = False
                processing_status["errors"].append("No API keys found in config.py")
                return
            gemini_client = GeminiClient(API_KEYS)
        except ImportError:
            # Fall back to environment variable
            import os
            api_key = os.getenv('GOOGLE_AI_API_KEY')
            if not api_key:
                processing_status["is_processing"] = False
                processing_status["errors"].append("No API keys found in config.py or GOOGLE_AI_API_KEY environment variable")
                return
            gemini_client = GeminiClient([api_key])
        
        # Process topics in batches
        for i in range(0, len(topic_titles), batch_size):
            batch = topic_titles[i:i + batch_size]
            batch_num = i // batch_size + 1
            
            processing_status["current_batch"] = batch_num
            processing_status["current_topic"] = batch[0] if batch else None
            
            try:
                # Get all existing topic IDs for cross-linking
                all_topic_ids = db.get_all_topic_ids()
                next_id = db.get_next_available_id()
                
                # Create topic objects for this batch
                batch_topics = []
                for idx, topic_title in enumerate(batch):
                    topic_obj = {
                        'id': next_id + idx,
                        'title': topic_title
                    }
                    batch_topics.append(topic_obj)
                
                # Generate topics using Gemini (batch processing)
                try:
                    result = gemini_client.generate_topics(batch_topics, all_topic_ids)
                    
                    # Handle response (single topic or list)
                    if isinstance(result, dict):
                        generated_topics = [result]
                    elif isinstance(result, list):
                        generated_topics = result
                    else:
                        processing_status["failed_topics"] += len(batch)
                        processing_status["errors"].append(f"Invalid result format for batch: {batch}")
                        continue
                    
                    # Process each generated topic
                    for topic_data in generated_topics:
                        try:
                            # Save to database
                            topic_saved = db.save_topic(topic_data, "fastapi_batch")
                            
                            if topic_saved:
                                # Save topic status as completed
                                db.save_topic_status(topic_data.get('title', ''), 'completed', None)
                                processing_status["processed_topics"] += 1
                            else:
                                db.save_topic_status(topic_data.get('title', ''), 'failed', 'Failed to save to database')
                                processing_status["failed_topics"] += 1
                                processing_status["errors"].append(f"Failed to save topic: {topic_data.get('title', 'Unknown')}")
                        except Exception as save_error:
                            processing_status["failed_topics"] += 1
                            processing_status["errors"].append(f"Error saving topic: {str(save_error)}")
                            
                except Exception as api_error:
                    # Handle batch API error
                    processing_status["failed_topics"] += len(batch)
                    processing_status["errors"].append(f"API error for batch: {str(api_error)}")
                    
                    # Mark all topics in batch as failed
                    for topic_title in batch:
                        db.save_topic_status(topic_title, 'failed', str(api_error))
                
                # Small delay between batches
                time.sleep(1)
                    
            except Exception as e:
                processing_status["failed_topics"] += len(batch)
                processing_status["errors"].append(f"Batch {batch_num} error: {str(e)}")
        
        # Mark processing as complete
        processing_status["is_processing"] = False
        processing_status["current_topic"] = None
        
    except Exception as e:
        processing_status["is_processing"] = False
        processing_status["errors"].append(f"Processing failed: {str(e)}")

# API Endpoints
@router.post("/topics", response_model=Dict[str, Any])
async def create_topics(request: CreateTopicsRequest, background_tasks: BackgroundTasks):
    """Create topics from bulk input."""
    topic_titles = request.topics
    batch_size = request.batch_size
    
    # Validate batch size (per API call)
    if not isinstance(batch_size, int) or batch_size < 1 or batch_size > 5:
        raise HTTPException(status_code=400, detail="Batch size must be between 1 and 5 topics per API call")
    
    if not topic_titles:
        raise HTTPException(status_code=400, detail="No topics provided")
    
    # Check if already processing
    if processing_status["is_processing"]:
        raise HTTPException(status_code=409, detail="Processing already in progress")
    
    # Start background processing
    background_tasks.add_task(process_topics_background, topic_titles, batch_size)
    
    return {
        "message": f"Started processing {len(topic_titles)} topics in batches of {batch_size}",
        "total_topics": len(topic_titles),
        "batch_size": batch_size,
        "estimated_batches": (len(topic_titles) + batch_size - 1) // batch_size
    }


@router.get("/topics", response_model=TopicsResponse)
async def get_topics(
    limit: int = Query(5, ge=1, le=100),
    offset: int = Query(0, ge=0),
    search: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    complexity: Optional[str] = Query(None),
    company: Optional[str] = Query(None),
    sort_by: str = Query("created_date"),
    sort_order: str = Query("desc")
):
    """Get topics with pagination, search, and filtering."""
    try:
        # Get topics with search and filters
        topics = db.get_topics_paginated(
            offset=offset, 
            limit=limit,
            search=search,
            category=category,
            status=status,
            complexity=complexity,
            company=company,
            sort_by=sort_by,
            sort_order=sort_order
        )
        
        # Get total count for pagination (with same filters)
        total_count = db.get_topics_count(
            search=search,
            category=category,
            status=status,
            complexity=complexity,
            company=company
        )
        
        return TopicsResponse(
            topics=topics,
            total_count=total_count,
            limit=limit,
            offset=offset
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status", response_model=ProcessingStatusResponse)
async def get_status():
    """Get current processing status."""
    return ProcessingStatusResponse(**processing_status)


@router.get("/topics/{topic_id}", response_model=TopicResponse)
async def get_topic(topic_id: int):
    """Get a specific topic."""
    try:
        topic = db.get_topic_by_id(topic_id)
        if not topic:
            raise HTTPException(status_code=404, detail="Topic not found")
        return TopicResponse(**topic)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/topics/{topic_id}")
async def delete_topic(topic_id: int):
    """Delete a topic."""
    try:
        # Delete from database
        success = db.delete_topic(topic_id)
        if success:
            return {"message": "Topic deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Topic not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/topics/{topic_id}/retry")
async def retry_topic(topic_id: int):
    """Retry processing a failed topic."""
    return {"message": "Topic retry not yet implemented"}


@router.get("/stats", response_model=StatsResponse)
async def get_stats():
    """Get database statistics."""
    try:
        stats = db.get_stats()
        return StatsResponse(**stats)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/cleanup-failed")
async def cleanup_failed_topics():
    """Clean up failed topics from the database."""
    try:
        cleaned_count = db.cleanup_failed_topics()
        return {
            "success": True,
            "message": f"Cleaned up {cleaned_count} failed topics",
            "cleaned_count": cleaned_count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/topic-status-summary")
async def get_topic_status_summary():
    """Get a summary of topic statuses."""
    try:
        summary = db.get_topic_status_summary()
        return {
            "success": True,
            "summary": summary
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
