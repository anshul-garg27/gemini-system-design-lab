"""
API Health Check endpoints for monitoring API key status and quotas.
"""
import asyncio
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from .gemini_client import GeminiClient

router = APIRouter(prefix="/api/health", tags=["health"])

class APIKeyStatus(BaseModel):
    """Status of a single API key."""
    key_index: int
    key_preview: str  # First 10 characters
    status: str  # "healthy", "rate_limited", "quota_exceeded", "error"
    last_checked: datetime
    error_message: Optional[str] = None
    usage_count: int
    quota_info: Optional[Dict[str, Any]] = None

class HealthCheckResponse(BaseModel):
    """Complete health check response."""
    total_keys: int
    healthy_keys: int
    rate_limited_keys: int
    quota_exceeded_keys: int
    error_keys: int
    last_check: datetime
    api_keys: List[APIKeyStatus]
    recommendations: List[str]

async def check_single_api_key(key_index: int, api_key: str) -> APIKeyStatus:
    """Check the health of a single API key."""
    try:
        # Create a Gemini client with the specific API key
        client = GeminiClient(api_key_index=key_index)
        
        # Try to make a simple API call
        test_prompt = "Generate a simple JSON response: {\"status\": \"healthy\", \"timestamp\": \"2024-01-01T00:00:00Z\"}"
        
        start_time = datetime.now()
        response = await client.generate_content(test_prompt)
        end_time = datetime.now()
        
        # Parse response to check if it's valid JSON
        import json
        try:
            json.loads(response)
            status = "healthy"
            error_message = None
        except json.JSONDecodeError:
            status = "error"
            error_message = "Invalid JSON response"
            
    except Exception as e:
        error_str = str(e).lower()
        if "429" in error_str or "rate" in error_str:
            status = "rate_limited"
            error_message = str(e)
        elif "quota" in error_str or "limit" in error_str:
            status = "quota_exceeded"
            error_message = str(e)
        else:
            status = "error"
            error_message = str(e)
    
    # Get usage statistics
    stats = GeminiClient.get_api_key_stats()
    usage_count = stats["usage_count"].get(key_index, 0)
    
    return APIKeyStatus(
        key_index=key_index,
        key_preview=api_key[:10] + "...",
        status=status,
        last_checked=datetime.now(),
        error_message=error_message,
        usage_count=usage_count,
        quota_info=None  # Could be enhanced to extract quota info from error messages
    )

@router.get("/check", response_model=HealthCheckResponse)
async def check_api_health():
    """Check the health of all API keys."""
    try:
        # Get API key statistics
        stats = GeminiClient.get_api_key_stats()
        
        if stats["total_keys"] == 0:
            raise HTTPException(status_code=400, detail="No API keys configured")
        
        # Check each API key
        tasks = []
        for i in range(stats["total_keys"]):
            # Get the API key (we need to access the private _api_keys)
            if not GeminiClient._api_keys:
                GeminiClient._load_api_keys()
            
            if i < len(GeminiClient._api_keys):
                api_key = GeminiClient._api_keys[i]
                task = check_single_api_key(i, api_key)
                tasks.append(task)
        
        # Run all checks concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        api_keys = []
        healthy_count = 0
        rate_limited_count = 0
        quota_exceeded_count = 0
        error_count = 0
        
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                api_key_status = APIKeyStatus(
                    key_index=i,
                    key_preview="Error...",
                    status="error",
                    last_checked=datetime.now(),
                    error_message=str(result),
                    usage_count=0
                )
                error_count += 1
            else:
                api_key_status = result
                if result.status == "healthy":
                    healthy_count += 1
                elif result.status == "rate_limited":
                    rate_limited_count += 1
                elif result.status == "quota_exceeded":
                    quota_exceeded_count += 1
                else:
                    error_count += 1
            
            api_keys.append(api_key_status)
        
        # Generate recommendations
        recommendations = []
        if healthy_count == 0:
            recommendations.append("🚨 All API keys are experiencing issues. Check your API key configuration.")
        elif healthy_count < stats["total_keys"] // 2:
            recommendations.append("⚠️ More than half of your API keys are experiencing issues.")
        
        if rate_limited_count > 0:
            recommendations.append(f"⏱️ {rate_limited_count} API key(s) are rate limited. Wait before retrying.")
        
        if quota_exceeded_count > 0:
            recommendations.append(f"📊 {quota_exceeded_count} API key(s) have exceeded quota limits. Consider upgrading your plan.")
        
        if healthy_count > 0:
            recommendations.append(f"✅ {healthy_count} API key(s) are healthy and ready to use.")
        
        return HealthCheckResponse(
            total_keys=stats["total_keys"],
            healthy_keys=healthy_count,
            rate_limited_keys=rate_limited_count,
            quota_exceeded_keys=quota_exceeded_count,
            error_keys=error_count,
            last_check=datetime.now(),
            api_keys=api_keys,
            recommendations=recommendations
        )
        
    except Exception as e:
        logging.error(f"Health check failed: {e}")
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")

@router.get("/stats")
async def get_api_stats():
    """Get API key usage statistics."""
    try:
        stats = GeminiClient.get_api_key_stats()
        return {
            "api_key_stats": stats,
            "timestamp": datetime.now()
        }
    except Exception as e:
        logging.error(f"Failed to get API stats: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get API stats: {str(e)}")

@router.post("/test-key")
async def test_specific_key(key_index: int):
    """Test a specific API key by index."""
    try:
        stats = GeminiClient.get_api_key_stats()
        
        if key_index < 0 or key_index >= stats["total_keys"]:
            raise HTTPException(status_code=400, detail=f"Invalid key index. Must be between 0 and {stats['total_keys'] - 1}")
        
        # Get the API key
        if not GeminiClient._api_keys:
            GeminiClient._load_api_keys()
        
        if key_index >= len(GeminiClient._api_keys):
            raise HTTPException(status_code=400, detail="API key not found")
        
        api_key = GeminiClient._api_keys[key_index]
        result = await check_single_api_key(key_index, api_key)
        
        return result
        
    except Exception as e:
        logging.error(f"Failed to test API key {key_index}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to test API key: {str(e)}")
