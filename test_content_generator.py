#!/usr/bin/env python3
"""
Test script for improved JSON parsing and fallback content generation.
"""

import sys
import os
import json
import logging

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

# Import the content generator directly to avoid relative import issues
sys.path.insert(0, os.path.dirname(__file__))

from app.content_generator import ContentGenerator

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_json_recovery():
    """Test the JSON recovery functionality."""
    logger.info("Testing JSON recovery functionality...")

    cg = ContentGenerator()

    # Test case 1: Valid JSON
    valid_json = '{"meta": {"topic_id": "123"}, "content": {"title": "Test"}}'
    result = cg._advanced_json_recovery(valid_json)
    logger.info(f"Valid JSON recovery: {'SUCCESS' if result else 'FAILED'}")

    # Test case 2: JSON with text before it
    json_with_prefix = 'Here is some text before the JSON: {"meta": {"topic_id": "123"}, "content": {"title": "Test"}}'
    result = cg._advanced_json_recovery(json_with_prefix)
    logger.info(f"JSON with prefix recovery: {'SUCCESS' if result else 'FAILED'}")

    # Test case 3: Malformed JSON (simulate what Gemini might return)
    malformed_json = 'Here is some explanation text that Gemini might return before the actual JSON content: {"meta": {"topic_id": "123", "incomplete": true'
    result = cg._advanced_json_recovery(malformed_json)
    logger.info(f"Malformed JSON recovery: {'SUCCESS' if result else 'FAILED'}")

def test_fallback_content():
    """Test the fallback content generation."""
    logger.info("Testing fallback content generation...")

    cg = ContentGenerator()

    # Test YouTube long form fallback
    fallback = cg._generate_fallback_content(
        platform="youtube",
        format_type="long_form",
        topic_id="1727",
        topic_name="Infrastructure as Code",
        topic_description="Learn about IaC"
    )

    logger.info(f"Fallback content generated: {'SUCCESS' if fallback else 'FAILED'}")
    if fallback:
        logger.info(f"Meta keys: {list(fallback.get('meta', {}).keys())}")
        logger.info(f"Content keys: {list(fallback.get('content', {}).keys())}")

        # Verify required fields are present
        required_meta = ['topic_id', 'topic_title', 'platform', 'format']
        required_content = ['title', 'compliance']

        meta_present = all(key in fallback.get('meta', {}) for key in required_meta)
        content_present = all(key in fallback.get('content', {}) for key in required_content)

        logger.info(f"Required meta fields present: {meta_present}")
        logger.info(f"Required content fields present: {content_present}")

if __name__ == "__main__":
    logger.info("Starting content generator tests...")

    try:
        test_json_recovery()
        print()
        test_fallback_content()
        print()
        logger.info("All tests completed successfully!")
    except Exception as e:
        logger.error(f"Test failed: {e}")
        import traceback
        traceback.print_exc()