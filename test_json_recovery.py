#!/usr/bin/env python3
"""
Simple test for JSON recovery logic without dependencies.
"""

import json
import logging
from typing import Optional, Dict, Any

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

print("Starting JSON recovery test...")

class JSONRecoveryTester:
    """Test class for JSON recovery methods."""

    def _advanced_json_recovery(self, raw_response: str) -> Optional[Dict[str, Any]]:
        """Advanced JSON recovery using multiple strategies."""
        try:
            response = raw_response.strip()

            # Strategy 1: Remove any text before the first '{'
            start_idx = response.find('{')
            if start_idx > 0:
                logger.info(f"Removing {start_idx} characters before JSON start")
                response = response[start_idx:]

                # Try to parse the cleaned response
                try:
                    return json.loads(response)
                except json.JSONDecodeError:
                    pass

            # Strategy 2: Find the largest valid JSON substring
            json_start = response.find('{')
            json_end = response.rfind('}')

            if json_start != -1 and json_end != -1 and json_end > json_start:
                json_candidate = response[json_start:json_end + 1]

                # Count braces to ensure they're balanced
                brace_count = 0
                for char in json_candidate:
                    if char == '{':
                        brace_count += 1
                    elif char == '}':
                        brace_count -= 1
                        if brace_count < 0:
                            break

                if brace_count == 0:
                    try:
                        return json.loads(json_candidate)
                    except json.JSONDecodeError:
                        pass

            return None

        except Exception as e:
            logger.warning(f"Advanced JSON recovery failed: {e}")
            return None

def test_json_recovery():
    """Test the JSON recovery functionality."""
    logger.info("Testing JSON recovery functionality...")

    tester = JSONRecoveryTester()

    # Test case 1: Valid JSON
    valid_json = '{"meta": {"topic_id": "123"}, "content": {"title": "Test"}}'
    result = tester._advanced_json_recovery(valid_json)
    logger.info(f"Valid JSON recovery: {'SUCCESS' if result else 'FAILED'}")
    if result:
        logger.info(f"Extracted title: {result.get('content', {}).get('title')}")

    # Test case 2: JSON with text before it
    json_with_prefix = 'Here is some text before the JSON: {"meta": {"topic_id": "123"}, "content": {"title": "Test"}}'
    result = tester._advanced_json_recovery(json_with_prefix)
    logger.info(f"JSON with prefix recovery: {'SUCCESS' if result else 'FAILED'}")
    if result:
        logger.info(f"Extracted title: {result.get('content', {}).get('title')}")

    # Test case 3: Malformed JSON (simulate what Gemini might return)
    malformed_json = 'Here is some explanation text that Gemini might return before the actual JSON content: {"meta": {"topic_id": "123"}, "content": {"title": "Test"}}'
    result = tester._advanced_json_recovery(malformed_json)
    logger.info(f"Malformed JSON with prefix recovery: {'SUCCESS' if result else 'FAILED'}")
    if result:
        logger.info(f"Extracted title: {result.get('content', {}).get('title')}")

    # Test case 4: Simulate the actual error from the logs (JSON starting at wrong position)
    problematic_response = 'Some text that causes "Expecting property name enclosed in double quotes" error: {"meta": {"topic_id": "1727"}, "content": {"title": "Infrastructure as Code"}}'
    result = tester._advanced_json_recovery(problematic_response)
    logger.info(f"Problematic response recovery: {'SUCCESS' if result else 'FAILED'}")
    if result:
        logger.info(f"Extracted content: {result}")

if __name__ == "__main__":
    logger.info("Starting JSON recovery tests...")
    test_json_recovery()
    logger.info("JSON recovery tests completed!")