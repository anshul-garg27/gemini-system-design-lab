#!/usr/bin/env python3
"""
Test suite for Hacker News Item content generation.
Tests prompt processing, schema validation, and direct schema instantiation.
"""

import sys
import os
import json
from pathlib import Path

# Add the app directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from schemas import HackerNewsItemContent, validate_content

def load_prompt_template():
    """Load the Hacker News Item prompt template"""
    prompt_path = Path(__file__).parent / "prompts" / "bodies" / "hacker-news-item.txt"
    if not prompt_path.exists():
        raise FileNotFoundError(f"Prompt template not found: {prompt_path}")
    
    with open(prompt_path, 'r', encoding='utf-8') as f:
        return f.read()

def process_prompt_with_topic(template, topic_data):
    """Process prompt template with topic data"""
    # Sample topic data for testing
    sample_data = {
        "topic_id": "2001",
        "topic_name": topic_data.get("name", "Distributed Rate Limiting at Scale"),
        "topic_description": topic_data.get("description", "Building a distributed rate limiter that handles 1M+ requests per second"),
        "audience": "advanced",
        "tone": "neutral",
        "locale": "en",
        "primary_url": "https://engineering.example.com/distributed-rate-limiting",
        **topic_data.get("brand", {
            "site_url": "https://engineering.example.com"
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
    """Test 1: Hacker News Item prompt template processing"""
    print("=" * 60)
    print("TEST 1: Hacker News Item Prompt Processing")
    print("=" * 60)
    
    try:
        template = load_prompt_template()
        
        # Test with distributed rate limiting topic
        topic_data = {
            "name": "Distributed Rate Limiting at Scale",
            "description": "Building a distributed rate limiter that handles 1M+ requests per second with sub-millisecond latency"
        }
        
        processed_prompt = process_prompt_with_topic(template, topic_data)
        
        print("✅ Prompt template processed successfully")
        print(f"📄 Template path: prompts/bodies/hacker-news-item.txt")
        print(f"🎯 Topic: {topic_data['name']}")
        print(f"📝 Processed prompt length: {len(processed_prompt)} characters")
        
        # Verify key elements are present
        checks = {
            "Contains topic name": topic_data["name"] in processed_prompt,
            "Contains JSON format": '"content":' in processed_prompt,
            "Contains Show HN variant": "show_hn_variant" in processed_prompt,
            "Contains comment preparation": "comment_preparation" in processed_prompt,
            "Contains compliance rules": "compliance" in processed_prompt,
            "No tracking params rule": "no tracking" in processed_prompt.lower()
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
    """Test 2: Hacker News Item schema validation with sample data"""
    print("\n" + "=" * 60)
    print("TEST 2: Hacker News Item Schema Validation")
    print("=" * 60)
    
    # Sample Hacker News Item content (regular submission)
    sample_content = {
        "title": "How we built a distributed rate limiter handling 1M+ RPS",
        "summary": "We needed to rate limit API requests across 50+ edge nodes with consistent limits. Our solution uses Redis Cluster with Lua scripts and achieves p99 latency under 2ms. The system has been running in production for 8 months handling peak loads of 1.2M requests per second.",
        "link": "https://engineering.example.com/distributed-rate-limiting",
        "text_post": "",
        "is_show_hn": False,
        
        "show_hn_variant": {
            "title": "Show HN: Distributed rate limiter with sub-2ms p99 latency",
            "blurb": "A Redis-based rate limiter that scales to 1M+ RPS across distributed nodes. Built for API gateways that need consistent rate limiting without central bottlenecks.",
            "setup": "Clone the repo, run `docker-compose up`, and send requests to localhost:8080/api/test. The demo shows rate limiting in action with real-time metrics at localhost:3000/dashboard.",
            "demo_url": "https://ratelimit-demo.example.com",
            "repo_url": "https://github.com/example/distributed-ratelimiter",
            "license": "MIT",
            "stack": ["Go", "Redis Cluster", "Docker", "Prometheus"],
            "metrics": [
                {"name": "p99 latency", "value": "1.8", "unit": "ms"},
                {"name": "throughput", "value": "1200000", "unit": "RPS"},
                {"name": "memory per node", "value": "256", "unit": "MB"}
            ],
            "limitations": [
                "Requires Redis Cluster (minimum 3 nodes)",
                "Clock skew between nodes can affect accuracy by ~1%",
                "No built-in rate limit rule hot-reloading yet"
            ],
            "request_for_feedback": [
                "Performance feedback on different Redis configurations",
                "Ideas for handling network partitions gracefully"
            ]
        },
        
        "comment_preparation": {
            "anticipated_questions": [
                {
                    "q": "How does this compare to nginx rate limiting?",
                    "a": "nginx rate limiting is per-instance, so you get inconsistent limits across a load balancer. Our solution provides global rate limiting with shared state via Redis. Trade-off is added latency (1-2ms) vs nginx's ~0.1ms, but you get true distributed limits."
                },
                {
                    "q": "What are the performance characteristics?",
                    "a": "p50: 0.8ms, p95: 1.4ms, p99: 1.8ms. Tested on c5.2xlarge instances with Redis Cluster on r5.large nodes. Throughput scales linearly with Redis nodes up to network limits."
                },
                {
                    "q": "Security/privacy?",
                    "a": "Rate limit keys are hashed SHA-256. No request content is stored, only counters and timestamps. Redis auth enabled, TLS in transit. Data retention is configurable (default 1 hour for expired keys)."
                }
            ],
            "benchmarks_detail": "Load testing with wrk on c5.2xlarge (8 vCPU, 16GB RAM). Redis Cluster: 3x r5.large nodes. Dataset: 100K unique API keys, zipfian distribution. 10-minute sustained load tests, 5 runs averaged.",
            "alternatives": ["nginx rate_limit_req", "Envoy rate limiting", "Kong rate limiting", "AWS API Gateway throttling"],
            "roadmap_next": ["Hot-reload rate limit rules", "Prometheus metrics export", "Multi-region replication"]
        },
        
        "moderation_notes": [
            "No tracking parameters in any URL.",
            "Technical focus with concrete numbers and limitations.",
            "Ready to discuss implementation details and trade-offs.",
            "Disclose that this is our production system."
        ],
        
        "compliance": {
            "title_char_count": 58,
            "summary_sentence_count": 3,
            "has_tracking_params": False,
            "is_text_post": False,
            "is_show_hn_complete": True,
            "includes_metrics": True,
            "includes_limitations": True,
            "checks": [
                "title ≤80 chars; no emojis/clickbait",
                "summary has 3 sentences with concrete numbers",
                "URL is canonical with no tracking parameters",
                "Show HN variant complete with demo/repo/stack/limitations",
                "Technical comment prep with benchmarks/alternatives/roadmap"
            ]
        }
    }
    
    try:
        print("🧪 Testing direct schema validation...")
        hn_item = HackerNewsItemContent(**sample_content)
        print("✅ Direct schema validation passed")
        print(f"📊 Title length: {len(hn_item.title)} chars")
        print(f"📝 Summary sentences: {len(hn_item.summary.split('.'))-1}")
        print(f"🔗 Has link: {'Yes' if hn_item.link else 'No'}")
        print(f"🎯 Show HN ready: {'Yes' if hn_item.show_hn_variant else 'No'}")
        print(f"📈 Metrics count: {len(hn_item.show_hn_variant.get('metrics', []))}")
        
        print("\n🧪 Testing schema validator function...")
        validated_content = validate_content("hacker_news", "item", sample_content)
        print("✅ Schema validator function passed")
        print(f"📋 Validated content type: {type(validated_content).__name__}")
        
        print(f"\n📋 Sample Hacker News Item Structure:")
        print(f"   • Title: {len(hn_item.title)} characters")
        print(f"   • Summary: {len(hn_item.summary)} characters")
        print(f"   • Link: {hn_item.link[:50]}..." if hn_item.link else "   • Link: None")
        print(f"   • Show HN variant: Complete")
        print(f"   • Comment prep: {len(hn_item.comment_preparation['anticipated_questions'])} Q&As")
        
        return True
        
    except Exception as e:
        print(f"❌ Schema validation failed: {e}")
        return False

def test_direct_schema_instantiation():
    """Test 3: Direct Hacker News Item schema instantiation (Show HN variant)"""
    print("\n" + "=" * 60)
    print("TEST 3: Direct Hacker News Item Schema Instantiation (Show HN)")
    print("=" * 60)
    
    # Show HN example
    show_hn_content = {
        "title": "Show HN: Real-time collaborative code editor in 500 lines",
        "summary": "Built a collaborative code editor using WebRTC for peer-to-peer sync. No server required after initial handshake. Supports 8+ simultaneous users with conflict resolution via operational transforms.",
        "link": "",
        "text_post": "I wanted to build a collaborative editor without requiring a backend server for the actual collaboration. After the initial WebRTC handshake via a simple signaling server, all editing happens peer-to-peer.\n\nThe core challenge was conflict resolution when multiple people edit simultaneously. I implemented operational transforms (OT) which ensures all peers converge to the same document state regardless of network delays.\n\nTry it at https://p2p-editor.dev - open the same room URL in multiple tabs to see real-time collaboration. The entire editor is under 500 lines of vanilla JavaScript.",
        "is_show_hn": True,
        
        "show_hn_variant": {
            "title": "Show HN: Real-time collaborative code editor in 500 lines",
            "blurb": "A peer-to-peer collaborative code editor using WebRTC. No backend server needed for collaboration after initial handshake.",
            "setup": "Visit https://p2p-editor.dev, create a room, share the URL with collaborators. Open in multiple browser tabs to test locally.",
            "demo_url": "https://p2p-editor.dev",
            "repo_url": "https://github.com/example/p2p-editor",
            "license": "MIT",
            "stack": ["Vanilla JavaScript", "WebRTC", "Operational Transforms", "CodeMirror"],
            "metrics": [
                {"name": "bundle size", "value": "45", "unit": "KB"},
                {"name": "max users tested", "value": "12", "unit": "users"},
                {"name": "sync latency", "value": "50", "unit": "ms"}
            ],
            "limitations": [
                "Requires modern browser with WebRTC support",
                "No persistence - documents lost when all users leave",
                "Signaling server needed for initial peer discovery"
            ],
            "request_for_feedback": [
                "Performance with larger documents (>10K lines)",
                "Ideas for adding persistence without a backend"
            ]
        },
        
        "comment_preparation": {
            "anticipated_questions": [
                {
                    "q": "How does this compare to VS Code Live Share?",
                    "a": "VS Code Live Share requires Microsoft's servers and VS Code. This works in any browser and is fully peer-to-peer after handshake. Trade-off is less features but much simpler architecture."
                },
                {
                    "q": "What happens when someone goes offline?",
                    "a": "Other peers continue collaborating. When the offline user reconnects, they get the latest document state. No data is lost as long as at least one peer stays online."
                },
                {
                    "q": "Security concerns with P2P?",
                    "a": "All WebRTC connections are encrypted. Document content never touches our servers after the initial handshake. Users should only share room URLs with trusted collaborators."
                }
            ],
            "benchmarks_detail": "Tested on Chrome/Firefox with 2-12 concurrent users. Latency measured as time from keystroke to remote display. Bundle size measured with gzip compression.",
            "alternatives": ["VS Code Live Share", "Google Docs", "Figma", "Notion", "CodePen Collab Mode"],
            "roadmap_next": ["Document persistence via IPFS", "Voice chat integration", "Mobile browser support"]
        },
        
        "moderation_notes": [
            "This is my personal project built over weekends.",
            "Demo URL has no tracking or analytics.",
            "Open to technical feedback and collaboration.",
            "Code is MIT licensed for community use."
        ],
        
        "compliance": {
            "title_char_count": 59,
            "summary_sentence_count": 3,
            "has_tracking_params": False,
            "is_text_post": True,
            "is_show_hn_complete": True,
            "includes_metrics": True,
            "includes_limitations": True,
            "checks": [
                "Show HN title ≤80 chars",
                "text_post explains what it is and how to try it",
                "demo_url and repo_url provided without tracking",
                "stack, metrics, and limitations documented",
                "technical comment preparation complete"
            ]
        }
    }
    
    try:
        hn_item = HackerNewsItemContent(**show_hn_content)
        print("✅ Direct schema instantiation successful")
        print(f"📊 Hacker News Item structure:")
        print(f"   • Title: {len(hn_item.title)} characters")
        print(f"   • Summary: {len(hn_item.summary)} characters")
        print(f"   • Text post: {len(hn_item.text_post)} characters")
        print(f"   • Show HN: {hn_item.is_show_hn}")
        print(f"   • Demo URL: {hn_item.show_hn_variant.get('demo_url', 'None')}")
        print(f"   • Metrics: {len(hn_item.show_hn_variant.get('metrics', []))}")
        print(f"   • Limitations: {len(hn_item.show_hn_variant.get('limitations', []))}")
        
        # Test JSON serialization
        json_data = hn_item.model_dump()
        json_str = json.dumps(json_data, indent=2)
        print("✅ JSON serialization successful")
        print(f"📄 JSON size: {len(json_str)} characters")
        
        return True
        
    except Exception as e:
        print(f"❌ Direct schema instantiation failed: {e}")
        return False

def main():
    """Run all Hacker News Item tests"""
    print("🧪 HACKER NEWS ITEM CONTENT GENERATION TESTS")
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
        print("🎉 All Hacker News Item tests passed! Ready for integration.")
        return True
    else:
        print("⚠️ Some tests failed. Check implementation.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
