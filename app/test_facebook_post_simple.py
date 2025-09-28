#!/usr/bin/env python3
"""
Simple test script for Facebook Post content generation.
Tests prompt processing, schema validation, and direct schema instantiation.
"""

import sys
import os
import json
from pathlib import Path

# Add the app directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from prompt_processor import PromptProcessor
from schemas import FacebookPostContent, validate_content_schema

def test_prompt_processing():
    """Test Facebook Post prompt template processing"""
    print("=" * 60)
    print("TEST 1: Facebook Post Prompt Processing")
    print("=" * 60)
    
    try:
        processor = PromptProcessor()
        
        # Test data
        topic_id = "1001"
        topic_name = "Database Sharding Strategies"
        topic_description = "Comprehensive guide to horizontal database partitioning techniques, including range-based, hash-based, and directory-based sharding approaches for scaling distributed systems."
        
        # Process the prompt template
        prompt_path = "prompts/bodies/facebook-post.txt"
        processed_prompt = processor.process_prompt_template(
            template_path=prompt_path,
            topic_id=topic_id,
            topic_name=topic_name,
            topic_description=topic_description,
            platform="facebook",
            format_type="post"
        )
        
        print(f"✅ Prompt template processed successfully")
        print(f"📄 Template path: {prompt_path}")
        print(f"🎯 Topic: {topic_name}")
        print(f"📝 Processed prompt length: {len(processed_prompt)} characters")
        print(f"🔍 Contains topic name: {'✅' if topic_name in processed_prompt else '❌'}")
        print(f"🔍 Contains JSON format: {'✅' if 'long_body' in processed_prompt else '❌'}")
        print(f"🔍 Contains groups strategy: {'✅' if 'groups_to_share' in processed_prompt else '❌'}")
        
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
    """Test Facebook Post schema validation with sample data"""
    print("\n" + "=" * 60)
    print("TEST 2: Facebook Post Schema Validation")
    print("=" * 60)
    
    # Sample Facebook Post content matching the new schema
    sample_content = {
        "headline": "The Database Scaling Secret That Netflix & Instagram Don't Want You to Know",
        "post": "Ever wonder how Netflix handles 230 million users without breaking?\n\nThe secret isn't what you think.\n\nIt's all about smart database sharding 🧵\n\nRead the full story below 👇",
        "alt_versions": [
            "Netflix serves 230M users daily. Here's their database secret that changed everything.",
            "The one database trick that separates billion-dollar companies from everyone else."
        ],
        "long_body": {
            "text": "I still remember the day our startup's database crashed at 3 AM.\n\nWe had just hit 100,000 users, and our single MySQL server couldn't handle the load. Sound familiar?\n\nThat's when I learned about database sharding – the same technique that powers Netflix, Instagram, and Twitter.\n\nHere's the story:\n\n**The Problem**\nMost companies start with a single database. It's simple, it works... until it doesn't. When you hit millions of records, everything slows down. Queries take forever. Your users get frustrated. Your business suffers.\n\n**The Solution**\nDatabase sharding splits your data across multiple servers. Instead of one database choking on millions of records, you have multiple databases each handling a portion.\n\nThink of it like this: Instead of one cashier serving 1000 customers, you have 10 cashiers each serving 100 customers.\n\n**Three Main Approaches:**\n\n1. **Range-based sharding**: Split users A-M on Server 1, N-Z on Server 2. Simple but can create hotspots.\n\n2. **Hash-based sharding**: Use algorithms to distribute data evenly. Twitter saw response times drop from 3 seconds to 300ms with this approach.\n\n3. **Directory-based sharding**: Use a lookup service to find data. Most flexible but adds complexity.\n\n**Real-World Impact:**\n- Instagram handles 500 million photo uploads daily using hash-based sharding\n- Netflix processes 1 billion hours of video monthly across sharded databases\n- Twitter reduced query time by 90% after implementing their sharding strategy\n\n**The Trade-offs:**\nSharding isn't free. Cross-database queries become complex. Data consistency gets harder. You need more operational overhead.\n\nBut here's the thing: 60% of companies that scale successfully use some form of sharding.\n\n**When to Shard:**\nDon't shard too early. Most applications don't need it until 10+ million records. But when you do need it, having a plan makes all the difference.\n\nWant the complete implementation guide with code examples and architecture diagrams? Check out our detailed breakdown: systemdesign.com/sharding?utm_source=facebook&utm_medium=post\n\nWhat's your experience with database scaling? Have you hit the wall where a single database wasn't enough? Share your story in the comments – I read every one.\n\n#DatabaseSharding #SystemDesign #TechArchitecture #Scaling #SoftwareEngineering",
            "word_count": 623,
            "emotional_angle": "relief"
        },
        "link_preview": {
            "title": "Database Sharding: Complete Implementation Guide",
            "description": "Learn how Netflix, Instagram & Twitter scale to millions with smart database sharding strategies.",
            "og_image_role": "card_wide"
        },
        "groups_pitch": "Sharing insights on database scaling strategies that helped major platforms handle millions of users. Thought this community would find the real-world examples valuable.",
        "groups_to_share": [
            {
                "name": "Software Engineering",
                "type": "group",
                "url": "",
                "why_relevant": "Database scaling is core to software engineering at scale",
                "share_blurb": "Real-world database sharding strategies from Netflix, Instagram, and Twitter. Includes implementation trade-offs and when to shard.",
                "rules_checklist": ["allow links?", "no promo days?"]
            },
            {
                "name": "System Design Interview",
                "type": "group", 
                "url": "",
                "why_relevant": "Sharding is a common system design interview topic",
                "share_blurb": "Database sharding deep-dive with actual performance numbers from major tech companies. Perfect for system design prep.",
                "rules_checklist": ["educational content allowed", "no spam"]
            },
            {
                "name": "Backend Developers",
                "type": "group",
                "url": "",
                "why_relevant": "Backend developers directly deal with database scaling challenges",
                "share_blurb": "How Twitter reduced query time by 90% and Instagram handles 500M daily uploads through smart sharding strategies.",
                "rules_checklist": ["technical content welcome", "allow external links"]
            },
            {
                "name": "Startup CTO Network",
                "type": "group",
                "url": "",
                "why_relevant": "CTOs need to plan for database scaling before hitting the wall",
                "share_blurb": "Database scaling lessons from a startup that crashed at 100K users. When to shard and how to avoid common pitfalls.",
                "rules_checklist": ["startup focused", "leadership content"]
            },
            {
                "name": "Database Professionals",
                "type": "group",
                "url": "",
                "why_relevant": "Database professionals implement and manage sharding strategies",
                "share_blurb": "Technical breakdown of range-based vs hash-based vs directory-based sharding with real performance metrics.",
                "rules_checklist": ["technical discussions encouraged", "professional content"]
            },
            {
                "name": "Tech Architecture",
                "type": "group",
                "url": "",
                "why_relevant": "Sharding is a key architectural decision for scalable systems",
                "share_blurb": "Architecture patterns for database sharding used by Netflix, Instagram, and Twitter. Includes trade-offs and implementation guidance.",
                "rules_checklist": ["architecture content welcome", "detailed posts encouraged"]
            },
            {
                "name": "Scalable Systems",
                "type": "group",
                "url": "",
                "why_relevant": "Database sharding is fundamental to building scalable systems",
                "share_blurb": "How major platforms handle millions of users through database sharding. Real numbers and implementation strategies.",
                "rules_checklist": ["scaling content relevant", "case studies welcome"]
            }
        ],
        "hashtags": [
            "DatabaseSharding",
            "SystemDesign", 
            "TechArchitecture",
            "Scaling",
            "SoftwareEngineering"
        ],
        "mention_suggestions": [
            "@Netflix",
            "@Instagram",
            "@Twitter"
        ],
        "image_prompts": [
            {
                "role": "card_wide",
                "title": "FB Card A — Wide Insight",
                "prompt": "1.91:1 wide insight card for Database Sharding Strategies. Short headline 'Scale Like Netflix' top-left; tiny database sharding diagram motif on right showing multiple connected servers; off-white/light background; thin vector strokes; subtle dotted grid; blue accent color; generous margins; flat vector aesthetic; export sharp for 1200x627.",
                "negative_prompt": "no stock-photo people, no logos, no neon, no 3D, no glossy gradients, no clutter",
                "style_notes": "corporate-clean; high contrast; mobile & desktop legible",
                "ratio": "1.91:1",
                "size_px": "1200x627",
                "alt_text": "Wide insight card with database sharding diagram"
            },
            {
                "role": "card_square",
                "title": "FB Card B — Square Variant",
                "prompt": "1:1 square variant for Database Sharding Strategies; same concept as wide card but optimized for square; bold headline 'Database Sharding'; small diagram motif showing data distribution; off-white bg; subtle grid; blue accent; generous whitespace; flat vector.",
                "negative_prompt": "no heavy gradients, no logos, no photos",
                "style_notes": "editorial poster feel; crisp kerning",
                "ratio": "1:1",
                "size_px": "1080x1080",
                "alt_text": "Square insight card variant with sharding concept"
            }
        ],
        "compliance": {
            "post_lines_count": 4,
            "long_body_word_count": 623,
            "hashtags_count": 5,
            "groups_count": 7,
            "image_prompt_count": 2,
            "has_tracked_link": True,
            "checks": [
                "above-the-fold post has 2–4 lines + 1 CTA",
                "story body is 500–700 words; includes mini-story/case + 1–2 stats",
                "exactly one tracked link if primary_url present",
                "3–6 hashtags; casual/professional; unique",
                "5–10 relevant groups suggested with reasons",
                "image_prompts length == image_plan.count (default 2)",
                "OG preview fields provided (title/description + image role)"
            ]
        }
    }
    
    try:
        # Test direct schema validation
        print("🧪 Testing direct schema validation...")
        fb_post_content = FacebookPostContent(**sample_content)
        print(f"✅ Direct schema validation passed")
        print(f"📊 Headline length: {len(fb_post_content.headline)} chars")
        print(f"📝 Long body word count: {fb_post_content.long_body['word_count']} words")
        print(f"🏷️ Hashtags count: {len(fb_post_content.hashtags)}")
        print(f"👥 Groups count: {len(fb_post_content.groups_to_share)}")
        print(f"🖼️ Image prompts count: {len(fb_post_content.image_prompts)}")
        
        # Test schema validator function
        print(f"\n🧪 Testing schema validator function...")
        validated_content = validate_content_schema('facebook', 'post', sample_content)
        print(f"✅ Schema validator function passed")
        print(f"📋 Validated content type: {type(validated_content).__name__}")
        
        # Display sample content structure
        print(f"\n📋 Sample Facebook Post Structure:")
        print(f"   • Headline: {len(sample_content['headline'])} characters")
        print(f"   • Post: {sample_content['compliance']['post_lines_count']} lines")
        print(f"   • Alt versions: {len(sample_content['alt_versions'])} variants")
        print(f"   • Long body: {sample_content['long_body']['word_count']} words")
        print(f"   • Groups strategy: {len(sample_content['groups_to_share'])} communities")
        print(f"   • Hashtags: {len(sample_content['hashtags'])} tags")
        print(f"   • Image prompts: {len(sample_content['image_prompts'])} cards")
        
        return True
        
    except Exception as e:
        print(f"❌ Schema validation failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_direct_schema_instantiation():
    """Test direct instantiation of Facebook Post schema"""
    print("\n" + "=" * 60)
    print("TEST 3: Direct Facebook Post Schema Instantiation")
    print("=" * 60)
    
    try:
        # Create Facebook Post content directly
        fb_post_content = FacebookPostContent(
            headline="Microservices vs Monoliths: The Truth Every Developer Should Know",
            post="Uber runs 2,200 microservices.\nShopify thrives with a monolith.\n\nWho's doing it right? 🤔\n\nThe answer might surprise you 👇",
            alt_versions=[
                "The microservices vs monolith debate, settled once and for all.",
                "Why Shopify chose monolith over microservices (and why it worked)."
            ],
            long_body={
                "text": "Five years ago, I made a decision that saved our startup $2 million.\n\nWe were debating: microservices or monolith?\n\nEveryone said microservices were the future. Netflix had thousands. Uber was scaling like crazy. We felt pressure to follow.\n\nBut we chose the monolith. Here's why:\n\n**The Microservices Hype**\nMicroservices promise independent scaling, fault isolation, and team autonomy. Sounds perfect, right?\n\nBut here's what they don't tell you:\n- 60% of teams struggle with microservices complexity\n- Network latency increases by 3-5x\n- Debugging becomes a nightmare across services\n- You need dedicated DevOps teams\n\n**The Monolith Reality**\nShopify serves 1.7 million merchants with a Rails monolith. Stack Overflow handles 1.3 billion page views monthly with a monolith.\n\nWhy? Because monoliths offer:\n- Simple deployment (one artifact)\n- Easy debugging (single codebase)\n- Faster development cycles\n- Lower operational overhead\n\n**When Each Makes Sense**\n\nChoose microservices when:\n- You have 50+ engineers\n- Clear service boundaries exist\n- You have strong DevOps capabilities\n- Independent scaling is critical\n\nChoose monoliths when:\n- Team size under 25 people\n- Rapid feature development needed\n- Limited DevOps resources\n- Uncertain domain boundaries\n\n**The Hybrid Approach**\nMany successful companies start with a modular monolith, then extract services as teams and boundaries become clear.\n\nGitHub started as a monolith. Twitter started as a monolith. Even Amazon started as a monolith.\n\nThe key is knowing when to evolve.\n\n**Our Decision**\nWe stayed with the monolith for 3 years. Shipped features 40% faster than our microservices competitors. When we finally needed to scale, we had clear boundaries and dedicated teams.\n\nResult? Smooth transition with minimal technical debt.\n\nArchitecture follows organization, not the other way around.\n\nWhat's your experience? Monolith or microservices? Share your story below – I'd love to hear different perspectives.\n\n#Microservices #Monolith #SoftwareArchitecture #TechDecisions #StartupLessons",
                "word_count": 587,
                "emotional_angle": "curiosity"
            },
            link_preview={
                "title": "Microservices vs Monolith: The Complete Guide",
                "description": "Learn when to choose microservices vs monoliths with real examples from Uber, Shopify, and successful startups.",
                "og_image_role": "card_wide"
            },
            groups_pitch="Sharing real-world architecture decisions and lessons learned from choosing monolith over microservices. Includes practical guidance for teams facing this decision.",
            groups_to_share=[
                {
                    "name": "Software Architecture",
                    "type": "group",
                    "url": "",
                    "why_relevant": "Core architectural decision-making content",
                    "share_blurb": "Real-world microservices vs monolith decision with 3-year outcome data. Practical guidance for architecture choices.",
                    "rules_checklist": ["architecture content welcome", "case studies allowed"]
                },
                {
                    "name": "Startup Tech Leaders",
                    "type": "group",
                    "url": "",
                    "why_relevant": "Critical technical decisions for startup CTOs",
                    "share_blurb": "How choosing monolith over microservices saved our startup $2M and 40% development time. Lessons for tech leaders.",
                    "rules_checklist": ["startup focused", "leadership content"]
                },
                {
                    "name": "Engineering Management",
                    "type": "group",
                    "url": "",
                    "why_relevant": "Team structure and technical decision alignment",
                    "share_blurb": "Architecture follows organization: when team size and structure should drive your microservices vs monolith decision.",
                    "rules_checklist": ["management content", "team scaling topics"]
                },
                {
                    "name": "Backend Engineering",
                    "type": "group",
                    "url": "",
                    "why_relevant": "Backend engineers implement these architectural patterns",
                    "share_blurb": "Technical breakdown of microservices vs monolith trade-offs with real performance and complexity data.",
                    "rules_checklist": ["technical content welcome", "architecture discussions"]
                },
                {
                    "name": "System Design",
                    "type": "group",
                    "url": "",
                    "why_relevant": "Common system design interview and real-world topic",
                    "share_blurb": "Microservices vs monolith decision framework with examples from Shopify, Uber, and successful startups.",
                    "rules_checklist": ["system design content", "real examples encouraged"]
                }
            ],
            hashtags=[
                "Microservices",
                "Monolith", 
                "SoftwareArchitecture",
                "TechDecisions",
                "StartupLessons"
            ],
            mention_suggestions=[
                "@Shopify",
                "@Uber"
            ],
            image_prompts=[
                {
                    "role": "card_wide",
                    "title": "FB Card A — Wide Insight",
                    "prompt": "1.91:1 wide insight card for Microservices vs Monoliths. Headline 'Micro vs Mono' top-left; tiny architecture diagram showing monolith vs microservices; off-white background; blue accent; flat vector; mobile legible.",
                    "negative_prompt": "no stock photos, no logos, no clutter",
                    "style_notes": "clean comparison; high contrast",
                    "ratio": "1.91:1",
                    "size_px": "1200x627",
                    "alt_text": "Wide card comparing microservices vs monolith"
                },
                {
                    "role": "card_square",
                    "title": "FB Card B — Square Variant",
                    "prompt": "1:1 square variant for Microservices vs Monoliths; bold headline; small architecture comparison diagram; off-white bg; blue accent; generous whitespace; flat vector.",
                    "negative_prompt": "no gradients, no logos, no photos",
                    "style_notes": "editorial poster feel; crisp typography",
                    "ratio": "1:1",
                    "size_px": "1080x1080",
                    "alt_text": "Square architecture comparison card"
                }
            ],
            compliance={
                "post_lines_count": 4,
                "long_body_word_count": 587,
                "hashtags_count": 5,
                "groups_count": 5,
                "image_prompt_count": 2,
                "has_tracked_link": False,
                "checks": [
                    "above-the-fold post has 2–4 lines + 1 CTA",
                    "story body is 500–700 words; includes mini-story/case + 1–2 stats",
                    "exactly one tracked link if primary_url present",
                    "3–6 hashtags; casual/professional; unique",
                    "5–10 relevant groups suggested with reasons",
                    "image_prompts length == image_plan.count (default 2)",
                    "OG preview fields provided (title/description + image role)"
                ]
            }
        )
        
        print(f"✅ Direct schema instantiation successful")
        print(f"📊 Facebook Post structure:")
        print(f"   • Headline: {len(fb_post_content.headline)} characters")
        print(f"   • Post lines: {fb_post_content.compliance['post_lines_count']}")
        print(f"   • Alt versions: {len(fb_post_content.alt_versions)}")
        print(f"   • Long body: {fb_post_content.long_body['word_count']} words")
        print(f"   • Groups: {len(fb_post_content.groups_to_share)}")
        print(f"   • Hashtags: {len(fb_post_content.hashtags)}")
        print(f"   • Image prompts: {len(fb_post_content.image_prompts)}")
        
        # Test JSON serialization
        json_output = fb_post_content.model_dump()
        print(f"✅ JSON serialization successful")
        print(f"📄 JSON size: {len(json.dumps(json_output))} characters")
        
        return True
        
    except Exception as e:
        print(f"❌ Direct schema instantiation failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all Facebook Post tests"""
    print("🧪 FACEBOOK POST CONTENT GENERATION TESTS")
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
        print("🎉 All Facebook Post tests passed! Ready for integration.")
    else:
        print("⚠️ Some tests failed. Please review the errors above.")
    
    return passed == len(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)