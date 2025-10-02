#!/usr/bin/env python3
"""
Test script using gemini-2.5-flash model (same as your app) to compare behavior.
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

class FlashGeminiTester:
    """Test class using gemini-2.5-flash (same as your app)."""
    
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
        
        # Initialize the model - using gemini-2.5-flash (same as your app)
        self.model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            generation_config={
                "temperature": 0.7,
                "top_p": 0.9,
                "top_k": 40,
                "max_output_tokens": 32768,  # Same as your app
                "response_mime_type": "application/json"  # Same as your app
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
    
    async def test_with_delays(self, num_requests: int = 5, delay_seconds: float = 2.0):
        """Test requests with delays between them (like your app should do)."""
        logger.info(f"Testing {num_requests} requests with {delay_seconds}s delays...")
        
        results = []
        for i in range(num_requests):
            try:
                logger.info(f"Making request {i+1}/{num_requests}")
                response = await asyncio.to_thread(self.model.generate_content, "Explain how AI works in a few words")
                
                if response.text:
                    logger.info(f"Request {i+1} successful")
                    results.append({
                        'id': i+1,
                        'success': True,
                        'response': response.text[:100] + "..." if len(response.text) > 100 else response.text
                    })
                else:
                    logger.error(f"Request {i+1} returned empty response")
                    results.append({
                        'id': i+1,
                        'success': False,
                        'error': 'Empty response'
                    })
                
                # Add delay between requests (except for the last one)
                if i < num_requests - 1:
                    logger.info(f"Waiting {delay_seconds}s before next request...")
                    await asyncio.sleep(delay_seconds)
                    
            except Exception as e:
                logger.error(f"Request {i+1} failed: {e}")
                results.append({
                    'id': i+1,
                    'success': False,
                    'error': str(e)
                })
                
                # Add delay even after failures
                if i < num_requests - 1:
                    await asyncio.sleep(delay_seconds)
        
        # Summary
        successful = sum(1 for r in results if r.get('success', False))
        logger.info(f"Delayed test results: {successful}/{num_requests} successful")
        
        return results

def test_multiple_api_keys():
    """Test with multiple API keys to see if rotation helps."""
    try:
        from config import API_KEYS
        logger.info(f"Found {len(API_KEYS)} API keys in config")
        
        # Test first 5 keys with delays
        for i, api_key in enumerate(API_KEYS[:5]):
            logger.info(f"\n--- Testing with API key {i+1}: {api_key[:10]}... ---")
            try:
                tester = FlashGeminiTester(api_key)
                result = tester.test_simple_request()
                logger.info(f"Key {i+1} works: {result[:50]}...")
                
                # Add delay between keys
                if i < 4:
                    logger.info("Waiting 3s before testing next key...")
                    import time
                    time.sleep(3)
                    
            except Exception as e:
                logger.error(f"Key {i+1} failed: {e}")
                
    except ImportError:
        logger.error("Could not import API_KEYS from config.py")

async def main():
    """Main test function."""
    logger.info("=== Flash Model Gemini API Tester ===")
    
    # Test 1: Simple request (like your curl but with flash model)
    logger.info("\n1. Testing simple request with gemini-2.5-flash...")
    try:
        tester = FlashGeminiTester()
        result = tester.test_simple_request()
        print(f"\nSimple request result:\n{result}\n")
    except Exception as e:
        logger.error(f"Simple request failed: {e}")
    
    # Test 2: Multiple API keys with delays
    logger.info("\n2. Testing multiple API keys with delays...")
    test_multiple_api_keys()
    
    # Test 3: Sequential requests with delays (recommended approach)
    logger.info("\n3. Testing sequential requests with 2s delays...")
    try:
        tester = FlashGeminiTester()
        results = await tester.test_with_delays(num_requests=5, delay_seconds=2.0)
        
        # Summary
        successful = sum(1 for r in results if r.get('success', False))
        print(f"\nSequential test summary: {successful}/5 requests successful")
        
        for result in results:
            if result.get('success'):
                print(f"✓ Request {result['id']}: {result['response']}")
            else:
                print(f"✗ Request {result['id']}: {result.get('error', 'Unknown error')}")
        
    except Exception as e:
        logger.error(f"Sequential test failed: {e}")
    
    # Test 4: Test with longer delays (like your app should do)
    logger.info("\n4. Testing with 5s delays (recommended for production)...")
    try:
        tester = FlashGeminiTester()
        results = await tester.test_with_delays(num_requests=3, delay_seconds=5.0)
        
        # Summary
        successful = sum(1 for r in results if r.get('success', False))
        print(f"\nLong delay test summary: {successful}/3 requests successful")
        
    except Exception as e:
        logger.error(f"Long delay test failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
