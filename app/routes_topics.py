"""
Topic management routes for the unified FastAPI application.
Migrated from Flask app to provide topic generation and management functionality.
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks, Query
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
import threading
import time
import json
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
import copy
import os
import re

from unified_database import UnifiedDatabase
from gemini_client import GeminiClient
from batch_processor import TopicBatchProcessor

router = APIRouter()
logger = logging.getLogger(__name__)

def _configure_module_logger():
    level_name = os.getenv('LOG_LEVEL', 'INFO').upper()
    level = getattr(logging, level_name, logging.INFO)
    if not hasattr(logging, level_name):
        logging.getLogger(__name__).warning(
            "Invalid LOG_LEVEL '%s'; defaulting to INFO", level_name
        )
    logger.setLevel(level)
    logger.propagate = True


_configure_module_logger()
status_lock = threading.Lock()

# Global processing status (similar to Flask app)
processing_status = {
    'is_processing': False,
    'current_batch': 0,
    'total_batches': 0,
    'processed_topics': 0,
    'failed_topics': 0,
    'skipped_topics': 0,
    'skipped_titles': [],
    'current_topic': None,
    'errors': [],
    'event_log': []
}


def record_status_event(message: str, level: str = "info"):
    """Append a timestamped message to the in-memory event log."""
    timestamp = datetime.now().strftime("%H:%M:%S")
    entry = f"[{timestamp}] {level.upper()}: {message}"
    with status_lock:
        event_log = processing_status.setdefault('event_log', [])
        event_log.append(entry)
        if len(event_log) > 50:
            del event_log[:-50]

# Initialize database and processor
db = UnifiedDatabase()  # Create instance, not just reference to class
processor = None


def init_processor():
    """Initialize the batch processor."""
    global processor
    try:
        processor = TopicBatchProcessor()
        logger.info("TopicBatchProcessor initialized")
        record_status_event("Initialized batch processor")
        return True
    except Exception as e:
        logger.exception("Error initializing TopicBatchProcessor: %s", e)
        record_status_event(f"Failed to initialize processor: {e}", level="error")
        return False


def process_single_batch(batch, batch_num, all_topic_ids):
    """Process a single batch of topics."""
    try:
        thread_name = threading.current_thread().name
        logger.info(
            "[Batch %s] Starting batch of %s topics on thread %s",
            batch_num + 1,
            len(batch),
            thread_name
        )
        record_status_event(
            f"Batch {batch_num + 1} started on {thread_name} with {len(batch)} topics"
        )
        
        # Update status to processing for all topics in this batch
        for topic in batch:
            # Use topic_status_id if available (NO title cleaning needed!)
            if 'topic_status_id' in topic and topic['topic_status_id']:
                db.update_topic_status_by_id(topic['topic_status_id'], 'processing')
                logger.debug("Updated topic_status_id=%s to 'processing'", topic['topic_status_id'])
            else:
                # Fallback: use raw title (should rarely happen)
                db.save_topic_status(topic['title'], 'processing', None)
        
        # Generate topics using Gemini
        generated_topics = processor.client.generate_topics(
            batch, 
            all_topic_ids=all_topic_ids,
            created_date=datetime.now().strftime("%Y-%m-%d"),
            updated_date=datetime.now().strftime("%Y-%m-%d")
        )
        
        # Small delay to respect rate limits
        time.sleep(1.0)
        
        # Handle response (single topic or list)
        if isinstance(generated_topics, dict):
            generated_topics = [generated_topics]
        
        logger.info(
            "[Batch %s] Completed successfully with %s topics on thread %s",
            batch_num + 1,
            len(generated_topics),
            thread_name
        )
        record_status_event(
            f"Batch {batch_num + 1} completed successfully"
        )
        return {
            'batch_num': batch_num,
            'success': True,
            'topics': generated_topics,
            'error': None
        }
    except Exception as e:
        logger.exception("[Batch %s] Failed with error: %s", batch_num + 1, e)
        record_status_event(
            f"Batch {batch_num + 1} failed: {e}",
            level="error"
        )
        return {
            'batch_num': batch_num,
            'success': False,
            'topics': [],
            'error': str(e)
        }


def process_topics_background(topic_titles, batch_size=5):
    """Process topics in background thread."""
    global processing_status
    logger.info(
        "Background processing started for %s topics with batch size %s",
        len(topic_titles),
        batch_size
    )
    record_status_event(
        f"Started processing {len(topic_titles)} topics (batch size {batch_size})"
    )
    try:
        # Initialize processor
        if not init_processor():
            with status_lock:
                processing_status.update({
                    'is_processing': False,
                    'errors': ['Failed to initialize processor']
                })
            logger.error("Processor initialization failed; aborting background processing")
            record_status_event("Processor initialization failed", level="error")
            return
        
        # Filter out topics that already exist and are completed
        topics_to_process = []
        skipped_topics = []
        retry_topics = []
        
        # Get the next available ID to avoid conflicts
        next_id = db.get_next_available_id()
        
        for i, title in enumerate(topic_titles):
            title = title.strip()
            
            # Check if topic_status exists for this title
            existing_status = db.get_topic_status_by_title(title)
            topic_status_id = None
            
            if existing_status:
                topic_status_id = existing_status['id']
                
                if existing_status['status'] == 'completed':
                    skipped_topics.append(title)
                    logger.info("Skipping existing completed topic: %s", title)
                    record_status_event(f"Skipped already completed topic: {title}")
                    continue
                elif existing_status['status'] in ['failed', 'pending']:
                    # Check if already in topics table
                    existing_topic = db.get_topic_by_title(title)
                    topic_id = existing_topic['id'] if existing_topic else (next_id + i)
                    
                    retry_topics.append({
                        'id': topic_id,
                        'topic_status_id': topic_status_id,
                        'title': title,
                        'status': 'pending',
                        'created_at': datetime.now().isoformat()
                    })
                    logger.info(
                        "Retrying existing topic with status '%s': %s (status_id=%s)",
                        existing_status['status'],
                        title,
                        topic_status_id
                    )
                    record_status_event(
                        f"Retrying topic {title} (status={existing_status['status']}, status_id={topic_status_id})"
                    )
                    continue
            else:
                # Create new topic_status entry
                topic_status_id = db.add_topic_for_processing(title)
                logger.info("Created new topic_status entry: %s (status_id=%s)", title, topic_status_id)
            
            # Use sequential IDs starting from next available ID
            topic_id = next_id + i
            topics_to_process.append({
                'id': topic_id,
                'topic_status_id': topic_status_id,
                'title': title,
                'status': 'pending',
                'created_at': datetime.now().isoformat()
            })
        
        # Combine new topics and retry topics
        all_topics_to_process = topics_to_process + retry_topics
        logger.info(
            "Prepared %s new topics and %s retries (skipped: %s)",
            len(topics_to_process),
            len(retry_topics),
            len(skipped_topics)
        )
        
        # If no topics to process, return early
        if not all_topics_to_process:
            processing_status.update({
                'is_processing': False,
                'processed_topics': len(skipped_topics),
                'skipped_topics': len(skipped_topics),
                'current_topic': f'All {len(skipped_topics)} topics already exist and are completed!'
            })
            logger.info("No topics to process; all %s topics were skipped", len(skipped_topics))
            return
        
        # Save topics to process with pending status (batch operation for better performance)
        topics_batch = [(topic['title'], 'pending', None) for topic in all_topics_to_process]
        db.save_topic_status_batch(topics_batch)
        logger.info(f"Batch saved {len(topics_batch)} topics with 'pending' status")
        
        # Update status with skipped topics info
        if skipped_topics:
            processing_status.update({
                'skipped_topics': len(skipped_topics),
                'skipped_titles': skipped_topics[:5]  # Show first 5 skipped topics
            })
        
        # Calculate batches
        total_batches = (len(all_topics_to_process) + batch_size - 1) // batch_size
        logger.info(
            "Scheduling %s batches (batch size=%s) for %s total topics",
            total_batches,
            batch_size,
            len(all_topics_to_process)
        )
        record_status_event(
            f"Scheduling {total_batches} batches for {len(all_topics_to_process)} topics"
        )

        with status_lock:
            processing_status.update({
                'is_processing': True,
                'current_batch': 0,
                'total_batches': total_batches,
                'processed_topics': len(skipped_topics),  # Count skipped as processed
                'failed_topics': 0,
                'current_topic': None,
                'errors': []
            })
        
        # Process in parallel batches
        all_topic_ids = [t['id'] for t in all_topics_to_process]
        
        # Calculate parallel processing parameters
        parallel_batches = min(80, total_batches)  # Max 10 parallel batches
        logger.info(
            "Parallel execution configured with up to %s concurrent batches",
            parallel_batches
        )
        batch_groups = []
        
        # Group batches for parallel processing
        for i in range(0, total_batches, parallel_batches):
            group_batches = []
            for batch_num in range(i, min(i + parallel_batches, total_batches)):
                start_idx = batch_num * batch_size
                end_idx = min(start_idx + batch_size, len(all_topics_to_process))
                batch = all_topics_to_process[start_idx:end_idx]
                group_batches.append((batch_num, batch))
            batch_groups.append(group_batches)
        logger.info("Created %s parallel groups", len(batch_groups))
        
        # Process each group of batches in parallel
        for group_idx, batch_group in enumerate(batch_groups):
            with status_lock:
                processing_status.update({
                    'current_batch': group_idx + 1,
                    'total_batches': len(batch_groups),
                    'current_topic': f"Processing parallel group {group_idx + 1}/{len(batch_groups)} ({len(batch_group)} batches)"
                })
            logger.info(
                "Processing group %s/%s containing %s batches",
                group_idx + 1,
                len(batch_groups),
                len(batch_group)
            )
            logger.debug(
                "[Parallel] Group %s contains batch indices: %s",
                group_idx + 1,
                [batch_num + 1 for batch_num, _ in batch_group]
            )
            record_status_event(
                f"Processing group {group_idx + 1}/{len(batch_groups)} with {len(batch_group)} batches"
            )
            
            # Process batches in parallel using ThreadPoolExecutor
            with ThreadPoolExecutor(max_workers=parallel_batches) as executor:
                logger.debug(
                    "[Parallel] Starting ThreadPoolExecutor for group %s with max_workers=%s",
                    group_idx + 1,
                    parallel_batches
                )
                # Submit all batches in this group for parallel processing
                future_to_batch = {}
                batch_lookup = {batch_num: batch for batch_num, batch in batch_group}
                for batch_num, batch in batch_group:
                    logger.info(
                        "Submitting batch %s (topics: %s) to executor",
                        batch_num + 1,
                        [t['title'] for t in batch]
                    )
                    record_status_event(
                        f"Submitted batch {batch_num + 1} (size={len(batch)}) to executor"
                    )
                    future = executor.submit(process_single_batch, batch, batch_num, all_topic_ids)
                    future_to_batch[future] = (batch_num, batch)
                
                # Collect results as they complete
                batch_results = []
                for future in as_completed(future_to_batch):
                    batch_num, batch = future_to_batch[future]
                    logger.debug(
                        "[Parallel] Batch %s future completed (thread=%s)",
                        batch_num + 1,
                        threading.current_thread().name
                    )
                for future in as_completed(future_to_batch):
                    batch_num, batch = future_to_batch[future]
                    try:
                        result = future.result()
                        batch_results.append(result)
                        logger.info("Batch %s finished with success=%s", batch_num + 1, result['success'])
                        status_msg = "succeeded" if result['success'] else "failed"
                        record_status_event(
                            f"Batch {batch_num + 1} finished with status {status_msg}"
                        )
                    except Exception as e:
                        logger.exception("Batch %s raised an exception: %s", batch_num + 1, e)
                        batch_results.append({
                            'batch_num': batch_num,
                            'success': False,
                            'error': str(e),
                            'topics': []
                        })
                
                # Process all results from this parallel group
                for result in batch_results:
                    if result['success']:
                        generated_topics = result['topics']
                        batch_num = result['batch_num']
                        original_batch = batch_lookup.get(batch_num, [])
                        
                        # Save successful topics
                        logger.info(f"Saving {len(generated_topics)} successful topics from batch {batch_num + 1}")
                        for i, topic in enumerate(generated_topics):
                            try:
                                # Get the original topic object to extract topic_status_id
                                original_topic = original_batch[i] if i < len(original_batch) else None
                                
                                db.save_topic(topic, f"web_batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
                                
                                # Use topic_status_id if available
                                # Pass Gemini's cleaned title as current_title
                                if original_topic and 'topic_status_id' in original_topic and original_topic['topic_status_id']:
                                    db.update_topic_status_by_id(
                                        original_topic['topic_status_id'], 
                                        'completed',
                                        current_title=topic['title']  # Gemini's cleaned title
                                    )
                                    logger.debug(
                                        "Updated topic_status_id=%s to 'completed' with current_title='%s'", 
                                        original_topic['topic_status_id'],
                                        topic['title']
                                    )
                                else:
                                    db.save_topic_status(topic['title'], 'completed', None)
                                
                                with status_lock:
                                    processing_status_copy = copy.deepcopy(processing_status)
                                    processing_status_copy['processed_topics'] += 1
                                    processing_status.update(processing_status_copy)
                            except Exception as e:
                                # Handle failure with topic_status_id
                                if original_topic and 'topic_status_id' in original_topic and original_topic['topic_status_id']:
                                    db.update_topic_status_by_id(original_topic['topic_status_id'], 'failed', str(e))
                                else:
                                    db.save_topic_status(topic['title'], 'failed', str(e))
                                    
                                with status_lock:
                                    processing_status_copy = copy.deepcopy(processing_status)
                                    processing_status_copy['failed_topics'] += 1
                                    processing_status.update(processing_status_copy)
                    else:
                        # Handle failed batch
                        failed_batch = batch_lookup.get(result['batch_num'])
                        if failed_batch is None:
                            logger.error(
                                "Batch %s failed but could not locate batch data for status update",
                                result['batch_num'] + 1
                            )
                            continue

                        for topic in failed_batch:
                            db.save_topic_status(topic['title'], 'failed', result['error'])
                            with status_lock:
                                processing_status_copy = copy.deepcopy(processing_status)
                                processing_status_copy['failed_topics'] += 1
                                processing_status.update(processing_status_copy)
                        
                        with status_lock:
                            processing_status_copy = copy.deepcopy(processing_status)
                            processing_status_copy['errors'].append(f"Batch {result['batch_num'] + 1} failed: {result['error']}")
                            processing_status.update(processing_status_copy)
                        logger.error(
                            "Batch %s failed; marked %s topics as failed",
                            result['batch_num'] + 1,
                            len(failed_batch)
                        )
        
        # Processing complete
        with status_lock:
            processing_status_copy = copy.deepcopy(processing_status)
            processing_status_copy['is_processing'] = False
            processing_status_copy['current_topic'] = 'Processing complete!'
            processing_status.update(processing_status_copy)
        logger.info(
            "Background processing finished. Processed=%s, failed=%s, skipped=%s",
            processing_status['processed_topics'],
            processing_status['failed_topics'],
            processing_status['skipped_topics']
        )
        
    except Exception as e:
        with status_lock:
            processing_status_copy = copy.deepcopy(processing_status)
            processing_status_copy['is_processing'] = False
            processing_status_copy['errors'].append(f"Processing failed: {str(e)}")
            processing_status.update(processing_status_copy)
        logger.exception("Background processing failed: %s", e)


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
    event_log: List[str]


class StatsResponse(BaseModel):
    total_topics: int
    completed_topics: int
    failed_topics: int
    success_rate: float
    average_difficulty: float
    category_count: int
    company_count: int


# API Endpoints
@router.post("/topics", response_model=Dict[str, Any])
async def create_topics(request: CreateTopicsRequest, background_tasks: BackgroundTasks):
    """Create topics from bulk input - saves as pending for worker processing."""
    topic_titles = request.topics
    batch_size = request.batch_size
    logger.info(
        "Received create_topics request with %s topics (batch_size=%s)",
        len(topic_titles),
        batch_size
    )

    # Validate batch size (per API call)
    if not isinstance(batch_size, int) or batch_size < 1 or batch_size > 5:
        logger.warning("Rejected create_topics request due to invalid batch size: %s", batch_size)
        raise HTTPException(status_code=400, detail="Batch size must be between 1 and 5 topics per API call")

    if not topic_titles:
        logger.warning("Rejected create_topics request due to missing topics")
        raise HTTPException(status_code=400, detail="No topics provided")

    # Save all topics with pending status
    saved_count = 0
    skipped_count = 0
    skipped_titles = []
    
    for title in topic_titles:
        original_title = title.strip()  # Keep original with all formatting
        
        # Check if topic already exists (by original title)
        existing_topic = db.get_topic_status_by_title(original_title)
        
        if existing_topic and existing_topic.get('status') == 'completed':
            skipped_count += 1
            skipped_titles.append(original_title)
            logger.info(f"Skipping already completed topic: {original_title}")
            continue
        
        # Save topic with ORIGINAL title (no cleaning!)
        # Gemini will clean it later and save as current_title
        success = db.save_topic_status(original_title, 'pending', None)
        if success:
            saved_count += 1
            logger.info(f"Saved topic '{original_title}' with pending status")
        else:
            logger.error(f"Failed to save topic '{original_title}'")
    
    logger.info(f"Created {saved_count} pending topics, skipped {skipped_count} completed topics")
    
    response = {
        "message": "Topics queued for processing",
        "total_topics": len(topic_titles),
        "saved_topics": saved_count,
        "skipped_topics": skipped_count
    }
    
    if skipped_titles:
        response["skipped_titles"] = skipped_titles[:5]  # Show first 5 skipped
    
    return response


@router.get("/topics", response_model=TopicsResponse)
async def get_topics(
    limit: int = Query(5, ge=1, le=100),
    offset: int = Query(0, ge=0),
    search: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    subcategory: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    complexity: Optional[str] = Query(None),
    company: Optional[str] = Query(None),
    tag: Optional[str] = Query(None),
    technology: Optional[str] = Query(None),
    sort_by: str = Query("created_date"),
    sort_order: str = Query("desc")
):
    """Get topics with pagination, search, and filtering."""
    try:
        # Force minimum limit of 1 (frontend sometimes sends 0)
        if limit < 1:
            limit = 5
        
        # Get topics with search and filters
        topics = db.get_topics_paginated(
            offset=offset, 
            limit=limit,
            search=search,
            category=category,
            subcategory=subcategory,
            status=status,
            complexity=complexity,
            company=company,
            tag=tag,
            technology=technology,
            sort_by=sort_by,
            sort_order=sort_order
        )
        
        # Parse JSON fields for Pydantic validation
        for topic in topics:
            json_fields = ['technologies', 'tags', 'related_topics', 'metrics', 
                          'implementation_details', 'learning_objectives', 'prerequisites']
            for field in json_fields:
                if field in topic and isinstance(topic[field], str):
                    try:
                        topic[field] = json.loads(topic[field])
                    except (json.JSONDecodeError, TypeError):
                        # Default to empty list/dict based on field type
                        topic[field] = [] if field != 'metrics' and field != 'implementation_details' else {}
        
        # Get total count for pagination (with same filters)
        total_count = db.get_topics_count(
            search=search,
            category=category,
            subcategory=subcategory,
            status=status,
            complexity=complexity,
            company=company,
            tag=tag,
            technology=technology
        )
        
        return TopicsResponse(
            topics=topics,
            total_count=total_count,
            limit=limit,
            offset=offset
        )
    except Exception as e:
        logger.error(f"Error in get_topics endpoint: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status", response_model=ProcessingStatusResponse)
async def get_status():
    """Get current processing status."""
    with status_lock:
        status_snapshot = copy.deepcopy(processing_status)
        status_snapshot.setdefault('event_log', [])
    return ProcessingStatusResponse(**status_snapshot)


@router.get("/topics/filter-options")
async def get_filter_options():
    """Get all available filter options for topics (categories, companies, etc.)."""
    try:
        options = db.get_filter_options()
        return {
            "success": True,
            "options": options
        }
    except Exception as e:
        logger.error(f"Error fetching filter options: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/topics/{topic_id}", response_model=TopicResponse)
async def get_topic(topic_id: int):
    """Get a specific topic."""
    topic = db.get_topic_by_id(topic_id)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    return TopicResponse(**topic)


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
    topic_status = db.get_topic_status(topic_id)
    if not topic_status:
        raise HTTPException(status_code=404, detail="Topic not found")
    
    if topic_status['status'] != 'failed':
        raise HTTPException(status_code=400, detail="Topic is not in failed status")
    
    # Retry processing
    try:
        if not processor:
            init_processor()
        
        topic_data = [{'id': topic_id, 'title': topic_status['title']}]
        all_ids = [topic_id]
        
        result = processor.client.generate_topics(topic_data, all_ids)
        
        if isinstance(result, dict):
            result = [result]
        
        for topic in result:
            db.save_topic(topic, f"retry_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
            db.save_topic_status(topic_status['title'], 'completed', None)
        
        return {"message": "Topic processed successfully"}
        
    except Exception as e:
        db.save_topic_status(topic_status['title'], 'failed', str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats", response_model=StatsResponse)
async def get_stats():
    """Get database statistics."""
    stats = db.get_stats()
    return StatsResponse(**stats)


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


@router.get("/processing-status")
async def get_processing_status():
    """Get current processing status for frontend display."""
    try:
        # Get processing summary from database
        summary = db.get_processing_summary()
        
        # Check if there are any pending or processing topics
        is_processing = summary['pending'] > 0 or summary['processing'] > 0
        
        return {
            "is_processing": is_processing,
            "pending_count": summary['pending'],
            "processing_count": summary['processing'],
            "completed_count": summary['completed'],
            "failed_count": summary['failed'],
            "total_count": summary['total'],
            "recent_failures": summary['recent_failures'],
            "show_status": is_processing or summary['failed'] > 0  # Show status if processing or has failures
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/worker-status")
async def get_worker_status():
    """Get worker service status."""
    try:
        # This endpoint can be used to check if worker is running
        # For now, we'll check if there are processing topics
        summary = db.get_processing_summary()
        
        # If there are topics in 'processing' status, worker is likely running
        worker_running = summary['processing'] > 0
        
        return {
            "worker_running": worker_running,
            "pending_topics": summary['pending'],
            "processing_topics": summary['processing'],
            "message": "Worker is processing topics" if worker_running else "Worker may be idle or not running"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
