#!/usr/bin/env python3
"""
Simple test script for YouTube Short content generation.
Tests prompt processing, schema validation, and direct schema instantiation.
"""

import sys
import os
import json
from pathlib import Path

# Add the app directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from prompt_processor import PromptProcessor
from schemas import YouTubeShortContent, validate_content_schema

def test_prompt_processing():
    """Test YouTube Short prompt template processing"""
    print("=" * 60)
    print("TEST 1: YouTube Short Prompt Processing")
    print("=" * 60)
    
    try:
        processor = PromptProcessor()
        
        # Test data
        topic_id = "1001"
        topic_name = "Database Sharding Strategies"
        topic_description = "Comprehensive guide to horizontal database partitioning techniques, including range-based, hash-based, and directory-based sharding approaches for scaling distributed systems."
        
        # Process the prompt template
        prompt_path = "prompts/bodies/youtube-short.txt"
        processed_prompt = processor.process_prompt_template(
            template_path=prompt_path,
            topic_id=topic_id,
            topic_name=topic_name,
            topic_description=topic_description,
            platform="youtube",
            format_type="short"
        )
        
        print(f"✅ Prompt template processed successfully")
        print(f"📄 Template path: {prompt_path}")
        print(f"🎯 Topic: {topic_name}")
        print(f"📝 Processed prompt length: {len(processed_prompt)} characters")
        print(f"🔍 Contains topic name: {'✅' if topic_name in processed_prompt else '❌'}")
        print(f"🔍 Contains JSON format: {'✅' if 'beats' in processed_prompt else '❌'}")
        print(f"🔍 Contains duration rules: {'✅' if '45–60s' in processed_prompt else '❌'}")
        
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
    """Test YouTube Short schema validation with sample data"""
    print("\n" + "=" * 60)
    print("TEST 2: YouTube Short Schema Validation")
    print("=" * 60)
    
    # Sample YouTube Short content matching the new schema
    sample_content = {
        "title": "Database Sharding: Scale to Millions Like Netflix & Instagram",
        "beats": [
            {
                "label": "Hook",
                "time_range": "0-3s",
                "narration": "Netflix handles 230 million users. Instagram processes 500 million photos daily. Here's their secret.",
                "on_screen_text": "230M users",
                "visuals": "punch-in + bold keyword",
                "sfx": ["whoosh"]
            },
            {
                "label": "Value-1",
                "time_range": "3-15s",
                "narration": "Database sharding splits your data across multiple servers. Instead of one database choking on millions of records.",
                "on_screen_text": "Split Data",
                "visuals": "diagram pop-in",
                "b_roll": ["screen capture pan"]
            },
            {
                "label": "Value-2",
                "time_range": "15-30s",
                "narration": "Range-based sharding: A-M users on Server 1, N-Z on Server 2. Simple but 70% of companies get hotspots.",
                "on_screen_text": "70% hotspots",
                "visuals": "number swipe",
                "b_roll": ["metric overlay"]
            },
            {
                "label": "Value-3",
                "time_range": "30-45s",
                "narration": "Hash-based sharding uses algorithms to distribute evenly. Twitter went from 3 seconds to 300ms response time.",
                "on_screen_text": "3s → 300ms",
                "visuals": "split frame",
                "b_roll": ["timeline flash"]
            },
            {
                "label": "Subscribe",
                "time_range": "50-55s",
                "narration": "Hit subscribe for more system design secrets",
                "on_screen_text": "Subscribe + 🔔",
                "visuals": "subscribe pop",
                "sfx": ["click"]
            },
            {
                "label": "EndScreen",
                "time_range": "55-60s",
                "narration": "Watch the full breakdown for implementation details",
                "on_screen_text": "Watch full breakdown",
                "visuals": "end card grid"
            }
        ],
        "script": "[0:00] Netflix handles 230 million users. Instagram processes 500 million photos daily. Here's their secret. [0:03] Database sharding splits your data across multiple servers. Instead of one database choking on millions of records. [0:15] Range-based sharding: A-M users on Server 1, N-Z on Server 2. Simple but 70% of companies get hotspots. [0:30] Hash-based sharding uses algorithms to distribute evenly. Twitter went from 3 seconds to 300ms response time. [0:50] Hit subscribe for more system design secrets. [0:55] Watch the full breakdown for implementation details.",
        "overlay_text_cues": [
            {"time": "0:00-0:03", "text": "230M users"},
            {"time": "0:03-0:15", "text": "Split Data"},
            {"time": "0:15-0:30", "text": "70% hotspots"},
            {"time": "0:30-0:45", "text": "3s → 300ms"},
            {"time": "0:50-0:55", "text": "Subscribe + 🔔"},
            {"time": "0:55-0:60", "text": "Watch full breakdown"}
        ],
        "b_roll_plan": [
            {"time": "3-10s", "ideas": ["diagram zoom", "cursor highlight"]},
            {"time": "15-25s", "ideas": ["metric overlay", "comparison bar"]},
            {"time": "30-40s", "ideas": ["before/after panel", "timeline flash"]}
        ],
        "music": {
            "vibe": ["energetic tech", "clean minimal"],
            "bpm_range": "90–120",
            "search_terms": ["trending minimal beat", "future garage instrumental"],
            "ducking_notes": "reduce -6dB under VO"
        },
        "sfx": ["whoosh", "click", "soft pop"],
        "end_screen": {
            "cta_line": "Watch the full breakdown → systemdesign.com/sharding?utm_source=youtube&utm_medium=short",
            "elements": ["subscribe", "next video", "channel handle"],
            "show_handles": True
        },
        "description": {
            "text": "Database sharding is how Netflix, Instagram, and Twitter handle millions of users without breaking. This 60-second breakdown covers the three main sharding strategies and why 70% of companies struggle with hotspots. [0:00] Hook - The secret behind massive scale [0:15] Range-based sharding explained [0:30] Hash-based sharding performance gains [0:55] Full breakdown link. Learn system design fundamentals that power the world's biggest platforms. Subscribe for more system design secrets! Full breakdown: systemdesign.com/sharding?utm_source=youtube&utm_medium=short",
            "word_count": 198,
            "timestamps": [
                {"time": "0:00", "label": "Hook"},
                {"time": "0:15", "label": "Key stat"},
                {"time": "0:30", "label": "Example"},
                {"time": "0:55", "label": "End screen"}
            ]
        },
        "tags": [
            "database sharding",
            "system design",
            "scalable architecture",
            "distributed systems",
            "database optimization",
            "backend engineering",
            "software architecture",
            "tech interview prep",
            "netflix architecture",
            "instagram scaling",
            "twitter performance",
            "horizontal scaling",
            "database partitioning",
            "microservices",
            "system design interview",
            "tech career",
            "software engineering",
            "database design",
            "performance optimization",
            "tech education"
        ],
        "image_prompts": [
            {
                "role": "cover_a",
                "title": "Short Cover A — Bold Hook",
                "prompt": "Vertical 9:16 cover for Database Sharding Strategies. Bold 4–6 word hook top-center; tiny semantic diagram motif on right; off-white bg; thin vector strokes; subtle dotted grid; one accent color; generous margins; flat vector; mobile legible.",
                "negative_prompt": "no photos, no faces, no logos, no neon, no 3D, no glossy gradients, no clutter",
                "style_notes": "editorial poster; crisp kerning",
                "ratio": "9:16",
                "size_px": "1080x1920",
                "alt_text": "Vertical cover with bold hook and small diagram"
            },
            {
                "role": "cover_b",
                "title": "Short Cover B — Whiteboard Vibe",
                "prompt": "Vertical 9:16 cover with whiteboard feel for Database Sharding Strategies. Handwritten-style headline (clean, legible), small corner diagram; off-white bg; subtle grid; one accent underline; generous whitespace; flat vector aesthetic.",
                "negative_prompt": "no messy handwriting, no photos, no logos, no heavy gradients",
                "style_notes": "minimalist; high contrast; mobile-first",
                "ratio": "9:16",
                "size_px": "1080x1920",
                "alt_text": "Whiteboard-style cover with handwritten headline"
            }
        ],
        "compliance": {
            "duration_seconds": 60,
            "title_char_count": 67,
            "tags_count": 20,
            "image_prompt_count": 2,
            "has_link_in_description": True,
            "checks": [
                "Hook 0–3s with a number",
                "3–4 value micro-beats (one stat, one example)",
                "Subscribe 50–55s; End screen 55–60s",
                "overlay text & b-roll cues present",
                "music vibe set; SFX optional",
                "title ≤80 chars",
                "description ≈200 words with timestamps",
                "EXACTLY 20 tags",
                "image_prompts length == image_plan.count (default 2)"
            ]
        }
    }
    
    try:
        # Test direct schema validation
        print("🧪 Testing direct schema validation...")
        short_content = YouTubeShortContent(**sample_content)
        print(f"✅ Direct schema validation passed")
        print(f"📊 Beats count: {len(short_content.beats)}")
        print(f"🏷️ Tags count: {len(short_content.tags)}")
        print(f"🖼️ Image prompts count: {len(short_content.image_prompts)}")
        print(f"⏱️ Duration: {short_content.compliance['duration_seconds']}s")
        print(f"📝 Title length: {short_content.compliance['title_char_count']} chars")
        
        # Test schema validator function
        print(f"\n🧪 Testing schema validator function...")
        validated_content = validate_content_schema('youtube', 'short', sample_content)
        print(f"✅ Schema validator function passed")
        print(f"📋 Validated content type: {type(validated_content).__name__}")
        
        # Display sample content structure
        print(f"\n📋 Sample YouTube Short Structure:")
        print(f"   • Title: {len(sample_content['title'])} characters")
        print(f"   • Beats: {len(sample_content['beats'])} structured segments")
        print(f"   • Script: {len(sample_content['script'])} characters")
        print(f"   • Overlay cues: {len(sample_content['overlay_text_cues'])} timing points")
        print(f"   • B-roll plan: {len(sample_content['b_roll_plan'])} segments")
        print(f"   • Tags: {len(sample_content['tags'])} keywords")
        print(f"   • Image prompts: {len(sample_content['image_prompts'])} covers")
        
        return True
        
    except Exception as e:
        print(f"❌ Schema validation failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_direct_schema_instantiation():
    """Test direct instantiation of YouTube Short schema"""
    print("\n" + "=" * 60)
    print("TEST 3: Direct YouTube Short Schema Instantiation")
    print("=" * 60)
    
    try:
        # Create YouTube Short content directly
        short_content = YouTubeShortContent(
            title="Microservices vs Monoliths: The 60-Second Truth",
            beats=[
                {
                    "label": "Hook",
                    "time_range": "0-3s",
                    "narration": "Uber has 2,200 microservices. Shopify runs a monolith serving 1.7M merchants. Who's right?",
                    "on_screen_text": "2,200 services",
                    "visuals": "punch-in + bold keyword",
                    "sfx": ["whoosh"]
                },
                {
                    "label": "Value-1",
                    "time_range": "3-15s",
                    "narration": "Monoliths: One codebase, simple deployment, faster development. Perfect for small teams.",
                    "on_screen_text": "One Codebase",
                    "visuals": "diagram pop-in",
                    "b_roll": ["screen capture pan"]
                },
                {
                    "label": "Value-2",
                    "time_range": "15-30s",
                    "narration": "Microservices: Independent scaling, fault isolation. But 60% of teams struggle with complexity.",
                    "on_screen_text": "60% struggle",
                    "visuals": "number swipe",
                    "b_roll": ["metric overlay"]
                },
                {
                    "label": "Value-3",
                    "time_range": "30-45s",
                    "narration": "The truth: Start monolith, extract services when teams grow. Architecture follows organization.",
                    "on_screen_text": "Start → Extract",
                    "visuals": "split frame",
                    "b_roll": ["timeline flash"]
                },
                {
                    "label": "Subscribe",
                    "time_range": "50-55s",
                    "narration": "Subscribe for more architecture insights",
                    "on_screen_text": "Subscribe + 🔔",
                    "visuals": "subscribe pop",
                    "sfx": ["click"]
                },
                {
                    "label": "EndScreen",
                    "time_range": "55-60s",
                    "narration": "Watch the deep dive for implementation strategies",
                    "on_screen_text": "Watch deep dive",
                    "visuals": "end card grid"
                }
            ],
            script="[0:00] Uber has 2,200 microservices. Shopify runs a monolith serving 1.7M merchants. Who's right? [0:03] Monoliths: One codebase, simple deployment, faster development. Perfect for small teams. [0:15] Microservices: Independent scaling, fault isolation. But 60% of teams struggle with complexity. [0:30] The truth: Start monolith, extract services when teams grow. Architecture follows organization. [0:50] Subscribe for more architecture insights. [0:55] Watch the deep dive for implementation strategies.",
            overlay_text_cues=[
                {"time": "0:00-0:03", "text": "2,200 services"},
                {"time": "0:03-0:15", "text": "One Codebase"},
                {"time": "0:15-0:30", "text": "60% struggle"},
                {"time": "0:30-0:45", "text": "Start → Extract"},
                {"time": "0:50-0:55", "text": "Subscribe + 🔔"},
                {"time": "0:55-0:60", "text": "Watch deep dive"}
            ],
            b_roll_plan=[
                {"time": "3-10s", "ideas": ["monolith diagram", "simple flow"]},
                {"time": "15-25s", "ideas": ["microservices network", "complexity visual"]},
                {"time": "30-40s", "ideas": ["evolution timeline", "team growth"]}
            ],
            music={
                "vibe": ["energetic tech", "clean minimal"],
                "bpm_range": "100–130",
                "search_terms": ["tech beat", "minimal electronic"],
                "ducking_notes": "reduce -6dB under VO"
            },
            sfx=["whoosh", "click", "pop"],
            end_screen={
                "cta_line": "Watch the deep dive → systemdesign.com/microservices?utm_source=youtube&utm_medium=short",
                "elements": ["subscribe", "next video", "channel handle"],
                "show_handles": True
            },
            description={
                "text": "Microservices vs Monoliths: the eternal architecture debate. This 60-second breakdown reveals why Uber chose 2,200 microservices while Shopify thrives with a monolith. [0:00] The setup - two different approaches [0:15] Microservices complexity reality [0:30] The strategic truth [0:55] Deep dive link. Learn when to choose each architecture pattern. Subscribe for more system design insights! Deep dive: systemdesign.com/microservices?utm_source=youtube&utm_medium=short",
                "word_count": 195,
                "timestamps": [
                    {"time": "0:00", "label": "Hook"},
                    {"time": "0:15", "label": "Complexity stat"},
                    {"time": "0:30", "label": "Strategy"},
                    {"time": "0:55", "label": "End screen"}
                ]
            },
            tags=[
                "microservices",
                "monolith architecture",
                "system design",
                "software architecture",
                "distributed systems",
                "scalable architecture",
                "backend engineering",
                "tech architecture",
                "software engineering",
                "system design interview",
                "uber architecture",
                "shopify scaling",
                "architecture patterns",
                "tech career",
                "engineering leadership",
                "software design",
                "tech education",
                "architecture decision",
                "system scaling",
                "tech interview prep"
            ],
            image_prompts=[
                {
                    "role": "cover_a",
                    "title": "Short Cover A — Bold Hook",
                    "prompt": "Vertical 9:16 cover for Microservices vs Monoliths. Bold comparison visual; off-white bg; clean typography; one accent color; mobile-optimized.",
                    "negative_prompt": "no photos, no logos, no clutter",
                    "style_notes": "editorial; high contrast",
                    "ratio": "9:16",
                    "size_px": "1080x1920",
                    "alt_text": "Microservices vs Monoliths comparison cover"
                },
                {
                    "role": "cover_b",
                    "title": "Short Cover B — Whiteboard Vibe",
                    "prompt": "Vertical 9:16 whiteboard-style cover with architecture diagrams; clean handwritten feel; minimal design.",
                    "negative_prompt": "no messy handwriting, no photos",
                    "style_notes": "whiteboard aesthetic; legible",
                    "ratio": "9:16",
                    "size_px": "1080x1920",
                    "alt_text": "Whiteboard architecture diagram cover"
                }
            ],
            compliance={
                "duration_seconds": 60,
                "title_char_count": 49,
                "tags_count": 20,
                "image_prompt_count": 2,
                "has_link_in_description": True,
                "checks": [
                    "Hook 0–3s with a number",
                    "3–4 value micro-beats (one stat, one example)",
                    "Subscribe 50–55s; End screen 55–60s",
                    "overlay text & b-roll cues present",
                    "music vibe set; SFX optional",
                    "title ≤80 chars",
                    "description ≈200 words with timestamps",
                    "EXACTLY 20 tags",
                    "image_prompts length == image_plan.count (default 2)"
                ]
            }
        )
        
        print(f"✅ Direct schema instantiation successful")
        print(f"📊 YouTube Short structure:")
        print(f"   • Title: {len(short_content.title)} characters")
        print(f"   • Beats: {len(short_content.beats)} segments")
        print(f"   • Script length: {len(short_content.script)} characters")
        print(f"   • Overlay cues: {len(short_content.overlay_text_cues)}")
        print(f"   • B-roll segments: {len(short_content.b_roll_plan)}")
        print(f"   • Tags: {len(short_content.tags)}")
        print(f"   • Image prompts: {len(short_content.image_prompts)}")
        print(f"   • Duration: {short_content.compliance['duration_seconds']}s")
        
        # Test JSON serialization
        json_output = short_content.model_dump()
        print(f"✅ JSON serialization successful")
        print(f"📄 JSON size: {len(json.dumps(json_output))} characters")
        
        return True
        
    except Exception as e:
        print(f"❌ Direct schema instantiation failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all YouTube Short tests"""
    print("🧪 YOUTUBE SHORT CONTENT GENERATION TESTS")
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
        print("🎉 All YouTube Short tests passed! Ready for integration.")
    else:
        print("⚠️ Some tests failed. Please review the errors above.")
    
    return passed == len(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)