#!/usr/bin/env python3
"""
Simple test script for X Twitter Thread content generation.
Tests prompt processing, schema validation, and direct schema instantiation.
"""

import sys
import os
import json
from pathlib import Path

# Add the app directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from prompt_processor import PromptProcessor
from schemas import XTwitterThreadContent, validate_content_schema

def test_prompt_processing():
    """Test X Twitter Thread prompt template processing"""
    print("=" * 60)
    print("TEST 1: X Twitter Thread Prompt Processing")
    print("=" * 60)
    
    try:
        processor = PromptProcessor()
        
        # Test data
        topic_id = "1001"
        topic_name = "Database Sharding Strategies"
        topic_description = "Comprehensive guide to horizontal database partitioning techniques, including range-based, hash-based, and directory-based sharding approaches for scaling distributed systems."
        
        # Process the prompt template
        prompt_path = "prompts/bodies/x-twitter-thread.txt"
        processed_prompt = processor.process_prompt_template(
            template_path=prompt_path,
            topic_id=topic_id,
            topic_name=topic_name,
            topic_description=topic_description,
            platform="x_twitter",
            format_type="thread"
        )
        
        print(f"✅ Prompt template processed successfully")
        print(f"📄 Template path: {prompt_path}")
        print(f"🎯 Topic: {topic_name}")
        print(f"📝 Processed prompt length: {len(processed_prompt)} characters")
        print(f"🔍 Contains topic name: {'✅' if topic_name in processed_prompt else '❌'}")
        print(f"🔍 Contains JSON format: {'✅' if 'tweets' in processed_prompt else '❌'}")
        
        # Show first 500 characters of processed prompt
        print(f"\n📋 Prompt preview (first 500 chars):")
        print("-" * 50)
        print(processed_prompt[:500] + "..." if len(processed_prompt) > 500 else processed_prompt)
        print("-" * 50)
        
        return True
        
    except Exception as e:
        print(f"❌ Prompt processing failed: {str(e)}")
        return False

def test_schema_validation():
    """Test X Twitter Thread schema validation with sample data"""
    print("\n" + "=" * 60)
    print("TEST 2: X Twitter Thread Schema Validation")
    print("=" * 60)
    
    # Sample X Twitter Thread content matching the new schema
    sample_content = {
        "tweets": [
            {
                "position": 1,
                "content": "🧵 Database sharding is the secret weapon behind every scalable system. Here's how the giants like Twitter, Instagram, and Netflix handle billions of requests daily (1/7)",
                "character_count": 168,
                "has_hook": True,
                "includes_thread_indicator": True
            },
            {
                "position": 2,
                "content": "What is sharding? Think of it as splitting your massive database table across multiple servers. Instead of one server struggling with 100M users, you have 10 servers each handling 10M users. 📊",
                "character_count": 195,
                "has_hook": False,
                "includes_thread_indicator": False
            },
            {
                "position": 3,
                "content": "🔑 Range-based sharding: Split data by ranges (A-M users on Server 1, N-Z on Server 2). Simple but can create hotspots if your data isn't evenly distributed.",
                "character_count": 156,
                "has_hook": False,
                "includes_thread_indicator": False
            },
            {
                "position": 4,
                "content": "⚡ Hash-based sharding: Use a hash function to distribute data evenly. More complex but prevents hotspots. This is what most big tech companies use.",
                "character_count": 148,
                "has_hook": False,
                "includes_thread_indicator": False
            },
            {
                "position": 5,
                "content": "🗂️ Directory-based sharding: Keep a lookup service that knows where each piece of data lives. Flexible but adds complexity and a potential single point of failure.",
                "character_count": 167,
                "has_hook": False,
                "includes_thread_indicator": False
            }
        ],
        "engagement_tweet": {
            "content": "Which sharding strategy does your team use? Drop a comment with your experience - especially any gotchas you've encountered! 👇",
            "character_count": 126,
            "engagement_type": "question",
            "call_to_action": "comment"
        },
        "hashtags": [
            "#DatabaseSharding",
            "#SystemDesign",
            "#ScalableArchitecture",
            "#DistributedSystems",
            "#TechArchitecture",
            "#DatabaseDesign",
            "#BackendEngineering",
            "#SoftwareEngineering",
            "#TechLeadership",
            "#DevOps"
        ],
        "mention_suggestions": [
            "@martinfowler",
            "@kelseyhightower",
            "@copyconstruct",
            "@mitchellh"
        ],
        "tweet_media_plan": [
            {
                "tweet_position": 1,
                "media_type": "image",
                "description": "Thread overview infographic",
                "required": True
            },
            {
                "tweet_position": 3,
                "media_type": "diagram",
                "description": "Range-based sharding visualization",
                "required": False
            },
            {
                "tweet_position": 4,
                "media_type": "diagram",
                "description": "Hash-based sharding flow",
                "required": False
            }
        ],
        "image_prompts": [
            {
                "position": 1,
                "prompt": "Clean infographic showing database sharding concept with multiple servers and data distribution, professional tech style, blue and white color scheme",
                "style": "infographic",
                "dimensions": "1200x675"
            },
            {
                "position": 2,
                "prompt": "Technical diagram showing range-based vs hash-based sharding comparison, clean lines, professional visualization",
                "style": "diagram",
                "dimensions": "1200x675"
            }
        ],
        "compliance": {
            "total_tweets": 5,
            "engagement_tweet_included": True,
            "character_counts_valid": True,
            "hashtag_count": 10,
            "mention_count": 4,
            "thread_structure_valid": True,
            "hook_strength": "strong",
            "cta_included": True
        }
    }
    
    try:
        # Test direct schema validation
        print("🧪 Testing direct schema validation...")
        thread_content = XTwitterThreadContent(**sample_content)
        print(f"✅ Direct schema validation passed")
        print(f"📊 Tweets count: {len(thread_content.tweets)}")
        print(f"🏷️ Hashtags count: {len(thread_content.hashtags)}")
        print(f"👥 Mentions count: {len(thread_content.mention_suggestions)}")
        print(f"🖼️ Image prompts count: {len(thread_content.image_prompts)}")
        
        # Test schema validator function
        print(f"\n🧪 Testing schema validator function...")
        validated_content = validate_content_schema('x_twitter', 'thread', sample_content)
        print(f"✅ Schema validator function passed")
        print(f"📋 Validated content type: {type(validated_content).__name__}")
        
        # Display sample content structure
        print(f"\n📋 Sample X Twitter Thread Structure:")
        print(f"   • Tweets: {len(sample_content['tweets'])} tweets")
        print(f"   • Engagement tweet: {sample_content['engagement_tweet']['engagement_type']}")
        print(f"   • Hashtags: {len(sample_content['hashtags'])} professional tags")
        print(f"   • Mentions: {len(sample_content['mention_suggestions'])} suggested handles")
        print(f"   • Media plan: {len(sample_content['tweet_media_plan'])} media attachments")
        print(f"   • Image prompts: {len(sample_content['image_prompts'])} visual assets")
        
        return True
        
    except Exception as e:
        print(f"❌ Schema validation failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_direct_schema_instantiation():
    """Test direct instantiation of X Twitter Thread schema"""
    print("\n" + "=" * 60)
    print("TEST 3: Direct X Twitter Thread Schema Instantiation")
    print("=" * 60)
    
    try:
        # Create X Twitter Thread content directly
        thread_content = XTwitterThreadContent(
            tweets=[
                {
                    "position": 1,
                    "content": "🧵 Microservices vs Monoliths: The eternal debate. Here's what 5 years of building both taught me (1/6)",
                    "character_count": 115,
                    "has_hook": True,
                    "includes_thread_indicator": True
                },
                {
                    "position": 2,
                    "content": "Monoliths aren't evil. They're actually perfect for small teams and early-stage products. Simple deployment, easier debugging, faster development cycles.",
                    "character_count": 154,
                    "has_hook": False,
                    "includes_thread_indicator": False
                },
                {
                    "position": 3,
                    "content": "But as you scale, monoliths become bottlenecks. One bug can bring down everything. One team's slow release blocks everyone else's features.",
                    "character_count": 144,
                    "has_hook": False,
                    "includes_thread_indicator": False
                },
                {
                    "position": 4,
                    "content": "Microservices solve this by isolating failures and enabling independent deployments. But they introduce network complexity, data consistency challenges, and operational overhead.",
                    "character_count": 175,
                    "has_hook": False,
                    "includes_thread_indicator": False
                },
                {
                    "position": 5,
                    "content": "The sweet spot? Start with a modular monolith. Extract services only when you have clear boundaries and dedicated teams to own them. Architecture follows organization.",
                    "character_count": 170,
                    "has_hook": False,
                    "includes_thread_indicator": False
                }
            ],
            engagement_tweet={
                "content": "What's your experience? Monolith or microservices? Share your war stories below! 👇",
                "character_count": 86,
                "engagement_type": "question",
                "call_to_action": "share experience"
            },
            hashtags=[
                "#Microservices",
                "#SystemDesign",
                "#SoftwareArchitecture",
                "#TechLeadership",
                "#DistributedSystems",
                "#Monolith",
                "#ScalableArchitecture",
                "#DevOps",
                "#TechStrategy"
            ],
            mention_suggestions=[
                "@martinfowler",
                "@samuelgoto",
                "@kelseyhightower"
            ],
            tweet_media_plan=[
                {
                    "tweet_position": 1,
                    "media_type": "infographic",
                    "description": "Monolith vs Microservices comparison chart",
                    "required": True
                }
            ],
            image_prompts=[
                {
                    "position": 1,
                    "prompt": "Professional comparison infographic showing monolith vs microservices architecture, clean design, tech colors",
                    "style": "infographic",
                    "dimensions": "1200x675"
                }
            ],
            compliance={
                "total_tweets": 5,
                "engagement_tweet_included": True,
                "character_counts_valid": True,
                "hashtag_count": 9,
                "mention_count": 3,
                "thread_structure_valid": True,
                "hook_strength": "strong",
                "cta_included": True
            }
        )
        
        print(f"✅ Direct schema instantiation successful")
        print(f"📊 Thread structure:")
        print(f"   • Total tweets: {len(thread_content.tweets)}")
        print(f"   • Engagement tweet type: {thread_content.engagement_tweet['engagement_type']}")
        print(f"   • Hashtags: {len(thread_content.hashtags)}")
        print(f"   • Mention suggestions: {len(thread_content.mention_suggestions)}")
        print(f"   • Media plan items: {len(thread_content.tweet_media_plan)}")
        print(f"   • Image prompts: {len(thread_content.image_prompts)}")
        
        # Test JSON serialization
        json_output = thread_content.model_dump()
        print(f"✅ JSON serialization successful")
        print(f"📄 JSON size: {len(json.dumps(json_output))} characters")
        
        return True
        
    except Exception as e:
        print(f"❌ Direct schema instantiation failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all X Twitter Thread tests"""
    print("🧪 X TWITTER THREAD CONTENT GENERATION TESTS")
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
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All X Twitter Thread tests passed! Ready for integration.")
    else:
        print("⚠️ Some tests failed. Please review the errors above.")
    
    return passed == len(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)