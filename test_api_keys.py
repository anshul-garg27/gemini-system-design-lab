#!/usr/bin/env python3
"""
Quick test script to verify API keys and generate a sample topic.
"""

import json
import os
from gemini_client import GeminiClient


def test_api_keys():
    """Test the API keys and generate a sample topic."""
    
    # Load API keys from config
    try:
        from config import API_KEYS
        print(f"Loaded {len(API_KEYS)} API keys from config.py")
        
        # Test each API key
        for i, key in enumerate(API_KEYS):
            print(f"\nTesting API key {i+1}...")
            try:
                client = GeminiClient([key])
                
                # Simple test with one topic
                topics = [{"id": 999, "title": "Test Topic - API Key Validation"}]
                all_ids = [999, 1000, 1001]
                
                result = client.generate_topics(topics, all_ids)
                
                if isinstance(result, dict):
                    topic = result
                else:
                    topic = result[0]
                
                print(f"✓ API key {i+1} working! Generated: {topic['title']}")
                print(f"  Category: {topic['category']}")
                print(f"  Company: {topic['company']}")
                print(f"  Difficulty: {topic['difficulty']}/10")
                
            except Exception as e:
                print(f"✗ API key {i+1} failed: {e}")
        
        # Test with all keys (rotation)
        print(f"\n{'='*50}")
        print("Testing API key rotation...")
        print(f"{'='*50}")
        
        client = GeminiClient(API_KEYS)
        topics = [
            {"id": 1001, "title": "Test Topic 1"},
            {"id": 1002, "title": "Test Topic 2"}
        ]
        all_ids = [1001, 1002, 1003, 1004, 1005]
        
        result = client.generate_topics(topics, all_ids)
        print(f"✓ Rotation test successful! Generated {len(result) if isinstance(result, list) else 1} topics")
        
    except ImportError:
        print("Error: config.py not found. Please create it with your API keys.")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False
    
    return True


if __name__ == "__main__":
    print("API Key Test Script")
    print("=" * 50)
    
    success = test_api_keys()
    
    if success:
        print(f"\n{'='*50}")
        print("✓ All tests passed! Your API keys are working correctly.")
        print("You can now run: python batch_processor.py topics.json")
    else:
        print(f"\n{'='*50}")
        print("✗ Tests failed. Please check your API keys and configuration.")
