#!/usr/bin/env python3
"""
Simple test script for YouTube Long Form content generation.
Tests prompt processing, schema validation, and direct schema instantiation.
"""

import sys
import os
import json
from pathlib import Path

# Add the app directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from prompt_processor import PromptProcessor
from schemas import YouTubeLongFormContent, validate_content_schema

def test_prompt_processing():
    """Test YouTube Long Form prompt template processing"""
    print("=" * 60)
    print("TEST 1: YouTube Long Form Prompt Processing")
    print("=" * 60)
    
    try:
        processor = PromptProcessor()
        
        # Test data
        topic_id = "1001"
        topic_name = "Database Sharding Strategies"
        topic_description = "Comprehensive guide to horizontal database partitioning techniques, including range-based, hash-based, and directory-based sharding approaches for scaling distributed systems."
        
        # Process the prompt template
        prompt_path = "prompts/bodies/youtube-long-form.txt"
        processed_prompt = processor.process_prompt_template(
            template_path=prompt_path,
            topic_id=topic_id,
            topic_name=topic_name,
            topic_description=topic_description,
            platform="youtube",
            format_type="long_form"
        )
        
        print(f"✅ Prompt template processed successfully")
        print(f"📄 Template path: {prompt_path}")
        print(f"🎯 Topic: {topic_name}")
        print(f"📝 Processed prompt length: {len(processed_prompt)} characters")
        print(f"🔍 Contains topic name: {'✅' if topic_name in processed_prompt else '❌'}")
        print(f"🔍 Contains JSON format: {'✅' if 'outline' in processed_prompt else '❌'}")
        print(f"🔍 Contains duration rules: {'✅' if '8–12 minute' in processed_prompt else '❌'}")
        
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
    """Test YouTube Long Form schema validation with sample data"""
    print("\n" + "=" * 60)
    print("TEST 2: YouTube Long Form Schema Validation")
    print("=" * 60)
    
    # Sample YouTube Long Form content matching the new schema
    sample_content = {
        "title": "Database Sharding: How Netflix & Instagram Scale to Millions",
        "thumbnail_text": "Scale Millions",
        "intro": {
            "time_range": "0:00–0:15",
            "narration": "Netflix handles 230 million users daily. Instagram processes 500 million photos. Here's exactly how they do it without breaking.",
            "on_screen_text": "230M users",
            "visuals": "punch-in + bold keyword; quick diagram flash",
            "b_roll": ["screen capture teaser", "metric overlay"],
            "sfx": ["whoosh"],
            "music": {"vibe": ["energetic tech", "clean minimal"], "bmp_range": "90–110"}
        },
        "outline": [
            {"section": "Hook & problem", "beats": ["230M users stat", "Why sharding matters", "What you'll learn"]},
            {"section": "Background", "beats": ["Database bottlenecks", "Scaling challenges", "When to shard"]},
            {"section": "Architecture / Mechanics", "beats": ["Range-based sharding", "Hash-based sharding", "Directory-based sharding"]},
            {"section": "Trade-offs & pitfalls", "beats": ["Hotspot problems", "Cross-shard queries", "Complexity overhead"]},
            {"section": "Case study", "beats": ["Instagram's approach", "Netflix's strategy", "Performance results"]},
            {"section": "Summary & CTA", "beats": ["Key takeaways", "Implementation tips", "Resources"]}
        ],
        "chapters": [
            {"index": 1, "name": "Hook & problem", "timestamp": "0:00"},
            {"index": 2, "name": "Background", "timestamp": "0:45"},
            {"index": 3, "name": "Range-based sharding", "timestamp": "2:15"},
            {"index": 4, "name": "Hash-based sharding", "timestamp": "4:00"},
            {"index": 5, "name": "Directory-based sharding", "timestamp": "5:30"},
            {"index": 6, "name": "Trade-offs & pitfalls", "timestamp": "7:00"},
            {"index": 7, "name": "Case study", "timestamp": "8:30"},
            {"index": 8, "name": "Summary & CTA", "timestamp": "10:00"}
        ],
        "script": [
            {
                "chapter_index": 1,
                "time_range": "0:00–0:45",
                "talking_points": ["230M users hook", "scaling problem", "video preview"],
                "details": "Netflix handles 230 million users daily. Instagram processes 500 million photos. Here's exactly how they do it without breaking. In the next 10 minutes, you'll learn the three sharding strategies that power the world's biggest platforms.",
                "screen_recording_notes": ["show Netflix dashboard", "Instagram metrics"],
                "graphics": ["Netflix logo lower-third", "metric chip 230M"]
            },
            {
                "chapter_index": 2,
                "time_range": "0:45–2:15",
                "talking_points": ["database bottlenecks", "single point failure", "scaling limits"],
                "details": "When your database hits millions of records, everything slows down. Queries take forever. Your single database becomes the bottleneck. That's where sharding comes in - splitting your data across multiple databases.",
                "screen_recording_notes": ["show slow query demo", "database performance graphs"],
                "graphics": ["bottleneck visualization", "performance chart"]
            },
            {
                "chapter_index": 3,
                "time_range": "2:15–4:00",
                "talking_points": ["range-based concept", "A-M vs N-Z example", "hotspot issues"],
                "details": "Range-based sharding splits data by ranges. Users A-M go to Server 1, N-Z to Server 2. Simple to understand, but creates hotspots if your data isn't evenly distributed.",
                "screen_recording_notes": ["range diagram animation", "hotspot visualization"],
                "graphics": ["range sharding diagram", "hotspot warning"]
            },
            {
                "chapter_index": 4,
                "time_range": "4:00–5:30",
                "talking_points": ["hash function concept", "even distribution", "Twitter example"],
                "details": "Hash-based sharding uses algorithms to distribute data evenly. Twitter uses this approach and saw response times drop from 3 seconds to 300ms. More complex but prevents hotspots.",
                "screen_recording_notes": ["hash function demo", "Twitter performance metrics"],
                "graphics": ["hash algorithm visualization", "performance improvement chart"]
            },
            {
                "chapter_index": 5,
                "time_range": "5:30–7:00",
                "talking_points": ["directory service concept", "lookup table", "flexibility vs complexity"],
                "details": "Directory-based sharding uses a lookup service to find data. Most flexible but adds complexity and a potential single point of failure. Use when you need maximum control.",
                "screen_recording_notes": ["directory service demo", "lookup table visualization"],
                "graphics": ["directory architecture diagram", "complexity warning"]
            },
            {
                "chapter_index": 6,
                "time_range": "7:00–8:30",
                "talking_points": ["cross-shard queries", "data consistency", "operational overhead"],
                "details": "Sharding isn't free. Cross-shard queries become complex. Data consistency gets harder. You need more operational overhead. 60% of teams underestimate this complexity.",
                "screen_recording_notes": ["complex query example", "consistency issues demo"],
                "graphics": ["complexity chart", "60% statistic"]
            },
            {
                "chapter_index": 7,
                "time_range": "8:30–10:00",
                "talking_points": ["Instagram hash approach", "Netflix range strategy", "performance results"],
                "details": "Instagram uses hash-based sharding for photos, handling 500M daily uploads. Netflix combines range and hash strategies for different data types. Both saw 10x performance improvements.",
                "screen_recording_notes": ["Instagram architecture", "Netflix system diagram"],
                "graphics": ["Instagram stats", "Netflix performance chart"]
            },
            {
                "chapter_index": 8,
                "time_range": "10:00–11:00",
                "talking_points": ["key takeaways", "when to shard", "implementation tips"],
                "details": "Key takeaways: Start simple with range-based, move to hash-based for scale, use directory-based for flexibility. Don't shard too early - most apps don't need it until 10M+ records.",
                "screen_recording_notes": ["summary diagram", "decision tree"],
                "graphics": ["takeaway bullets", "10M threshold"]
            }
        ],
        "visual_aids": {
            "b_roll_plan": [
                {"time": "1:00–2:00", "ideas": ["database performance graphs", "slow query visualization"]},
                {"time": "3:00–4:00", "ideas": ["range sharding animation", "hotspot heatmap"]},
                {"time": "5:00–6:00", "ideas": ["hash function visualization", "even distribution demo"]},
                {"time": "8:00–9:00", "ideas": ["Instagram architecture", "Netflix system overview"]}
            ],
            "graphics_list": [
                {"name": "sharding_overview_diagram", "purpose": "explain concept", "appears_at": "1:30"},
                {"name": "range_vs_hash_comparison", "purpose": "compare strategies", "appears_at": "4:30"},
                {"name": "performance_metrics_chart", "purpose": "show improvements", "appears_at": "9:00"}
            ],
            "lower_thirds": ["Database Sharding Expert", "Netflix: 230M users", "Instagram: 500M photos/day"],
            "music": {"vibe": ["clean minimal", "future garage"], "bpm_range": "90–120", "ducking_notes": "VO sidechain −6 dB"},
            "sfx": ["click", "soft pop", "whoosh"]
        },
        "cta": {
            "midroll": "If this helps, hit like so more developers see it.",
            "end": "Grab the full implementation guide → systemdesign.com/sharding?utm_source=youtube&utm_medium=long",
            "end_screen": {"duration_seconds": 20, "elements": ["subscribe", "watch next", "playlist"], "show_handles": True}
        },
        "description": {
            "text": "Database sharding is how Netflix, Instagram, and Twitter handle millions of users without breaking. This comprehensive guide covers the three main sharding strategies, real-world trade-offs, and implementation lessons from the biggest tech companies. You'll learn when to use range-based vs hash-based vs directory-based sharding, how to avoid common pitfalls, and see actual performance improvements from companies scaling to hundreds of millions of users. Perfect for system design interviews and real-world architecture decisions. Key topics covered: database bottlenecks and scaling challenges, range-based sharding with hotspot prevention, hash-based sharding for even distribution, directory-based sharding for maximum flexibility, cross-shard query complexity and solutions, data consistency strategies, operational overhead considerations, Instagram's photo sharding approach, Netflix's multi-strategy implementation, performance metrics and improvements. Whether you're preparing for system design interviews at FAANG companies or architecting real systems, this video gives you the practical knowledge to make informed sharding decisions. Full implementation guide: systemdesign.com/sharding?utm_source=youtube&utm_medium=long",
            "chapters": [
                {"time": "0:00", "title": "Hook & problem"},
                {"time": "0:45", "title": "Background"},
                {"time": "2:15", "title": "Range-based sharding"},
                {"time": "4:00", "title": "Hash-based sharding"},
                {"time": "5:30", "title": "Directory-based sharding"},
                {"time": "7:00", "title": "Trade-offs & pitfalls"},
                {"time": "8:30", "title": "Case study"},
                {"time": "10:00", "title": "Summary & CTA"}
            ],
            "resources": [
                {"title": "Full implementation guide", "url": "systemdesign.com/sharding?utm_source=youtube&utm_medium=long"},
                {"title": "Instagram Engineering Blog", "url": ""},
                {"title": "Netflix Tech Blog", "url": ""}
            ],
            "hashtags": ["#DatabaseSharding", "#SystemDesign", "#ScalableArchitecture"]
        },
        "tags": [
            "database sharding",
            "system design",
            "scalable architecture",
            "distributed systems",
            "database optimization",
            "horizontal scaling",
            "netflix architecture",
            "instagram scaling",
            "database partitioning",
            "system design interview",
            "backend engineering",
            "software architecture",
            "database design",
            "performance optimization",
            "tech interview prep",
            "distributed databases",
            "microservices",
            "database scaling",
            "tech education",
            "software engineering"
        ],
        "image_prompts": [
            {
                "role": "thumb_a",
                "title": "Thumb A — Two-word Punch",
                "prompt": "16:9 thumbnail for Database Sharding Strategies. Two-word punch 'Scale Millions' in bold geometric sans; small database diagram glyph; off-white background; thin vector strokes; subtle dotted grid; blue accent color; generous margins; flat vector; extreme readability on mobile and desktop.",
                "negative_prompt": "no faces, no logos, no neon, no 3D, no glossy gradients, no clutter",
                "style_notes": "poster-like hierarchy; crisp kerning; strong contrast",
                "ratio": "16:9",
                "size_px": "1280x720",
                "alt_text": "Scale Millions with database diagram glyph"
            },
            {
                "role": "thumb_b",
                "title": "Thumb B — Architecture Motif",
                "prompt": "16:9 thumbnail with simplified database sharding architecture for Database Sharding Strategies; 3-4 big arrows showing data flow; 3-5 short labels (Range, Hash, Directory); bold yet minimal; off-white bg; single blue accent; flat vector aesthetic; mobile-first legibility.",
                "negative_prompt": "no photos, no faces, no logos, no heavy gradients",
                "style_notes": "diagram-first; concise labels; high contrast",
                "ratio": "16:9",
                "size_px": "1280x720",
                "alt_text": "Database sharding architecture with flow arrows"
            }
        ],
        "compliance": {
            "est_duration_minutes": 11,
            "title_char_count": 58,
            "chapters_count": 8,
            "description_word_count": 542,
            "tags_count": 20,
            "image_prompt_count": 2,
            "has_tracked_link": True,
            "checks": [
                "intro 0–15s with numeric hook/benefit",
                "outline covers all mandatory beats",
                "chapters have ascending timestamps",
                "script time ranges sum to 8–12 minutes",
                "visual aids & b-roll plan present",
                "description ≥500 words with chapters",
                "EXACTLY 20 tags (no '#')",
                "image_prompts length == image_plan.count (default 2)"
            ]
        }
    }
    
    try:
        # Test direct schema validation
        print("🧪 Testing direct schema validation...")
        long_form_content = YouTubeLongFormContent(**sample_content)
        print(f"✅ Direct schema validation passed")
        print(f"📊 Title length: {len(long_form_content.title)} chars")
        print(f"📋 Chapters count: {len(long_form_content.chapters)}")
        print(f"📝 Script sections: {len(long_form_content.script)}")
        print(f"🏷️ Tags count: {len(long_form_content.tags)}")
        print(f"🖼️ Image prompts count: {len(long_form_content.image_prompts)}")
        print(f"⏱️ Duration: {long_form_content.compliance['est_duration_minutes']} minutes")
        
        # Test schema validator function
        print(f"\n🧪 Testing schema validator function...")
        validated_content = validate_content_schema('youtube', 'long_form', sample_content)
        print(f"✅ Schema validator function passed")
        print(f"📋 Validated content type: {type(validated_content).__name__}")
        
        # Display sample content structure
        print(f"\n📋 Sample YouTube Long Form Structure:")
        print(f"   • Title: {len(sample_content['title'])} characters")
        print(f"   • Outline sections: {len(sample_content['outline'])}")
        print(f"   • Chapters: {len(sample_content['chapters'])} with timestamps")
        print(f"   • Script sections: {len(sample_content['script'])} detailed segments")
        print(f"   • Visual aids: B-roll, graphics, lower thirds")
        print(f"   • Description: {sample_content['compliance']['description_word_count']} words")
        print(f"   • Tags: {len(sample_content['tags'])} keywords")
        print(f"   • Thumbnails: {len(sample_content['image_prompts'])} designs")
        
        return True
        
    except Exception as e:
        print(f"❌ Schema validation failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_direct_schema_instantiation():
    """Test direct instantiation of YouTube Long Form schema"""
    print("\n" + "=" * 60)
    print("TEST 3: Direct YouTube Long Form Schema Instantiation")
    print("=" * 60)
    
    try:
        # Create YouTube Long Form content directly
        long_form_content = YouTubeLongFormContent(
            title="Microservices Architecture: Complete Guide for Scale",
            thumbnail_text="Microservices",
            intro={
                "time_range": "0:00–0:15",
                "narration": "Uber runs 2,200 microservices. Amazon has thousands. Here's the complete guide to building microservices that actually scale.",
                "on_screen_text": "2,200 services",
                "visuals": "punch-in + microservices diagram",
                "b_roll": ["Uber architecture", "Amazon services"],
                "sfx": ["whoosh"],
                "music": {"vibe": ["energetic tech"], "bpm_range": "95–115"}
            },
            outline=[
                {"section": "Hook & problem", "beats": ["2,200 services stat", "Monolith limitations", "What you'll learn"]},
                {"section": "Background", "beats": ["Monolith vs microservices", "When to migrate", "Key principles"]},
                {"section": "Architecture patterns", "beats": ["Service boundaries", "Communication patterns", "Data management"]},
                {"section": "Implementation strategies", "beats": ["API design", "Service discovery", "Load balancing"]},
                {"section": "Trade-offs & challenges", "beats": ["Complexity overhead", "Network latency", "Debugging difficulties"]},
                {"section": "Case study", "beats": ["Uber's migration", "Netflix approach", "Lessons learned"]},
                {"section": "Summary & next steps", "beats": ["Key decisions", "Migration strategy", "Resources"]}
            ],
            chapters=[
                {"index": 1, "name": "Hook & problem", "timestamp": "0:00"},
                {"index": 2, "name": "Background", "timestamp": "0:30"},
                {"index": 3, "name": "Architecture patterns", "timestamp": "2:00"},
                {"index": 4, "name": "Implementation strategies", "timestamp": "4:30"},
                {"index": 5, "name": "Trade-offs & challenges", "timestamp": "6:30"},
                {"index": 6, "name": "Case study", "timestamp": "8:00"},
                {"index": 7, "name": "Summary & next steps", "timestamp": "9:30"}
            ],
            script=[
                {
                    "chapter_index": 1,
                    "time_range": "0:00–0:30",
                    "talking_points": ["2,200 services hook", "scale problem", "video overview"],
                    "details": "Uber runs 2,200 microservices. Amazon has thousands. But most companies fail at microservices. In this video, you'll learn the complete architecture guide.",
                    "screen_recording_notes": ["Uber dashboard", "service map"],
                    "graphics": ["Uber logo", "2,200 stat"]
                },
                {
                    "chapter_index": 2,
                    "time_range": "0:30–2:00",
                    "talking_points": ["monolith limitations", "microservices benefits", "migration timing"],
                    "details": "Monoliths work great until they don't. Single deployments, shared databases, tight coupling. Microservices solve this with independent services, separate databases, loose coupling.",
                    "screen_recording_notes": ["monolith diagram", "microservices comparison"],
                    "graphics": ["architecture comparison", "coupling visualization"]
                }
            ],
            visual_aids={
                "b_roll_plan": [
                    {"time": "1:00–2:00", "ideas": ["monolith vs microservices diagram", "coupling visualization"]},
                    {"time": "3:00–4:00", "ideas": ["service boundary examples", "API communication"]}
                ],
                "graphics_list": [
                    {"name": "microservices_overview", "purpose": "architecture comparison", "appears_at": "1:30"},
                    {"name": "service_communication", "purpose": "API patterns", "appears_at": "4:00"}
                ],
                "lower_thirds": ["Microservices Expert", "Uber: 2,200 services"],
                "music": {"vibe": ["clean minimal"], "bpm_range": "90–120", "ducking_notes": "VO sidechain −6 dB"},
                "sfx": ["click", "pop"]
            },
            cta={
                "midroll": "If this helps, smash that like button.",
                "end": "Get the complete implementation guide → systemdesign.com/microservices?utm_source=youtube&utm_medium=long",
                "end_screen": {"duration_seconds": 20, "elements": ["subscribe", "watch next"], "show_handles": True}
            },
            description={
                "text": "Microservices architecture powers the world's most scalable systems. This comprehensive guide covers everything from service boundaries to implementation strategies, with real examples from Uber, Netflix, and Amazon. You'll learn when to migrate from monoliths, how to design service boundaries, communication patterns, data management strategies, and common pitfalls to avoid. Perfect for system design interviews and real-world architecture decisions. Topics covered include monolith vs microservices trade-offs, service boundary design principles, API communication patterns, service discovery mechanisms, load balancing strategies, data consistency patterns, debugging and monitoring challenges, Uber's 2,200 service architecture, Netflix's approach to microservices, migration strategies and timelines. Whether you're architecting new systems or migrating existing monoliths, this guide provides practical insights for building microservices that scale. Complete implementation guide: systemdesign.com/microservices?utm_source=youtube&utm_medium=long",
                "chapters": [
                    {"time": "0:00", "title": "Hook & problem"},
                    {"time": "0:30", "title": "Background"},
                    {"time": "2:00", "title": "Architecture patterns"},
                    {"time": "4:30", "title": "Implementation strategies"},
                    {"time": "6:30", "title": "Trade-offs & challenges"},
                    {"time": "8:00", "title": "Case study"},
                    {"time": "9:30", "title": "Summary & next steps"}
                ],
                "resources": [
                    {"title": "Complete implementation guide", "url": "systemdesign.com/microservices?utm_source=youtube&utm_medium=long"}
                ],
                "hashtags": ["#Microservices", "#SystemDesign", "#SoftwareArchitecture"]
            },
            tags=[
                "microservices",
                "system design",
                "software architecture",
                "distributed systems",
                "scalable architecture",
                "monolith migration",
                "service boundaries",
                "API design",
                "system design interview",
                "backend engineering",
                "uber architecture",
                "netflix microservices",
                "service discovery",
                "load balancing",
                "data consistency",
                "microservices patterns",
                "distributed architecture",
                "tech interview prep",
                "software engineering",
                "architecture patterns"
            ],
            image_prompts=[
                {
                    "role": "thumb_a",
                    "title": "Thumb A — Two-word Punch",
                    "prompt": "16:9 thumbnail for Microservices Architecture. 'Microservices' in bold sans; small service diagram glyph; off-white bg; blue accent; flat vector; mobile readable.",
                    "negative_prompt": "no faces, no logos, no clutter",
                    "style_notes": "clean hierarchy; strong contrast",
                    "ratio": "16:9",
                    "size_px": "1280x720",
                    "alt_text": "Microservices with service diagram"
                },
                {
                    "role": "thumb_b",
                    "title": "Thumb B — Architecture Motif",
                    "prompt": "16:9 thumbnail with microservices architecture diagram; connected services; flow arrows; minimal labels; off-white bg; blue accent; flat vector.",
                    "negative_prompt": "no photos, no logos, no gradients",
                    "style_notes": "diagram-first; high contrast",
                    "ratio": "16:9",
                    "size_px": "1280x720",
                    "alt_text": "Microservices architecture diagram"
                }
            ],
            compliance={
                "est_duration_minutes": 10,
                "title_char_count": 52,
                "chapters_count": 7,
                "description_word_count": 520,
                "tags_count": 20,
                "image_prompt_count": 2,
                "has_tracked_link": True,
                "checks": [
                    "intro 0–15s with numeric hook/benefit",
                    "outline covers all mandatory beats",
                    "chapters have ascending timestamps",
                    "script time ranges sum to 8–12 minutes",
                    "visual aids & b-roll plan present",
                    "description ≥500 words with chapters",
                    "EXACTLY 20 tags (no '#')",
                    "image_prompts length == image_plan.count (default 2)"
                ]
            }
        )
        
        print(f"✅ Direct schema instantiation successful")
        print(f"📊 YouTube Long Form structure:")
        print(f"   • Title: {len(long_form_content.title)} characters")
        print(f"   • Thumbnail text: '{long_form_content.thumbnail_text}'")
        print(f"   • Outline sections: {len(long_form_content.outline)}")
        print(f"   • Chapters: {len(long_form_content.chapters)}")
        print(f"   • Script sections: {len(long_form_content.script)}")
        print(f"   • Tags: {len(long_form_content.tags)}")
        print(f"   • Thumbnails: {len(long_form_content.image_prompts)}")
        print(f"   • Duration: {long_form_content.compliance['est_duration_minutes']} minutes")
        
        # Test JSON serialization
        json_output = long_form_content.model_dump()
        print(f"✅ JSON serialization successful")
        print(f"📄 JSON size: {len(json.dumps(json_output))} characters")
        
        return True
        
    except Exception as e:
        print(f"❌ Direct schema instantiation failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all YouTube Long Form tests"""
    print("🧪 YOUTUBE LONG FORM CONTENT GENERATION TESTS")
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
        print("🎉 All YouTube Long Form tests passed! Ready for integration.")
    else:
        print("⚠️ Some tests failed. Please review the errors above.")
    
    return passed == len(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)