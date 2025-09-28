"""
Task service for content generation.
"""
import asyncio
import uuid
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import json
import traceback

from .schemas import (
    GenerateAllRequest, JobStatusEnum, ResultsResponse, PlatformRequest, ContentEnvelope, JobStatusResponse
)
from .gemini_client import GeminiClient
from .store import Store


class TaskService:
    """Service for managing content generation tasks."""
    
    def __init__(self):
        self.store = Store()
        self.max_concurrent_tasks = 6
        self.semaphore = asyncio.Semaphore(self.max_concurrent_tasks)
        # Don't initialize gemini_client here - create per task with different API keys
    
    async def run_generation_job(
        self, 
        job_id: str, 
        request: GenerateAllRequest, 
        selected_platforms: List[Dict[str, str]]
    ):
        """Run a complete generation job with multiple platforms."""
        try:
            # Create tasks for each platform with API key rotation
            tasks = []
            for i, platform_info in enumerate(selected_platforms):
                platform = platform_info["platform"]
                format_name = platform_info["format"]
                
                task_id = str(uuid.uuid4())
                await self.store.create_task(
                    task_id=task_id,
                    job_id=job_id,
                    platform=platform,
                    format_name=format_name,
                    status="pending"
                )
                
                # Create task coroutine with specific API key index for rotation
                # Use modulo to cycle through available API keys (0-12)
                api_key_index = i % 13  # Assuming 13 API keys (0-12)
                task_coro = self.run_single_task(
                    task_id=task_id,
                    platform=platform,
                    format_name=format_name,
                    request=request,
                    api_key_index=api_key_index
                )
                tasks.append(task_coro)
            
            # Run all tasks in parallel
            await asyncio.gather(*tasks, return_exceptions=True)
            
            # Update job status
            await self.update_job_status(job_id)
            
        except Exception as e:
            logging.error(f"Error in generation job {job_id}: {e}")
            logging.error(f"Traceback: {traceback.format_exc()}")
            # Update job status to error
            await self.store.update_job_status(job_id, "error")
    
    async def run_single_task(
        self,
        task_id: str,
        platform: str,
        format_name: str,
        request: GenerateAllRequest,
        api_key_index: Optional[int] = None
    ):
        """Run a single platform task with specific API key."""
        async with self.semaphore:
            try:
                await self.store.update_task_status(task_id, "running", started_at=datetime.now())
                
                # Generate content with specific API key
                logging.info(f"Task {task_id}: Using API key index {api_key_index} for {platform}:{format_name}")
                result = await self.generate_content(
                    platform=platform,
                    format_name=format_name,
                    request=request,
                    api_key_index=api_key_index
                )
                
                # Save result
                await self.store.save_task_result(
                    task_id=task_id,
                    raw_response=json.dumps(result),
                    normalized_json=json.dumps(result)
                )
                
                await self.store.update_task_status(task_id, "completed", finished_at=datetime.now())
                
            except Exception as e:
                error_msg = f"Error in task {task_id}: {e}"
                logging.error(error_msg)
                logging.error(f"Traceback: {traceback.format_exc()}")
                
                # No fallback content - let the error propagate
                
                await self.store.update_task_status(task_id, "error", error=str(e))
    
    async def generate_content(
        self,
        platform: str,
        format_name: str,
        request: GenerateAllRequest,
        api_key_index: Optional[int] = None
    ) -> Dict[str, Any]:
        """Generate content for a specific platform and format with API key rotation."""
        try:
            logging.info(f"Starting content generation for {platform}:{format_name}")
            logging.info(f"Topic: {request.topicName} (ID: {request.topicId})")
            logging.info(f"Description: {request.topicDescription[:100]}...")
            
            # Use the new ContentGenerator with PromptProcessor
            from .content_generator import ContentGenerator
            content_generator = ContentGenerator()
            
            # Override the Gemini client to use specific API key index
            if api_key_index is not None:
                content_generator.gemini_client = GeminiClient(api_key_index=api_key_index)
                logging.info(f"Using API key index {api_key_index} for {platform}:{format_name}")
            else:
                logging.info(f"Using default API key rotation for {platform}:{format_name}")
            
            logging.info(f"Initializing content generation with PromptProcessor...")
            
            # Generate content using the new system
            result = await content_generator.generate_platform_content(
                platform=platform,
                format_type=format_name,
                topic_id=request.topicId,
                topic_name=request.topicName,
                topic_description=request.topicDescription
            )
            
            logging.info(f"Content generation completed for {platform}:{format_name}")
            
            # Check if result is None
            if result is None:
                logging.error("Result is None - this should not happen!")
                raise Exception("Content generation returned None")
            
            # Check if result is ContentEnvelope or dict and handle accordingly
            if hasattr(result, 'meta') and hasattr(result, 'content'):
                # It's a ContentEnvelope object
                logging.info(f"Result meta type: {type(result.meta).__name__}")
                logging.info(f"Result content type: {type(result.content).__name__}")
                
                # Convert ContentEnvelope to dict for compatibility
                content_dict = {
                    "meta": result.meta.dict() if hasattr(result.meta, 'dict') else result.meta,
                    "content": result.content.dict() if hasattr(result.content, 'dict') else result.content
                }
            else:
                # It's already a dict (fallback case)
                logging.info(f"Result meta keys: {list(result.get('meta', {}).keys())}")
                logging.info(f"Result content keys: {list(result.get('content', {}).keys())}")
                content_dict = result
            
            logging.info(f"Successfully generated and converted content for {platform}/{format_name}")
            return content_dict
            
        except Exception as e:
            logging.error(f"Content generation failed for {platform}/{format_name}: {e}")
            logging.error(f"Traceback: {traceback.format_exc()}")
            # Re-raise the exception to expose the actual error
            raise e
    
    def build_prompt(self, platform: str, format_name: str, request: GenerateAllRequest) -> str:
        """Build prompt for specific platform and format."""
        # Load platform-specific body
        body_path = f"app/prompts/bodies/{platform}-{format_name}.txt"
        try:
            with open(body_path, "r") as f:
                body_template = f.read()
                # Check if this is a comprehensive prompt (starts with "SYSTEM:")
                if body_template.strip().startswith("SYSTEM:"):
                    # Use comprehensive prompt as-is (no header needed)
                    prompt = body_template
                else:
                    # Use legacy approach with header for older prompts
                    header_path = "app/prompts/header.txt"
                    try:
                        with open(header_path, "r") as f:
                            global_header = f.read()
                    except FileNotFoundError:
                        global_header = "Generate content for the following topic:\n\n"
                    prompt = f"{global_header}\n\n{body_template}"
        except FileNotFoundError:
            # Fallback for missing prompt files
            header_path = "app/prompts/header.txt"
            try:
                with open(header_path, "r") as f:
                    global_header = f.read()
            except FileNotFoundError:
                global_header = "Generate content for the following topic:\n\n"
            body_template = f"Generate {platform} {format_name} content for: {{topic_name}}\n\nDescription: {{topic_description}}"
            prompt = f"{global_header}\n\n{body_template}"
        
        # Replace placeholders
        prompt = prompt.replace("{topic_name}", request.topicName)
        prompt = prompt.replace("{topic_description}", request.topicDescription)
        prompt = prompt.replace("{audience}", request.audience.value)
        prompt = prompt.replace("{tone}", request.tone)
        prompt = prompt.replace("{locale}", request.locale.value)
        prompt = prompt.replace("{primary_url}", request.primaryUrl)
        
        return prompt
    
    
    def validate_response(self, platform: str, format_name: str, response: str) -> Dict[str, Any]:
        """Validate response against platform schema."""
        try:
            # Parse JSON
            data = json.loads(response)
            
            # TODO: Implement proper validation using schemas
            # For now, return the parsed data
            return data
            
        except json.JSONDecodeError as e:
            # Log the actual response for debugging
            logging.error(f"JSON parsing failed for {platform}/{format_name}")
            logging.error(f"Response length: {len(response)} characters")
            logging.error(f"Response preview (first 500 chars): {response[:500]}")
            logging.error(f"Response around error position: {response[max(0, e.pos-50):e.pos+50]}")
            
            # Try to clean common JSON issues
            cleaned_response = self.attempt_json_cleanup(response)
            if cleaned_response != response:
                try:
                    logging.info("Attempting to parse cleaned JSON...")
                    data = json.loads(cleaned_response)
                    logging.info("Successfully parsed cleaned JSON")
                    return data
                except json.JSONDecodeError:
                    logging.error("Cleaned JSON also failed to parse")
            
            raise ValueError(f"Invalid JSON response: {e}")
    
    def attempt_json_cleanup(self, response: str) -> str:
        """Attempt to clean common JSON formatting issues."""
        # Remove any text before the first {
        start_idx = response.find('{')
        if start_idx > 0:
            response = response[start_idx:]
        
        # Remove any text after the last }
        end_idx = response.rfind('}')
        if end_idx > 0:
            response = response[:end_idx + 1]
        
        # Fix common issues with comments in JSON
        lines = response.split('\n')
        cleaned_lines = []
        for line in lines:
            # Remove // comments
            if '//' in line:
                line = line[:line.find('//')]
            # Remove /* */ comments (simple case)
            if '/*' in line and '*/' in line:
                start = line.find('/*')
                end = line.find('*/') + 2
                line = line[:start] + line[end:]
            cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines)
    
    async def update_job_status(self, job_id: str):
        """Update job status based on task completion."""
        tasks = await self.store.get_job_tasks(job_id)
        
        if not tasks:
            return
        
        completed_tasks = [t for t in tasks if t["status"] == "completed"]
        error_tasks = [t for t in tasks if t["status"] == "error"]
        
        if len(completed_tasks) == len(tasks):
            status = "done"
        elif len(error_tasks) == len(tasks):
            status = "error"
        else:
            status = "running"
        
        # Update job status in database
        await self.store.update_job_status(job_id, status)


# Global task service instance - will be created when needed
task_service = None

def get_task_service():
    """Get or create the task service instance."""
    global task_service
    if task_service is None:
        task_service = TaskService()
    return task_service


# Public functions for routes
async def run_generation_job(job_id: str, request: GenerateAllRequest, selected_platforms: List[Dict[str, str]]):
    """Run a generation job."""
    service = get_task_service()
    await service.run_generation_job(job_id, request, selected_platforms)


async def run_single_platform_task(platform: str, format: str, request: PlatformRequest) -> ContentEnvelope:
    """Run a single platform task."""
    # Convert PlatformRequest to GenerateAllRequest format
    generate_request = GenerateAllRequest(
        topicId=request.topicId,
        topicName=request.topicName,
        topicDescription=request.topicDescription,
        audience=request.audience,
        tone=request.tone,
        locale=request.locale,
        primaryUrl=request.primaryUrl,
        brand=request.brand,
        targetPlatforms=[f"{platform}:{format}"],
        options=request.options
    )
    
    # Generate content with automatic API key rotation
    service = get_task_service()
    result = await service.generate_content(platform, format, generate_request)
    
    # TODO: Convert result to ContentEnvelope
    # For now, return a placeholder
    return ContentEnvelope(
        meta={
            "topic_id": request.topicId,
            "topic_title": request.topicName,
            "platform": platform,
            "format": format,
            "content_schema_version": "v1.0.0",
            "model_version": "gemini-2.5-flash",
            "prompt_version": f"{platform}-{format}-1.0",
            "audience": request.audience,
            "tone": request.tone,
            "locale": request.locale,
            "primary_keywords": [],
            "secondary_keywords": [],
            "lsi_terms": [],
            "canonical": request.primaryUrl,
            "brand": request.brand,
            "options": request.options
        },
        content=result
    )


async def get_job_status(job_id: str) -> Optional[JobStatusResponse]:
    """Get job status."""
    try:
        # Use store directly without creating task service (avoids Gemini client init)
        store = Store()
        job_data = await store.db.get_job_status(job_id)
        
        if not job_data:
            logging.warning(f"Job {job_id} not found")
            return None
        
        # Get task errors
        tasks = await store.get_job_tasks(job_id)
        errors = []
        for task in tasks:
            if task.get("status") == "error" and task.get("error"):
                errors.append({
                    "taskId": task["id"],
                    "platform": task["platform"],
                    "format": task["format"],
                    "message": task["error"]
                })
        
        return JobStatusResponse(
            jobId=job_id,
            status=JobStatusEnum(job_data["status"]),
            progress=job_data["progress"],
            errors=errors if errors else None
        )
    except Exception as e:
        logging.error(f"Error getting job status for {job_id}: {e}")
        logging.error(f"Traceback: {traceback.format_exc()}")
        return None


async def get_job_results(job_id: str) -> Optional[ResultsResponse]:
    """Get job results."""
    try:
        # Use store directly without creating task service (avoids Gemini client init)
        store = Store()
        results_data = await store.db.get_job_results(job_id)
        
        if not results_data:
            logging.warning(f"Results for job {job_id} not found")
            return None
        
        return ResultsResponse(
            jobId=job_id,
            status=results_data["status"],
            results=results_data["results"],
            errors=results_data["errors"]
        )
    except Exception as e:
        logging.error(f"Error getting job results for {job_id}: {e}")
        logging.error(f"Traceback: {traceback.format_exc()}")
        return None
