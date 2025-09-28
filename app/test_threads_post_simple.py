#!/usr/bin/env python3
"""
Simple test script for Threads Post content generation.
Tests prompt processing, schema validation, and direct schema instantiation.
"""

import sys
import os
import json
from pathlib import Path

# Add the app directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from prompt_processor import PromptProcessor
from schemas import ThreadsPostContent, validate_content

def test_prompt_processing():
    """Test Threads Post prompt template processing"""
    print("=" * 60)
    print("TEST 1: Threads Post Prompt Processing")
    print("=" * 60)
    
    try:
        processor = PromptProcessor()
        
        # Test data
        topic_id = "3001"
        topic_name = "Load Balancing Strategies"
        topic_description = "Comprehensive overview of load balancing algorithms including round-robin, weighted round-robin, least connections, and consistent hashing for distributing traffic across multiple servers in high-availability systems."
        
        # Process the prompt template
        prompt_path = "prompts/bodies/threads-post.txt"
        processed_prompt = processor.process_prompt_template(
            template_path=prompt_path,
            topic_id=topic_id,
            topic_name=topic_name,
            topic_description=topic_description,
            platform="threads",
            format_type="post"
        )
        
        print(f"✅ Prompt template processed successfully")
        print(f"📄 Template path: {prompt_path}")
        print(f"🎯 Topic: {topic_name}")
        print(f"📝 Processed prompt length: {len(processed_prompt)} characters")
        print(f"🔍 Contains topic name: {'✅' if topic_name in processed_prompt else '❌'}")
        print(f"🔍 Contains JSON format: {'✅' if 'reply_chain' in processed_prompt else '❌'}")
        print(f"🔍 Contains image prompts: {'✅' if 'image_prompts' in processed_prompt else '❌'}")
        print(f"🔍 Contains compliance rules: {'✅' if 'compliance' in processed_prompt else '❌'}")
        
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
    """Test Threads Post schema validation with sample data"""
    print("\n" + "=" * 60)
    print("TEST 2: Threads Post Schema Validation")
    print("=" * 60)
    
    # Sample Threads Post content matching the schema
    sample_content = {
        "post": "Ever wonder how Netflix handles 200M+ users without crashing? 🤔\n\nThe secret is smart load balancing.\n\nHere's how it works 👇",
        "alt_versions": [
            "200M Netflix users, zero downtime. The load balancing magic behind it all.",
            "Load balancing: the unsung hero keeping your favorite apps running 24/7."
        ],
        "reply_chain": [
            {
                "index": 2,
                "text": "Round-robin is the simplest approach 🔄\n\nRequest 1 → Server A\nRequest 2 → Server B\nRequest 3 → Server C\nRepeat.\n\nBut what if Server A is slower? #loadbalancing",
                "chars_count": 147,
                "mentions": [],
                "hashtags_inline": ["#loadbalancing"]
            },
            {
                "index": 3,
                "text": "That's where weighted algorithms shine ⚖️\n\nPowerful servers get more traffic.\nWeaker servers get less.\n\nResult: Better performance across the board.",
                "chars_count": 151,
                "mentions": [],
                "hashtags_inline": []
            },
            {
                "index": 4,
                "text": "Least connections is even smarter 🧠\n\nSends new requests to the server with fewest active connections.\n\nPerfect for long-running requests. #systemdesign",
                "chars_count": 156,
                "mentions": [],
                "hashtags_inline": ["#systemdesign"]
            }
        ],
        "hashtags": [
            "loadbalancing",
            "systemdesign",
            "scaling",
            "backend",
            "distributed",
            "performance",
            "netflix"
        ],
        "mentions_suggestions": [
            "@Netflix",
            "@awscloud"
        ],
        "link_plan": {
            "enabled": True,
            "placement": "last_post",
            "url": "https://systemdesign.com/load-balancing?utm_source=threads&utm_medium=post"
        },
        "image_prompts": [
            {
                "role": "square_a",
                "title": "Square A — Insight Card",
                "prompt": "1:1 square insight card for Load Balancing Strategies. Bold headline 'Load Balance' top-center; tiny server cluster diagram motif bottom-right; off-white bg; thin vector strokes; subtle dotted grid; blue accent color; generous margins; flat vector; mobile legible.",
                "negative_prompt": "no photos, no faces, no logos, no neon, no 3D, no glossy gradients, no clutter",
                "style_notes": "editorial poster tone; crisp kerning; strong contrast",
                "ratio": "1:1",
                "size_px": "1080x1080",
                "alt_text": "Square insight card with load balancing headline and server diagram"
            },
            {
                "role": "square_b",
                "title": "Square B — Checklist Motif",
                "prompt": "1:1 square card for Load Balancing Strategies with clean checklist: Round-Robin ✓, Weighted ✓, Least Connections ✓, Consistent Hash ✓; off-white bg; thin strokes; subtle grid; blue accent underlines; generous whitespace; flat vector aesthetic.",
                "negative_prompt": "no messy icons, no photos, no logos, no heavy gradients",
                "style_notes": "checklist clarity; mobile-first legibility",
                "ratio": "1:1",
                "size_px": "1080x1080",
                "alt_text": "Checklist-style square card with load balancing algorithms"
            }
        ],
        "compliance": {
            "main_post_chars_count": 123,
            "replies_total": 3,
            "hashtags_count": 7,
            "image_prompt_count": 2,
            "has_tracked_link": True,
            "per_post_hashtags_ok": True,
            "per_post_mentions_ok": True,
            "checks": [
                "main post ≤500 chars; 1–3 sentences",
                "reply_chain 0–4 items; each ≤500 chars",
                "5–10 casual hashtags total; human, non-spammy",
                "images: 2 prompts by default (1:1, 1080×1080)",
                "image_prompts length == image_plan.count when provided",
                "exactly one link if primary_url present, placed per link_plan"
            ]
        }
    }
    
    try:
        # Test direct schema validation
        print("🧪 Testing direct schema validation...")
        threads_post_content = ThreadsPostContent(**sample_content)
        print(f"✅ Direct schema validation passed")
        print(f"📊 Main post length: {len(threads_post_content.post)} chars")
        print(f"📝 Reply chain length: {len(threads_post_content.reply_chain)} posts")
        print(f"🏷️ Hashtags count: {len(threads_post_content.hashtags)}")
        print(f"👥 Mention suggestions: {len(threads_post_content.mentions_suggestions)}")
        print(f"🖼️ Image prompts: {len(threads_post_content.image_prompts)}")
        
        # Test schema validator function
        print(f"\n🧪 Testing schema validator function...")
        validated_content = validate_content('threads', 'post', sample_content)
        print(f"✅ Schema validator function passed")
        print(f"📋 Validated content type: {type(validated_content).__name__}")
        
        # Display sample content structure
        print(f"\n📋 Sample Threads Post Structure:")
        print(f"   • Main post: {len(sample_content['post'])} characters")
        print(f"   • Alt versions: {len(sample_content['alt_versions'])} variants")
        print(f"   • Reply chain: {len(sample_content['reply_chain'])} replies")
        print(f"   • Hashtags: {len(sample_content['hashtags'])} tags")
        print(f"   • Mentions: {len(sample_content['mentions_suggestions'])} suggestions")
        print(f"   • Images: {len(sample_content['image_prompts'])} prompts")
        
        return True
        
    except Exception as e:
        print(f"❌ Schema validation failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_direct_schema_instantiation():
    """Test direct instantiation of Threads Post schema"""
    print("\n" + "=" * 60)
    print("TEST 3: Direct Threads Post Schema Instantiation")
    print("=" * 60)
    
    try:
        # Create Threads Post content directly
        threads_post_content = ThreadsPostContent(
            post="Database sharding just saved our startup from a 3AM meltdown 😅\n\nHere's what we learned about scaling to millions of users 👇",
            alt_versions=[
                "From startup crash to scaling millions: our database sharding journey.",
                "3AM database meltdown → sharding success story. Here's how we did it."
            ],
            reply_chain=[
                {
                    "index": 2,
                    "text": "We started with one MySQL server handling everything 📊\n\n✅ Simple to manage\n❌ Single point of failure\n❌ Limited by one machine's resources\n\nWorked great... until 100K users. #scaling",
                    "chars_count": 189,
                    "mentions": [],
                    "hashtags_inline": ["#scaling"]
                },
                {
                    "index": 3,
                    "text": "Horizontal sharding changed everything 🚀\n\nUsers 1-1M → Shard A\nUsers 1M-2M → Shard B\nUsers 2M+ → Shard C\n\nQuery time dropped from 3s to 300ms instantly.",
                    "chars_count": 171,
                    "mentions": [],
                    "hashtags_inline": []
                }
            ],
            hashtags=[
                "sharding",
                "database",
                "scaling",
                "startup",
                "systemdesign",
                "mysql"
            ],
            mentions_suggestions=[
                "@MySQL"
            ],
            link_plan={
                "enabled": True,
                "placement": "last_post",
                "url": "https://systemdesign.com/database-sharding?utm_source=threads&utm_medium=post"
            },
            image_prompts=[
                {
                    "role": "square_a",
                    "title": "Square A — Insight Card",
                    "prompt": "1:1 square insight card for Database Sharding. Bold headline 'Shard Smart' center; tiny database split diagram motif; off-white bg; thin vector strokes; subtle dotted grid; green accent color; generous margins; flat vector; mobile legible.",
                    "negative_prompt": "no photos, no faces, no logos, no neon, no 3D, no glossy gradients, no clutter",
                    "style_notes": "editorial poster tone; crisp kerning; strong contrast",
                    "ratio": "1:1",
                    "size_px": "1080x1080",
                    "alt_text": "Square insight card with database sharding headline and split diagram"
                },
                {
                    "role": "square_b",
                    "title": "Square B — Checklist Motif",
                    "prompt": "1:1 square card for Database Sharding with clean performance metrics: 100K users ✓, 1M users ✓, 3s → 300ms ✓; off-white bg; thin strokes; subtle grid; green accent underlines; generous whitespace; flat vector aesthetic.",
                    "negative_prompt": "no messy icons, no photos, no logos, no heavy gradients",
                    "style_notes": "metrics clarity; mobile-first legibility",
                    "ratio": "1:1",
                    "size_px": "1080x1080",
                    "alt_text": "Checklist-style square card with sharding performance metrics"
                }
            ],
            compliance={
                "main_post_chars_count": 127,
                "replies_total": 2,
                "hashtags_count": 6,
                "image_prompt_count": 2,
                "has_tracked_link": True,
                "per_post_hashtags_ok": True,
                "per_post_mentions_ok": True,
                "checks": [
                    "main post ≤500 chars; 1–3 sentences",
                    "reply_chain 0–4 items; each ≤500 chars",
                    "5–10 casual hashtags total; human, non-spammy",
                    "images: 2 prompts by default (1:1, 1080×1080)",
                    "image_prompts length == image_plan.count when provided",
                    "exactly one link if primary_url present, placed per link_plan"
                ]
            }
        )
        
        print(f"✅ Direct schema instantiation successful")
        print(f"📊 Threads Post structure:")
        print(f"   • Main post: {len(threads_post_content.post)} characters")
        print(f"   • Alt versions: {len(threads_post_content.alt_versions)}")
        print(f"   • Reply chain: {len(threads_post_content.reply_chain)} replies")
        print(f"   • Hashtags: {len(threads_post_content.hashtags)}")
        print(f"   • Mentions: {len(threads_post_content.mentions_suggestions)}")
        print(f"   • Images: {len(threads_post_content.image_prompts)}")
        print(f"   • Link enabled: {threads_post_content.link_plan['enabled']}")
        
        # Test JSON serialization
        json_output = threads_post_content.model_dump()
        print(f"✅ JSON serialization successful")
        print(f"📄 JSON size: {len(json.dumps(json_output))} characters")
        
        return True
        
    except Exception as e:
        print(f"❌ Direct schema instantiation failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all Threads Post tests"""
    print("🧪 THREADS POST CONTENT GENERATION TESTS")
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
        print("🎉 All Threads Post tests passed! Ready for integration.")
    else:
        print("⚠️ Some tests failed. Please review the errors above.")
    
    return passed == len(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)