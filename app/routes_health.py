"""
API Health Check endpoints for monitoring API key status and quotas.
"""
import asyncio
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from gemini_client import GeminiClient

router = APIRouter(prefix="/api/health", tags=["health"])

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
        # Create a GeminiClient with a specific API key
        # We'll temporarily create a client with just this one key
        temp_client = GeminiClient(api_keys=[api_key])
        
        # Create a simple test request
        test_topics = [{"id": 99999, "title": "API Health Check Test"}]
        all_topic_ids = [99999]
        
        start_time = datetime.now()
        
        # Try a simple generation - this will test if the API key works
        try:
            result = temp_client.generate_topics(
                topics=test_topics[:1],  # Just one topic
                all_topic_ids=all_topic_ids,
                created_date="2024-01-01",
                updated_date="2024-01-01"
            )
            
            # If we got a result, the API is working
            if result:
                status = "healthy"
                error_message = None
            else:
                status = "error"
                error_message = "Empty response"
                
        except Exception as e:
            raise e
            
    except Exception as e:
        error_str = str(e)
        logging.error(f"Health check error for key {key_index}: {error_str}")
        
        # More specific error checking
        if "429" in error_str or "rate limit" in error_str.lower():
            status = "rate_limited"
            error_message = str(e)
        elif "quota" in error_str.lower() and "exceeded" in error_str.lower():
            status = "quota_exceeded"  
            error_message = str(e)
        elif "invalid" in error_str.lower() and "api" in error_str.lower():
            status = "error"
            error_message = "Invalid API key"
        elif "api call failed" in error_str.lower():
            # Check the status code in the error message
            if "429" in error_str:
                status = "rate_limited"
            elif "403" in error_str or "401" in error_str:
                status = "error"
                error_message = "Authentication error"
            else:
                status = "error"
            error_message = str(e)
        else:
            # Don't assume quota exceeded for generic errors
            status = "error"
            error_message = str(e)
    
    # Since root GeminiClient doesn't have get_api_key_stats, use defaults
    usage_count = 0
    
    return APIKeyStatus(
        key_index=key_index,
        key_preview=api_key[:10] + "..." if api_key else f"Key_{key_index}...",
        status=status,
        last_checked=datetime.now(),
        error_message=error_message,
        usage_count=usage_count,
        quota_info=None
    )

@router.get("/check", response_model=HealthCheckResponse)
async def check_api_health():
    """Check the health of all API keys."""
    try:
        # Load API keys the same way GeminiClient does
        api_keys = []
        
        # Try to import from config file first
        try:
            from config import API_KEYS
            if API_KEYS and len(API_KEYS) > 0:
                api_keys = API_KEYS.copy()
                logger.info(f"Loaded {len(api_keys)} API keys from config.py")
        except ImportError:
            logger.info("config.py not found or API_KEYS not defined")
        
        # Fallback to environment variable if config.py not available
        if not api_keys:
            import os
            env_key = os.getenv('GOOGLE_AI_API_KEY')
            if env_key:
                api_keys = [env_key]
                logger.info("Using API key from environment variable")
        
        if not api_keys:
            raise HTTPException(status_code=400, detail="No API keys configured. Add API_KEYS to config.py or set GOOGLE_AI_API_KEY environment variable")
        
        total_keys = len(api_keys)
        logger.info(f"Checking health of {total_keys} API keys")
        
        # Check each API key
        tasks = []
        for i, api_key in enumerate(api_keys):
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
        elif healthy_count < total_keys // 2:
            recommendations.append("⚠️ More than half of your API keys are experiencing issues.")
        
        if rate_limited_count > 0:
            recommendations.append(f"⏱️ {rate_limited_count} API key(s) are rate limited. Wait before retrying.")
        
        if quota_exceeded_count > 0:
            recommendations.append(f"📊 {quota_exceeded_count} API key(s) have exceeded quota limits. Consider upgrading your plan.")
        
        if healthy_count > 0:
            recommendations.append(f"✅ {healthy_count} API key(s) are healthy and ready to use.")
        
        return HealthCheckResponse(
            total_keys=total_keys,
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
        # Load API keys to get count
        api_keys = []
        
        try:
            from config import API_KEYS
            if API_KEYS and len(API_KEYS) > 0:
                api_keys = API_KEYS.copy()
        except ImportError:
            pass
        
        if not api_keys:
            import os
            env_key = os.getenv('GOOGLE_AI_API_KEY')
            if env_key:
                api_keys = [env_key]
        
        return {
            "api_key_stats": {
                "total_keys": len(api_keys),
                "message": f"Found {len(api_keys)} API key(s) configured",
                "source": "config.py" if len(api_keys) > 1 else "environment variable"
            },
            "timestamp": datetime.now()
        }
    except Exception as e:
        logging.error(f"Failed to get API stats: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get API stats: {str(e)}")

@router.post("/test-key")
async def test_specific_key(key_index: int):
    """Test a specific API key by index."""
    try:
        # Load API keys
        api_keys = []
        
        try:
            from config import API_KEYS
            if API_KEYS and len(API_KEYS) > 0:
                api_keys = API_KEYS.copy()
        except ImportError:
            pass
        
        if not api_keys:
            import os
            env_key = os.getenv('GOOGLE_AI_API_KEY')
            if env_key:
                api_keys = [env_key]
        
        if not api_keys:
            raise HTTPException(status_code=400, detail="No API keys configured")
        
        if key_index < 0 or key_index >= len(api_keys):
            raise HTTPException(status_code=400, detail=f"Invalid key index. Must be between 0 and {len(api_keys) - 1}")
        
        # Test the specific key
        result = await check_single_api_key(key_index, api_keys[key_index])
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Failed to test API key {key_index}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to test API key: {str(e)}")
