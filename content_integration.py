"""
Integration service to connect Topic Generator with Content Generator.
"""
import requests
import json
from typing import List, Dict, Any


class ContentIntegrationService:
    """Service to integrate topic generation with content generation."""
    
    def __init__(self):
        self.topic_service_url = "http://localhost:5001"
        self.content_service_url = "http://localhost:8000"
    
    def get_topics_for_content_generation(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get completed topics from the topic generator."""
        try:
            response = requests.get(f"{self.topic_service_url}/api/topics", params={
                'limit': limit,
                'status': 'completed'
            })
            response.raise_for_status()
            return response.json().get('topics', [])
        except Exception as e:
            print(f"Error fetching topics: {e}")
            return []
    
    def generate_content_for_topic(self, topic: Dict[str, Any], platforms: List[str]) -> Dict[str, Any]:
        """Generate content for a specific topic across multiple platforms."""
        try:
            # Prepare request for content generation service
            content_request = {
                "topicId": str(topic['id']),
                "topicName": topic['title'],
                "topicDescription": topic.get('description', topic['title']),
                "audience": "intermediate",  # Default, could be derived from topic
                "tone": "clear, confident, non-cringe",
                "locale": "en",
                "primaryUrl": f"https://example.com/topic/{topic['id']}",
                "brand": {
                    "siteUrl": "https://example.com",
                    "handles": {
                        "instagram": "@yourhandle",
                        "x": "@yourhandle",
                        "linkedin": "yourhandle",
                        "youtube": "yourhandle",
                        "github": "yourhandle"
                    },
                    "utmBase": f"utm_source={{platform}}&utm_medium=social&utm_campaign={topic['id']}"
                },
                "targetPlatforms": platforms,
                "options": {
                    "include_images": True,
                    "max_length_levels": "standard",
                    "force": False
                }
            }
            
            # Call content generation service
            response = requests.post(
                f"{self.content_service_url}/api/content/generate-all",
                json=content_request,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return response.json()
            
        except Exception as e:
            print(f"Error generating content for topic {topic['id']}: {e}")
            return {"error": str(e)}
    
    def get_content_results(self, job_id: str) -> Dict[str, Any]:
        """Get results from content generation job."""
        try:
            response = requests.get(f"{self.content_service_url}/api/results/{job_id}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching content results: {e}")
            return {"error": str(e)}
    
    def batch_generate_content(self, topic_ids: List[int], platforms: List[str]) -> List[Dict[str, Any]]:
        """Generate content for multiple topics in batch."""
        results = []
        
        # Get topics
        topics = self.get_topics_for_content_generation(limit=len(topic_ids))
        
        for topic in topics:
            if topic['id'] in topic_ids:
                result = self.generate_content_for_topic(topic, platforms)
                results.append({
                    'topic_id': topic['id'],
                    'topic_name': topic['title'],
                    'content_job': result
                })
        
        return results


# Example usage
if __name__ == "__main__":
    integration_service = ContentIntegrationService()
    
    # Example: Generate content for topics with IDs 1, 2, 3
    topic_ids = [1, 2, 3]
    platforms = ["instagram:carousel", "x_twitter:thread", "youtube:long_form"]
    
    results = integration_service.batch_generate_content(topic_ids, platforms)
    
    for result in results:
        print(f"Topic: {result['topic_name']}")
        print(f"Content Job: {result['content_job']}")
        print("---")
