"""
Orchestrator routes for content generation service.
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Dict, Any, List
import uuid
import asyncio
from datetime import datetime

from .schemas import (
    GenerateAllRequest, JobResponse, JobStatusResponse, ResultsResponse, RegenerateRequest
)
from .store import Store
from .service_tasks import get_task_service
from .gemini_client import GeminiClient

router = APIRouter()
store = Store()


async def run_generation_job_background(job_id: str, request: GenerateAllRequest, selected_platforms: List[Dict[str, str]]):
    """Background task for content generation."""
    try:
        task_service = get_task_service()
        await task_service.run_generation_job(job_id, request, selected_platforms)
    except Exception as e:
        print(f"Error in background task for job {job_id}: {e}")
        # Update job status to error
        try:
            await store.update_job_status(job_id, "error")
        except:
            pass


@router.get("/topics")
async def get_topics(limit: int = 50, offset: int = 0):
    """Get topics from the unified database."""
    try:
        topics = store.get_topics_paginated(limit=limit, offset=offset)
        return topics
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/content/generate-all", response_model=JobResponse)
async def generate_all_content(
    request: GenerateAllRequest,
    background_tasks: BackgroundTasks
):
    """
    Generate content for multiple platforms in parallel.
    """
    try:
        # Create job
        job_id = str(uuid.uuid4())
        
        # Parse target platforms
        selected = []
        for platform_format in request.targetPlatforms:
            platform, format_name = platform_format.split(":")
            selected.append({
                "platform": platform,
                "format": format_name
            })
        
        # Create job in database
        await store.create_job(
            job_id=job_id,
            topic_id=request.topicId,
            topic_name=request.topicName,
            status="running"
        )
        
        # Start background task for content generation
        background_tasks.add_task(
            run_generation_job_background,
            job_id,
            request,
            selected
        )
        
        return JobResponse(
            jobId=job_id,
            status="running",
            selected=selected
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/jobs/{job_id}", response_model=JobStatusResponse)
async def get_job_status_endpoint(job_id: str):
    """
    Get the status of a generation job.
    """
    try:
        # Get job status from database
        job_status = await store.get_job_status(job_id)
        
        if not job_status:
            raise HTTPException(status_code=404, detail="Job not found")
        
        # Get task progress
        tasks = await store.get_job_tasks(job_id)
        total_tasks = len(tasks)
        completed_tasks = len([t for t in tasks if t.get('status') == 'completed'])
        
        return JobStatusResponse(
            jobId=job_id,
            status=job_status.get('status', 'pending'),
            progress={"total": total_tasks, "done": completed_tasks},
            errors=[]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/results/{job_id}", response_model=ResultsResponse)
async def get_job_results_endpoint(job_id: str):
    """
    Get the results of a completed generation job.
    """
    try:
        # Import unified database here to avoid circular imports
        from unified_database import unified_db
        
        # Use unified database method that properly formats results
        results_data = await unified_db.get_job_results(job_id)
        
        if not results_data:
            raise HTTPException(status_code=404, detail="Job not found")
        
        return results_data
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/results/topic/{topic_id}")
async def get_results_by_topic(topic_id: str):
    """
    Get all content generation results for a specific topic.
    """
    try:
        from unified_database import unified_db
        results = await unified_db.get_results_by_topic(topic_id)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/api-keys/stats")
async def get_api_key_stats():
    """
    Get API key usage statistics for monitoring.
    """
    try:
        stats = GeminiClient.get_api_key_stats()
        # Add timestamp to the stats
        stats["timestamp"] = datetime.now().isoformat()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/content/regenerate", response_model=JobResponse)
async def regenerate_content(
    request: RegenerateRequest,
    background_tasks: BackgroundTasks
):
    """
    Regenerate content for specific platforms.
    """
    try:
        # Create new job for regeneration
        job_id = str(uuid.uuid4())
        
        # TODO: Get original job data and create new job
        # For now, return a placeholder response
        selected = []
        for target in request.targets:
            selected.append({
                "platform": target["platform"],
                "format": target["format"]
            })
        
        return JobResponse(
            jobId=job_id,
            status="running",
            selected=selected
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
