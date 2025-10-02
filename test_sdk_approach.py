#!/usr/bin/env python3
"""
Test script using Google Generative AI SDK approach to test API calls and rate limiting.
This script mimics the same API call as your curl command but uses the SDK.
"""

import os
import sys
import asyncio
import logging
from typing import List, Dict, Any
import google.generativeai as genai
from datetime import datetime

# Add the app directory to path to import config
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SDKGeminiTester:
    """Test class using Google Generative AI SDK."""
    
    def __init__(self, api_key: str = None):
        """Initialize with a specific API key or use the first one from config."""
        if api_key:
            self.api_key = api_key
        else:
            # Load from config
            try:
                from config import API_KEYS
                self.api_key = API_KEYS[0]  # Use first API key
                logger.info(f"Using API key from config: {self.api_key[:10]}...")
            except ImportError:
                # Fallback to environment
                self.api_key = os.getenv('GOOGLE_AI_API_KEY')
                if not self.api_key:
                    raise ValueError("No API key found. Set GOOGLE_AI_API_KEY env var or add to config.py")
                logger.info(f"Using API key from environment: {self.api_key[:10]}...")
        
        # Configure the API
        genai.configure(api_key=self.api_key)
        
        # Initialize the model - using gemini-2.5-pro to match your curl
        self.model = genai.GenerativeModel(
            model_name="gemini-2.5-pro",
            generation_config={
                "temperature": 0.7,
                "top_p": 0.9,
                "top_k": 40,
                "max_output_tokens": 8192,
            }
        )
    
    def test_simple_request(self, prompt: str = "Explain how AI works in a few words") -> str:
        """Test a simple request similar to your curl command."""
        try:
            logger.info(f"Making request with prompt: {prompt}")
            response = self.model.generate_content(prompt)
            
            if response.text:
                logger.info("Request successful!")
                return response.text
            else:
                logger.error("Empty response received")
                return "Empty response"
                
        except Exception as e:
            logger.error(f"Request failed: {e}")
            raise e
    
    async def test_concurrent_requests(self, num_requests: int = 5, prompt: str = "Explain how AI works in a few words"):
        """Test multiple concurrent requests to see rate limiting behavior."""
        logger.info(f"Testing {num_requests} concurrent requests...")
        
        async def make_request(request_id: int):
            try:
                logger.info(f"Starting request {request_id}")
                # Use asyncio.to_thread to run the synchronous SDK call in a thread
                response = await asyncio.to_thread(self.model.generate_content, prompt)
                
                if response.text:
                    logger.info(f"Request {request_id} successful")
                    return {
                        'id': request_id,
                        'success': True,
                        'response': response.text[:100] + "..." if len(response.text) > 100 else response.text
                    }
                else:
                    logger.error(f"Request {request_id} returned empty response")
                    return {
                        'id': request_id,
                        'success': False,
                        'error': 'Empty response'
                    }
                    
            except Exception as e:
                logger.error(f"Request {request_id} failed: {e}")
                return {
                    'id': request_id,
                    'success': False,
                    'error': str(e)
                }
        
        # Create tasks for concurrent requests
        tasks = [make_request(i) for i in range(num_requests)]
        
        # Run all requests concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Analyze results
        successful = sum(1 for r in results if isinstance(r, dict) and r.get('success', False))
        failed = len(results) - successful
        
        logger.info(f"Concurrent test results: {successful} successful, {failed} failed")
        
        for result in results:
            if isinstance(result, dict):
                if result.get('success'):
                    logger.info(f"✓ Request {result['id']}: {result['response']}")
                else:
                    logger.error(f"✗ Request {result['id']}: {result.get('error', 'Unknown error')}")
            else:
                logger.error(f"✗ Exception: {result}")
        
        return results

def test_with_different_api_keys():
    """Test with different API keys to see if rotation helps."""
    try:
        from config import API_KEYS
        logger.info(f"Found {len(API_KEYS)} API keys in config")
        
        # Test first few keys
        for i, api_key in enumerate(API_KEYS[:3]):
            logger.info(f"\n--- Testing with API key {i+1}: {api_key[:10]}... ---")
            try:
                tester = SDKGeminiTester(api_key)
                result = tester.test_simple_request()
                logger.info(f"Key {i+1} works: {result[:50]}...")
            except Exception as e:
                logger.error(f"Key {i+1} failed: {e}")
                
    except ImportError:
        logger.error("Could not import API_KEYS from config.py")

async def main():
    """Main test function."""
    logger.info("=== SDK Gemini API Tester ===")
    
    # Test 1: Simple request (like your curl)
    logger.info("\n1. Testing simple request (like your curl)...")
    try:
        tester = SDKGeminiTester()
        result = tester.test_simple_request()
        print(f"\nSimple request result:\n{result}\n")
    except Exception as e:
        logger.error(f"Simple request failed: {e}")
    
    # Test 2: Test with different API keys
    logger.info("\n2. Testing different API keys...")
    test_with_different_api_keys()
    
    # Test 3: Concurrent requests (to simulate your app's behavior)
    logger.info("\n3. Testing concurrent requests...")
    try:
        tester = SDKGeminiTester()
        results = await tester.test_concurrent_requests(num_requests=5)
        
        # Summary
        successful = sum(1 for r in results if isinstance(r, dict) and r.get('success', False))
        print(f"\nConcurrent test summary: {successful}/5 requests successful")
        
    except Exception as e:
        logger.error(f"Concurrent test failed: {e}")
    
    # Test 4: High concurrency (like your app)
    logger.info("\n4. Testing high concurrency (20 requests)...")
    try:
        tester = SDKGeminiTester()
        results = await tester.test_concurrent_requests(num_requests=20)
        
        # Summary
        successful = sum(1 for r in results if isinstance(r, dict) and r.get('success', False))
        print(f"\nHigh concurrency test summary: {successful}/20 requests successful")
        
    except Exception as e:
        logger.error(f"High concurrency test failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
