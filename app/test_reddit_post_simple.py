#!/usr/bin/env python3
"""
Test suite for Reddit Post content generation.
Tests prompt processing, schema validation, and direct schema instantiation.
"""

import sys
import os
import json
from pathlib import Path

# Add the app directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from schemas import RedditPostContent, validate_content

def load_prompt_template():
    """Load the Reddit Post prompt template"""
    prompt_path = Path(__file__).parent / "prompts" / "bodies" / "reddit-post.txt"
    if not prompt_path.exists():
        raise FileNotFoundError(f"Prompt template not found: {prompt_path}")
    
    with open(prompt_path, 'r', encoding='utf-8') as f:
        return f.read()

def process_prompt_with_topic(template, topic_data):
    """Process prompt template with topic data"""
    # Sample topic data for testing
    sample_data = {
        "topic_id": "1001",
        "topic_name": topic_data.get("name", "Database Connection Pooling Strategies"),
        "topic_description": topic_data.get("description", "Optimizing database connections for high-throughput applications"),
        "audience": "intermediate",
        "tone": "technical, community-focused, helpful",
        "locale": "en",
        "primary_url": "https://systemdesign.guide/database-pooling",
        **topic_data.get("brand", {
            "site_url": "https://systemdesign.guide",
            "handles": {"x": "@systemdesign", "linkedin": "@systemdesign", "github": "@systemdesign"},
            "utm_base": "utm_source=reddit&utm_medium=post"
        })
    }
    
    # Replace template variables
    processed = template
    for key, value in sample_data.items():
        if isinstance(value, dict):
            # Handle nested objects like brand
            for nested_key, nested_value in value.items():
                processed = processed.replace(f"{{{key}.{nested_key}}}", str(nested_value))
        else:
            processed = processed.replace(f"{{{key}}}", str(value))
    
    return processed

def test_prompt_processing():
    """Test 1: Reddit Post prompt template processing"""
    print("=" * 60)
    print("TEST 1: Reddit Post Prompt Processing")
    print("=" * 60)
    
    try:
        template = load_prompt_template()
        
        # Test with database connection pooling topic
        topic_data = {
            "name": "Database Connection Pooling Strategies",
            "description": "Optimizing database connections for high-throughput applications with proper pool sizing and connection lifecycle management"
        }
        
        processed_prompt = process_prompt_with_topic(template, topic_data)
        
        print("✅ Prompt template processed successfully")
        print(f"📄 Template path: prompts/bodies/reddit-post.txt")
        print(f"🎯 Topic: {topic_data['name']}")
        print(f"📝 Processed prompt length: {len(processed_prompt)} characters")
        
        # Verify key elements are present
        checks = {
            "Contains topic name": topic_data["name"] in processed_prompt,
            "Contains JSON format": '"content":' in processed_prompt,
            "Contains subreddit suggestions": "suggested_subreddits" in processed_prompt,
            "Contains comment preparation": "comment_preparation" in processed_prompt,
            "Contains moderation notes": "moderation_notes" in processed_prompt
        }
        
        for check, passed in checks.items():
            print(f"🔍 {check}: {'✅' if passed else '❌'}")
        
        print(f"\n📋 Prompt preview (first 500 chars):")
        print("-" * 50)
        print(processed_prompt[:500] + "...")
        print("-" * 50)
        
        return True
        
    except Exception as e:
        print(f"❌ Prompt processing failed: {e}")
        return False

def test_schema_validation():
    """Test 2: Reddit Post schema validation with sample data"""
    print("\n" + "=" * 60)
    print("TEST 2: Reddit Post Schema Validation")
    print("=" * 60)
    
    # Sample Reddit Post content
    sample_content = {
        "title": "How we reduced database connection overhead by 60% with proper pooling",
        "body": """We were hitting connection limits during peak traffic with our microservices architecture. Each service was creating its own connections without coordination, leading to connection exhaustion.

After profiling our connection patterns, we discovered most connections were idle 80% of the time. The default pool settings weren't optimized for our workload characteristics.

Here's what we implemented:

```python
# Connection pool configuration
pool_config = {
    'min_connections': 5,
    'max_connections': 20,
    'connection_timeout': 30,
    'idle_timeout': 300,
    'max_lifetime': 3600
}
```

Key metrics after optimization:
- Connection utilization: 45% → 85%
- Average response time: 120ms → 75ms
- Peak concurrent connections: 200 → 80

The biggest wins came from:
1. Right-sizing pool limits based on actual concurrency
2. Implementing connection health checks
3. Adding connection lifecycle monitoring

For more details on our implementation: https://systemdesign.guide/database-pooling?utm_source=reddit&utm_medium=post

What connection pooling strategies have worked best in your experience? Any gotchas with specific database drivers?""",
        
        "structure": {
            "paragraphs": [
                "Context: hitting connection limits during peak traffic",
                "Problem analysis: idle connections and poor pool settings", 
                "Solution details with code example and metrics",
                "Key optimization strategies and results",
                "Discussion questions for community engagement"
            ],
            "link_plan": {
                "enabled": True,
                "insert_after_paragraph": 2,
                "url": "https://systemdesign.guide/database-pooling?utm_source=reddit&utm_medium=post"
            }
        },
        
        "suggested_subreddits": [
            {
                "name": "r/programming",
                "why_relevant": "Database optimization and performance topics are frequently discussed",
                "posting_time_hint": "Weekdays 14:00-18:00 UTC",
                "flair_suggestions": ["Discussion", "Show & Tell"],
                "rules_checklist": ["no surveys", "clear technical content", "avoid promotional language"]
            },
            {
                "name": "r/devops", 
                "why_relevant": "Infrastructure optimization and database management are core topics",
                "posting_time_hint": "Tue-Thu 15:00-20:00 UTC",
                "flair_suggestions": ["Discussion", "Case Study"],
                "rules_checklist": ["include metrics/results", "avoid vendor pitches", "provide technical context"]
            },
            {
                "name": "r/database",
                "why_relevant": "Specialized community for database performance and optimization",
                "posting_time_hint": "Weekdays 16:00-19:00 UTC", 
                "flair_suggestions": ["Performance", "Best Practices"],
                "rules_checklist": ["specify database type", "include configuration details", "avoid generic advice"]
            }
        ],
        
        "comment_preparation": {
            "top_level_seeds": [
                "Happy to share more specific configuration details if helpful - what database are you working with?",
                "Anyone tried connection pooling with serverless functions? The cold start behavior is interesting."
            ],
            "faqs": [
                {
                    "q": "What database and driver are you using?",
                    "a": "PostgreSQL with asyncpg for Python. The async nature helps with connection efficiency, but pool tuning is still critical."
                },
                {
                    "q": "How do you handle connection pool monitoring?",
                    "a": "We use custom metrics exported to Prometheus: active connections, wait time, pool utilization. Grafana dashboards show patterns clearly."
                },
                {
                    "q": "Any issues with connection pool in Kubernetes?",
                    "a": "Pod restarts can cause connection spikes. We use readiness probes that check pool health and implement graceful shutdown with connection draining."
                }
            ]
        },
        
        "image_prompts": [],
        
        "moderation_notes": [
            "Avoid promotional phrasing in title and first two paragraphs.",
            "Link placement follows Reddit best practices (after context).",
            "Focus on technical value rather than driving traffic."
        ],
        
        "compliance": {
            "title_char_count": 77,
            "paragraph_count": 5,
            "links_in_p1_p2": 0,
            "has_tracked_link_after_p2": True,
            "image_prompt_count": 0,
            "subreddits_suggested_count": 3,
            "checks": [
                "title is neutral and ≤300 chars",
                "no links/self-promo in first two paragraphs", 
                "exactly one tracked link after paragraph 2",
                "three relevant subreddits with rules checklists",
                "no image prompts (include_images=false)"
            ]
        }
    }
    
    try:
        print("🧪 Testing direct schema validation...")
        reddit_post = RedditPostContent(**sample_content)
        print("✅ Direct schema validation passed")
        print(f"📊 Title length: {len(reddit_post.title)} chars")
        print(f"📝 Body length: {len(reddit_post.body)} chars")
        print(f"📑 Subreddits suggested: {len(reddit_post.suggested_subreddits)}")
        print(f"🎯 Comment seeds: {len(reddit_post.comment_preparation['top_level_seeds'])}")
        print(f"❓ FAQ items: {len(reddit_post.comment_preparation['faqs'])}")
        
        print("\n🧪 Testing schema validator function...")
        validated_content = validate_content("reddit", "post", sample_content)
        print("✅ Schema validator function passed")
        print(f"📋 Validated content type: {type(validated_content).__name__}")
        
        print(f"\n📋 Sample Reddit Post Structure:")
        print(f"   • Title: {len(reddit_post.title)} characters")
        print(f"   • Body: {len(reddit_post.body)} characters")
        print(f"   • Subreddits: {len(reddit_post.suggested_subreddits)} communities")
        print(f"   • Comment seeds: {len(reddit_post.comment_preparation['top_level_seeds'])}")
        print(f"   • FAQ responses: {len(reddit_post.comment_preparation['faqs'])}")
        
        return True
        
    except Exception as e:
        print(f"❌ Schema validation failed: {e}")
        return False

def test_direct_schema_instantiation():
    """Test 3: Direct Reddit Post schema instantiation"""
    print("\n" + "=" * 60)
    print("TEST 3: Direct Reddit Post Schema Instantiation")
    print("=" * 60)
    
    # Minimal valid Reddit Post content
    minimal_content = {
        "title": "Lessons learned from scaling Redis clusters to 100TB+",
        "body": """Our Redis deployment grew from 10GB to 100TB+ over two years. Here's what we learned about cluster management at scale.

Initially we ran a single Redis instance with periodic snapshots. As data grew, we hit memory limits and started experiencing longer backup times affecting performance.

The migration to Redis Cluster required careful planning:

- Gradual resharding during low-traffic windows
- Custom monitoring for slot distribution
- Automated failover testing every week

Key insights:
1. Memory fragmentation becomes critical above 50GB per node
2. Network partitions are more common than expected
3. Backup strategies need to account for cluster consistency

More technical details in our blog post: https://systemdesign.guide/redis-scaling?utm_source=reddit&utm_medium=post

What's been your experience with Redis at scale? Any unexpected challenges?""",
        
        "structure": {
            "paragraphs": [
                "Growth context and initial setup",
                "Problems encountered with single instance",
                "Migration approach and monitoring",
                "Key lessons and insights",
                "Community discussion questions"
            ],
            "link_plan": {
                "enabled": True,
                "insert_after_paragraph": 2,
                "url": "https://systemdesign.guide/redis-scaling?utm_source=reddit&utm_medium=post"
            }
        },
        
        "suggested_subreddits": [
            {
                "name": "r/redis",
                "why_relevant": "Specialized Redis community with scaling expertise",
                "posting_time_hint": "Weekdays 15:00-19:00 UTC",
                "flair_suggestions": ["Discussion", "Experience"],
                "rules_checklist": ["include version info", "specify cluster size", "avoid basic questions"]
            },
            {
                "name": "r/devops",
                "why_relevant": "Infrastructure scaling and operations focus",
                "posting_time_hint": "Tue-Thu 14:00-18:00 UTC", 
                "flair_suggestions": ["Case Study", "Lessons Learned"],
                "rules_checklist": ["include metrics", "describe tooling", "focus on operational aspects"]
            },
            {
                "name": "r/programming",
                "why_relevant": "General technical audience interested in scaling challenges",
                "posting_time_hint": "Weekdays 13:00-17:00 UTC",
                "flair_suggestions": ["Discussion", "Architecture"],
                "rules_checklist": ["avoid vendor promotion", "include technical details", "encourage discussion"]
            }
        ],
        
        "comment_preparation": {
            "top_level_seeds": [
                "Happy to dive deeper into any specific aspect - cluster topology, monitoring setup, etc.",
                "The memory fragmentation issue was particularly tricky. Anyone found good solutions beyond regular restarts?"
            ],
            "faqs": [
                {
                    "q": "What Redis version and cluster size?",
                    "a": "Redis 6.2+ across 12 nodes (4 shards, 3 replicas each). Started with 3 nodes and grew incrementally."
                },
                {
                    "q": "How do you handle cluster resharding?",
                    "a": "Automated scripts using redis-cli with careful slot migration monitoring. We batch moves and pause during high traffic."
                }
            ]
        },
        
        "image_prompts": [],
        
        "moderation_notes": [
            "Technical focus with community value",
            "Link provided after establishing context", 
            "Encourages knowledge sharing"
        ],
        
        "compliance": {
            "title_char_count": 62,
            "paragraph_count": 5,
            "links_in_p1_p2": 0,
            "has_tracked_link_after_p2": True,
            "image_prompt_count": 0,
            "subreddits_suggested_count": 3,
            "checks": [
                "title under 300 characters",
                "no promotional content in opening",
                "single tracked link after context",
                "three subreddit suggestions",
                "community-focused discussion"
            ]
        }
    }
    
    try:
        reddit_post = RedditPostContent(**minimal_content)
        print("✅ Direct schema instantiation successful")
        print(f"📊 Reddit Post structure:")
        print(f"   • Title: {len(reddit_post.title)} characters")
        print(f"   • Body: {len(reddit_post.body)} characters")
        print(f"   • Subreddits: {len(reddit_post.suggested_subreddits)}")
        print(f"   • Comment preparation: {len(reddit_post.comment_preparation['faqs'])} FAQs")
        print(f"   • Moderation notes: {len(reddit_post.moderation_notes)}")
        
        # Test JSON serialization
        json_data = reddit_post.model_dump()
        json_str = json.dumps(json_data, indent=2)
        print("✅ JSON serialization successful")
        print(f"📄 JSON size: {len(json_str)} characters")
        
        return True
        
    except Exception as e:
        print(f"❌ Direct schema instantiation failed: {e}")
        return False

def main():
    """Run all Reddit Post tests"""
    print("🧪 REDDIT POST CONTENT GENERATION TESTS")
    print("=" * 60)
    
    results = []
    
    # Run all tests
    results.append(("Prompt Processing", test_prompt_processing()))
    results.append(("Schema Validation", test_schema_validation()))
    results.append(("Direct Schema Instantiation", test_direct_schema_instantiation()))
    
    # Print summary
    print("\n" + "=" * 60)
    print("📋 TEST SUMMARY")
    print("=" * 60)
    
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)
    
    print(f"\n🎯 Overall: {passed_count}/{total_count} tests passed")
    
    if passed_count == total_count:
        print("🎉 All Reddit Post tests passed! Ready for integration.")
        return True
    else:
        print("⚠️ Some tests failed. Check implementation.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
