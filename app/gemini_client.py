"""
Gemini client for content generation.
"""
import os
import json
import logging
from typing import Dict, Any, Optional
import asyncio
import google.generativeai as genai


class GeminiClient:
    """Client for interacting with Gemini 2.5 Flash API."""
    
    # Class-level API key rotation
    _api_keys = []
    _current_key_index = 0
    _key_usage_count = {}
    
    def __init__(self, api_key_index: Optional[int] = None):
        """Initialize Gemini client with API key rotation support."""
        # Load API keys if not already loaded
        if not self._api_keys:
            self._load_api_keys()
        
        # Determine which API key to use
        if api_key_index is not None:
            # Use specific API key index
            if 0 <= api_key_index < len(self._api_keys):
                api_key = self._api_keys[api_key_index]
                self.api_key_index = api_key_index
            else:
                raise ValueError(f"API key index {api_key_index} out of range (0-{len(self._api_keys)-1})")
        else:
            # Use next available API key (round-robin)
            api_key = self._get_next_api_key()
        
        logging.info(f"Using API key index {self.api_key_index}: {api_key[:10]}...")
        
        # Configure the API
        genai.configure(api_key=api_key)
        
        # Initialize the model with enhanced configuration
        self.model = genai.GenerativeModel(
            model_name="gemini-flash-latest",
            generation_config={
                "temperature": 0.7,
                "top_p": 0.9,
                "top_k": 40,
                "max_output_tokens": 32768,  # Increased from 8192 to 32768
                "response_mime_type": "application/json"
            }
        )
        
        # Store for retry logic
        self.max_retries = 3
        self.retry_delay = 2
    
    @classmethod
    def _load_api_keys(cls):
        """Load API keys from config.py and environment variables."""
        # Try config.py first
        try:
            from config import API_KEYS
            if API_KEYS and len(API_KEYS) > 0:
                cls._api_keys = API_KEYS.copy()
                logging.info(f"Loaded {len(cls._api_keys)} API keys from config.py")
        except ImportError:
            logging.warning("config.py not found or API_KEYS not defined")
        
        # Fallback to environment variables if config.py not available
        if not cls._api_keys:
            api_key = os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_AI_API_KEY')
            if api_key:
                cls._api_keys = [api_key]
                logging.info("Using API key from environment variables")
        
        if not cls._api_keys:
            raise ValueError("No Gemini API keys found. Add API_KEYS to config.py or set GEMINI_API_KEY/GOOGLE_AI_API_KEY environment variable")
        
        # Initialize usage count for all keys
        if not cls._key_usage_count:
            cls._key_usage_count = {i: 0 for i in range(len(cls._api_keys))}
    
    @classmethod
    def _get_next_api_key(cls):
        """Get the next API key using round-robin rotation."""
        if not cls._api_keys:
            cls._load_api_keys()
        
        # Use round-robin to get next key
        api_key = cls._api_keys[cls._current_key_index]
        key_index = cls._current_key_index
        
        # Update usage count
        cls._key_usage_count[key_index] += 1
        
        # Move to next key for next request
        cls._current_key_index = (cls._current_key_index + 1) % len(cls._api_keys)
        
        # Store the index for this instance
        return api_key
    
    def _get_next_api_key(self):
        """Instance method to get next API key and store index."""
        api_key = self.__class__._api_keys[self.__class__._current_key_index]
        self.api_key_index = self.__class__._current_key_index
        
        # Update usage count
        self.__class__._key_usage_count[self.api_key_index] += 1
        
        # Move to next key for next request
        self.__class__._current_key_index = (self.__class__._current_key_index + 1) % len(self.__class__._api_keys)
        
        return api_key
    
    @classmethod
    def get_api_key_stats(cls):
        """Get comprehensive API key usage statistics."""
        # Ensure API keys are loaded
        if not cls._api_keys:
            cls._load_api_keys()
        
        # Calculate usage statistics
        total_usage = sum(cls._key_usage_count.values())
        unused_keys = len([k for k, v in cls._key_usage_count.items() if v == 0])
        
        return {
            "total_keys": len(cls._api_keys),
            "current_key_index": cls._current_key_index,
            "usage_count": cls._key_usage_count.copy(),
            "total_usage": total_usage,
            "unused_keys": unused_keys,
            "keys_with_usage": len(cls._api_keys) - unused_keys,
            "remaining_keys": unused_keys
        }

    async def generate_content(self, prompt: str) -> str:
        """
        Generate content using Gemini 2.5 Flash with API key rotation on rate limits.
        
        Args:
            prompt: The prompt to send to Gemini
            
        Returns:
            Generated content as JSON string
        """
        last_error = None
        
        for attempt in range(self.max_retries + 1):
            try:
                logging.info(f"Gemini API attempt {attempt + 1}/{self.max_retries + 1} with key index {self.api_key_index}")
                
                # Generate content using the SDK
                response = await asyncio.to_thread(
                    self.model.generate_content, 
                    prompt
                )
                
                # Extract the generated text
                if response.text:
                    logging.info(f"Gemini API success on attempt {attempt + 1}")
                    return response.text
                else:
                    last_error = Exception("Empty response from Gemini API")
                    logging.warning("Gemini API returned empty response")
                    
            except Exception as e:
                logging.error(f"Gemini API error on attempt {attempt + 1}: {e}")
                last_error = e
                
                # Check if it's a rate limit error and try API key rotation
                if "429" in str(e) or "quota" in str(e).lower():
                    logging.warning(f"Rate limit hit with API key {self.api_key_index}")
                    
                    # Try to rotate to next API key
                    if len(self._api_keys) > 1:
                        try:
                            # Get next API key
                            next_api_key = self._get_next_api_key()
                            logging.info(f"Rotating to API key index {self.api_key_index}")
                            
                            # Reconfigure with new API key
                            genai.configure(api_key=next_api_key)
                            
                            # Reinitialize the model with new API key
                            self.model = genai.GenerativeModel(
                                model_name="gemini-flash-latest",
                                generation_config={
                                    "temperature": 0.7,
                                    "top_p": 0.9,
                                    "top_k": 40,
                                    "max_output_tokens": 32768,  # Increased from 8192 to 32768
                                    "response_mime_type": "application/json"
                                }
                            )
                            
                            # Continue with retry using new API key
                            continue
                            
                        except Exception as rotation_error:
                            logging.error(f"API key rotation failed: {rotation_error}")
                    
                    # If rotation failed or no more keys, wait and retry with same key
                    wait_time = 2 ** attempt
                    logging.warning(f"Rate limited, waiting {wait_time}s before retry")
                    if attempt < self.max_retries:
                        await asyncio.sleep(wait_time)
                        continue
                    else:
                        break
                
                # For other errors, wait and retry
                if attempt < self.max_retries:
                    wait_time = self.retry_delay * (attempt + 1)
                    logging.warning(f"Waiting {wait_time}s before retry")
                    await asyncio.sleep(wait_time)
                    continue
                else:
                    break
        
        # If all retries failed, raise the last error
        if last_error:
            raise last_error
        else:
            raise Exception("Content generation failed after all retries")
    
    async def generate_with_retry(self, prompt: str, max_retries: int = 1) -> str:
        """
        Generate content with retry logic.
        
        Args:
            prompt: The prompt to send to Gemini
            max_retries: Maximum number of retries
            
        Returns:
            Generated content as string
        """
        original_max_retries = self.max_retries
        self.max_retries = max_retries
        
        try:
            return await self.generate_content(prompt)
        finally:
            self.max_retries = original_max_retries
