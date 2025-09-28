#!/usr/bin/env python3
"""
Example script demonstrating how to use the Gemini client for system design topics.
"""

import json
import os
from gemini_client import GeminiClient


def main():
    """Demonstrate basic usage of the GeminiClient."""
    
    # Check for API keys
    try:
        from config import API_KEYS
        if not API_KEYS:
            print("Error: No API keys found in config.py")
            return
    except ImportError:
        if not os.getenv('GOOGLE_AI_API_KEY'):
            print("Error: Please set API keys in config.py or GOOGLE_AI_API_KEY environment variable")
            print("Get your API key from: https://aistudio.google.com/")
            return
    
    # Example topics
    topics = [
        {"id": 101, "title": "How WhatsApp Group Calls Scale to Dozens"},
        {"id": 102, "title": "How Redis Internally Works"}
    ]
    
    # All available topic IDs for cross-linking
    all_topic_ids = [101, 102, 103, 104, 105]
    
    try:
        # Initialize client
        print("Initializing Gemini client...")
        client = GeminiClient()
        
        # Generate topics
        print("Generating topics...")
        result = client.generate_topics(topics, all_topic_ids)
        
        # Display results
        print("\n" + "="*60)
        print("GENERATED TOPICS")
        print("="*60)
        
        # Handle both single object and array responses
        if isinstance(result, dict):
            topics_result = [result]
        else:
            topics_result = result
        
        for topic in topics_result:
            print(f"\nTopic {topic['id']}: {topic['title']}")
            print(f"Category: {topic['category']}")
            print(f"Company: {topic['company']}")
            print(f"Complexity: {topic['complexity_level']} (Difficulty: {topic['difficulty']}/10)")
            print(f"Technologies: {', '.join(topic['technologies'])}")
            print(f"Description: {topic['description']}")
            print(f"Read time: {topic['estimated_read_time']}")
            print(f"Related topics: {topic['related_topics']}")
        
        # Save to file
        output_file = "example_output.json"
        with open(output_file, 'w') as f:
            json.dump(result, f, indent=2)
        print(f"\nResults saved to: {output_file}")
        
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
