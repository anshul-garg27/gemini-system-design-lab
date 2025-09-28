#!/usr/bin/env python3
"""
Gemini 2.5 Flash client for generating system design topics with structured JSON output.
"""

import json
import os
import sys
from contextlib import contextmanager
from datetime import datetime
from queue import SimpleQueue
from typing import List, Dict, Any, Union
import requests
from jsonschema import validate, ValidationError
import random


class GeminiClient:
    """Client for Gemini 2.5 Flash API with structured output support."""
    
    def __init__(self, api_keys: List[str] = None):
        """Initialize the Gemini client.
        
        Args:
            api_keys: List of Google AI API keys for rotation. If None, will try to get from config or env var.
        """
        if api_keys:
            self.api_keys = api_keys
        else:
            # Try to import from config file first
            try:
                from config import API_KEYS
                self.api_keys = API_KEYS
            except ImportError:
                # Fall back to environment variable
                env_key = os.getenv('GOOGLE_AI_API_KEY')
                if env_key:
                    self.api_keys = [env_key]
                else:
                    raise ValueError("API keys required. Set API_KEYS in config.py or GOOGLE_AI_API_KEY env var.")
        
        if not self.api_keys:
            raise ValueError("At least one API key required.")
        
        # Shuffle keys so concurrent workers distribute load fairly
        shuffled_keys = self.api_keys[:]
        random.shuffle(shuffled_keys)
        self._key_queue: SimpleQueue[str] = SimpleQueue()
        for key in shuffled_keys:
            self._key_queue.put(key)
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent"
        
        # Load the JSON schema for validation
        self.schema = self._load_schema()
    
    @contextmanager
    def _acquire_api_key(self):
        """Context manager that yields a temporarily reserved API key."""
        api_key = self._key_queue.get()
        try:
            yield api_key
        finally:
            self._key_queue.put(api_key)
    
    @staticmethod
    def _get_headers(api_key: str) -> Dict[str, str]:
        """Get headers for a specific API key."""
        return {
            "Content-Type": "application/json",
            "x-goog-api-key": api_key
        }
    
    def _load_schema(self) -> Dict[str, Any]:
        """Load the JSON schema for response validation."""
        return {
            "type": "object",
            "properties": {
                "topics": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": [
                            "id", "title", "description", "category", "subcategory", "company",
                            "technologies", "complexity_level", "tags", "related_topics",
                            "metrics", "implementation_details", "learning_objectives",
                            "difficulty", "estimated_read_time", "prerequisites",
                            "created_date", "updated_date"
                        ],
                        "properties": {
                            "id": {"type": "integer"},
                            "title": {"type": "string"},
                            "description": {"type": "string", "minLength": 40, "maxLength": 5000},
                            "category": {
                                "type": "string",
                                "enum": [
                                    "big_tech_companies", "databases", "system_design", "cloud_infrastructure",
                                    "security", "ai_ml", "networking", "algorithms", "messaging_streaming"
                                ]
                            },
                            "subcategory": {"type": "string"},
                            "company": {"type": "string", "pattern": "^[a-z0-9_.\\-/]+$"},
                            "technologies": {"type": "array", "minItems": 3, "items": {"type": "string"}},
                            "complexity_level": {
                                "type": "string",
                                "enum": ["beginner", "intermediate", "advanced", "expert"]
                            },
                            "tags": {"type": "array", "minItems": 3, "items": {"type": "string"}},
                            "related_topics": {
                                "type": "array", "minItems": 2, "maxItems": 3, "items": {"type": "integer"}
                            },
                            "metrics": {
                                "type": "object",
                                "required": ["scale", "performance", "reliability", "latency"],
                                "properties": {
                                    "scale": {"type": "string"},
                                    "performance": {"type": "string"},
                                    "reliability": {"type": "string"},
                                    "latency": {"type": "string"}
                                }
                            },
                            "implementation_details": {
                                "type": "object",
                                "required": ["architecture", "scaling", "storage", "caching", "monitoring"],
                                "properties": {
                                    "architecture": {"type": "string"},
                                    "scaling": {"type": "string"},
                                    "storage": {"type": "string"},
                                    "caching": {"type": "string"},
                                    "monitoring": {"type": "string"}
                                }
                            },
                            "learning_objectives": {
                                "type": "array", "minItems": 3, "items": {"type": "string"}
                            },
                            "difficulty": {"type": "integer", "minimum": 1, "maximum": 10},
                            "estimated_read_time": {"type": "string", "pattern": "^[0-9]+(\\.[0-9]+)? (minute|minutes|hour|hours)$"},
                            "prerequisites": {"type": "array", "minItems": 2, "items": {"type": "string"}},
                            "created_date": {"type": "string", "format": "date"},
                            "updated_date": {"type": "string", "format": "date"}
                        }
                    }
                }
            }
        }
    
    def _get_system_instruction(self) -> str:
        """Get the system instruction for Gemini."""
        return """You are an expert system architect and technical writer specializing in large-scale distributed systems, databases, cloud infrastructure, and modern software engineering.

Your job:
- For each input topic, produce one JSON object that strictly follows the provided JSON Schema.
- Do NOT include prose, markdown, code fences, comments, or explanations—return JSON only.
- Use realistic, industry-standard values and reference real companies/tech where relevant.
- Keep descriptions concise (2–3 sentences, max 500 characters).
- Use lowercase snake_case for `company` (single company name only, no commas or "n/a" - examples: "google", "microsoft", "aws", "three.js_community").
- Choose the most appropriate `category` from the allowed enum.
- Set `complexity_level` to one of: beginner, intermediate, advanced, expert.
- `difficulty` must be an integer 1–10 aligned with complexity.
- `estimated_read_time` must be in format "X minutes" or "X.Y hours" (e.g., "15 minutes", "1.5 hours", "1 hour").
- `related_topics` must contain 2–3 distinct integer IDs (not including the topic's own id), preferably from the provided `all_topic_ids`.
- Dates must be ISO `YYYY-MM-DD`. Use the supplied `created_date` and `updated_date`.
- Return a JSON object with a "topics" array containing all generated topics."""
    
    def _build_user_prompt(self, topics: List[Dict[str, Any]], all_topic_ids: List[int], 
                          created_date: str, updated_date: str) -> str:
        """Build the user prompt with topic data."""
        topics_json = json.dumps(topics)
        all_ids_json = json.dumps(all_topic_ids)
        
        return f"""You will receive:
        - `topics`: a list (1–5) of {{id, title}} pairs
        - `all_topic_ids`: all IDs available for cross-linking
        - `created_date` and `updated_date` strings (YYYY-MM-DD)

Instructions:
For each topic in `topics`, generate one JSON object following the schema.
Return a JSON object with a "topics" array containing all generated topics.
Return JSON ONLY.

Input:
topics: {topics_json}
all_topic_ids: {all_ids_json}
created_date: "{created_date}"
updated_date: "{updated_date}" """
    
    def generate_topics(self, topics: List[Dict[str, Any]], all_topic_ids: List[int],
                       created_date: str = None, updated_date: str = None) -> Union[Dict, List[Dict]]:
        """Generate system design topics using Gemini 2.5 Flash.
        
        Args:
            topics: List of topic dicts with 'id' and 'title' keys
            all_topic_ids: All available topic IDs for cross-linking
            created_date: ISO date string (YYYY-MM-DD), defaults to today
            updated_date: ISO date string (YYYY-MM-DD), defaults to today
            
        Returns:
            Single dict (if one topic) or list of dicts (if multiple topics)
            
        Raises:
            requests.RequestException: If API call fails
            ValidationError: If response doesn't match schema
        """
        if not topics:
            raise ValueError("At least one topic required")
        
        if len(topics) > 5:
            raise ValueError("Maximum 5 topics per batch")
        
        # Set default dates
        today = datetime.now().strftime("%Y-%m-%d")
        created_date = created_date or today
        updated_date = updated_date or today
        
        # Build request payload
        payload = {
            "contents": [{
                "role": "user",
                "parts": [{"text": self._build_user_prompt(topics, all_topic_ids, created_date, updated_date)}]
            }],
            "generationConfig": {
                "responseMimeType": "application/json",
                "temperature": 0.2,
                "topP": 0.9,
                "responseSchema": self.schema
            },
            "systemInstruction": {
                "parts": [{"text": self._get_system_instruction()}]
            }
        }
        
        # Make API call with retry logic for rate limiting
        max_retries = len(self.api_keys)
        last_error = None
        
        for attempt in range(max_retries):
            with self._acquire_api_key() as api_key:
                try:
                    response = requests.post(
                        f"{self.base_url}?key={api_key}",
                        headers=self._get_headers(api_key),
                        json=payload,
                        timeout=300
                    )
                    
                    if response.ok:
                        break
                    elif response.status_code == 429:  # Rate limited
                        print("Rate limited, rotating API key...")
                        if attempt < max_retries - 1:
                            continue
                    else:
                        raise requests.RequestException(f"API call failed: {response.status_code} - {response.text}")
                        
                except requests.RequestException as e:
                    last_error = e
                    if attempt < max_retries - 1:
                        print("Request failed, rotating API key...")
                        print(e)
                        continue
                    else:
                        raise last_error
        
        if not response.ok:
            raise requests.RequestException(f"API call failed after {max_retries} attempts: {response.status_code} - {response.text}")
        
        # Parse response
        result = response.json()
        
        if 'candidates' not in result or not result['candidates']:
            raise ValueError("No candidates in response")
        
        content = result['candidates'][0]['content']['parts'][0]['text']
        
        try:
            parsed_content = json.loads(content)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in response: {e}")
        
        # Validate against schema
        try:
            validate(parsed_content, self.schema)
        except ValidationError as e:
            raise ValidationError(f"Response validation failed: {e}")
        
        # Extract topics from the response
        if 'topics' in parsed_content:
            topics = parsed_content['topics']
            # Return single topic if only one, otherwise return list
            if len(topics) == 1:
                return topics[0]
            else:
                return topics
        else:
            raise ValueError("Response missing 'topics' field")


def main():
    """Example usage of the GeminiClient."""
    # Example topics
    topics = [
        {"id": 101, "title": "How WhatsApp Group Calls Scale to Dozens"},
        {"id": 102, "title": "How Redis Internally Works"}
    ]
    all_topic_ids = [101, 102, 103, 104, 105]
    
    try:
        client = GeminiClient()
        result = client.generate_topics(topics, all_topic_ids)
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
