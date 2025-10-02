#!/usr/bin/env python3
"""
Test script using the exact same API key from your curl command.
"""

import os
import sys
import asyncio
import logging
from typing import List, Dict, Any
import google.generativeai as genai
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class CurlKeyTester:
    """Test class using the exact API key from your curl command."""
    
    def __init__(self, api_key: str = "AIzaSyBdXAduqMEZLVb2cuaijAOEeP5qpMNS624"):
        """Initialize with the API key from your curl command."""
        self.api_key = api_key
        logger.info(f"Using curl API key: {self.api_key[:10]}...")
        
        # Configure the API
        genai.configure(api_key=self.api_key)
        
        # Initialize the model - using gemini-2.5-pro (same as your curl)
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
    
    async def test_multiple_requests(self, num_requests: int = 3, delay_seconds: float = 5.0):
        """Test multiple requests with delays."""
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
        logger.info(f"Test results: {successful}/{num_requests} successful")
        
        return results

async def main():
    """Main test function."""
    logger.info("=== Curl API Key Tester ===")
    
    # Test 1: Simple request (like your curl)
    logger.info("\n1. Testing simple request with curl API key...")
    try:
        tester = CurlKeyTester()
        result = tester.test_simple_request()
        print(f"\nSimple request result:\n{result}\n")
    except Exception as e:
        logger.error(f"Simple request failed: {e}")
    
    # Test 2: Multiple requests with delays
    logger.info("\n2. Testing multiple requests with 10s delays...")
    try:
        tester = CurlKeyTester()
        results = await tester.test_multiple_requests(num_requests=3, delay_seconds=10.0)
        
        # Summary
        successful = sum(1 for r in results if r.get('success', False))
        print(f"\nMultiple requests summary: {successful}/3 requests successful")
        
        for result in results:
            if result.get('success'):
                print(f"✓ Request {result['id']}: {result['response']}")
            else:
                print(f"✗ Request {result['id']}: {result.get('error', 'Unknown error')}")
        
    except Exception as e:
        logger.error(f"Multiple requests test failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
