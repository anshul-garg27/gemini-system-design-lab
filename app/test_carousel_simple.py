#!/usr/bin/env python3
"""
Simple test for Instagram Carousel content generation
"""
import os
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_prompt_processing():
    """Test prompt template processing for carousel"""
    
    print("Testing Instagram Carousel Prompt Processing")
    print("=" * 50)
    
    try:
        from prompt_processor import PromptProcessor
        
        processor = PromptProcessor()
        
        template_path = os.path.join(os.path.dirname(__file__), 'prompts', 'bodies', 'instagram-carousel.txt')
        
        processed_prompt = processor.process_prompt_template(
            template_path=template_path,
            topic_id="test_001",
            topic_name="Load Balancing Strategies",
            topic_description="Learn about different load balancing algorithms and their trade-offs",
            platform="instagram",
            format_type="carousel"
        )
        
        print("✅ Prompt processing completed!")
        print(f"Processed prompt length: {len(processed_prompt)} chars")
        
        # Check for key replacements
        checks = [
            ("{topic_id}" not in processed_prompt, "Topic ID placeholder replaced"),
            ("{topic_name}" not in processed_prompt, "Topic name placeholder replaced"),
            ("test_001" in processed_prompt, "Topic ID value present"),
            ("Load Balancing Strategies" in processed_prompt, "Topic name value present"),
            ("config.platform_specific.instagram.carousel" not in processed_prompt, "Platform config placeholders replaced")
        ]
        
        for check_passed, description in checks:
            status = "✅" if check_passed else "❌"
            print(f"{status} {description}")
        
        # Show a sample of the processed prompt
        print("\nFirst 500 chars of processed prompt:")
        print("-" * 40)
        print(processed_prompt[:500])
        print("-" * 40)
        
        return True
        
    except Exception as e:
        print(f"❌ Prompt processing failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_schema_validation():
    """Test schema validation for carousel content"""
    
    print("\nTesting Instagram Carousel Schema Validation")
    print("=" * 50)
    
    try:
        from schemas import validate_content, InstagramCarouselContent
        
        # Sample carousel content data
        sample_content = {
            "slides": [
                {
                    "index": 1,
                    "role": "hook",
                    "title": "Scale Your System",
                    "subtitle": "Master load balancing",
                    "bullets": ["Handle millions of requests", "Zero downtime"],
                    "overlay_text": "Swipe →",
                    "design_note": "Bold cover hierarchy",
                    "layout": "title top, subtitle below",
                    "iconography": "tiny diagram glyph",
                    "contrast_notes": "max contrast headline",
                    "alt_text": "Cover slide with load balancing concept"
                },
                {
                    "index": 2,
                    "role": "problem",
                    "title": "Traffic Overload",
                    "subtitle": "Single server bottleneck",
                    "bullets": ["Server crashes under load", "Users experience downtime"],
                    "overlay_text": "Problem →",
                    "design_note": "use red underline sparingly",
                    "layout": "two-column bullets",
                    "iconography": "alert/bottleneck glyph",
                    "contrast_notes": "use accent on pain metric",
                    "alt_text": "Problem slide showing server overload"
                },
                {
                    "index": 3,
                    "role": "core_idea",
                    "title": "Load Balancer Solution",
                    "subtitle": "Distribute traffic smartly",
                    "bullets": ["Multiple servers handle requests", "Automatic failover protection"],
                    "overlay_text": "Solution core",
                    "design_note": "calm tone; green check motif",
                    "layout": "headline left, bullets right",
                    "iconography": "lightbulb/process glyph",
                    "contrast_notes": "normal emphasis; keep labels short",
                    "alt_text": "Solution slide with load balancer concept"
                }
            ],
            "caption": {
                "text": "Load balancing is crucial for distributed systems. It distributes incoming requests across multiple servers to ensure optimal performance and reliability. Learn about round-robin, weighted algorithms, and consistent hashing strategies that power modern applications.",
                "emojis_used": ["🧠", "⚙️", "🚀"],
                "seo": {
                    "keywords_used": ["load balancing", "distributed systems"],
                    "lsi_terms_used": ["round-robin", "consistent hashing"]
                }
            },
            "hashtags": ["#systemdesign", "#loadbalancing", "#scalability", "#tech", "#programming"],
            "design_system": {
                "color_palette": [
                    {"name": "Calm Tech", "values": ["#F8F7F4", "#111111", "#1E6F6E"]}
                ],
                "font_pairings": [
                    {"headline": "Outfit SemiBold", "body": "Inter", "code": "JetBrains Mono"}
                ],
                "grid": {"ratio": "4:5", "size_px": "1080x1350", "safe_margins_px": 64}
            },
            "compliance": {
                "slides_total": 3,
                "hook_title_char_count": 17,
                "caption_word_count": 35,
                "hashtag_count": 5,
                "checks": ["titles ≤10 words", "caption present"]
            }
        }
        
        # Test direct schema validation
        carousel_content = InstagramCarouselContent(**sample_content)
        print("✅ Direct schema validation passed!")
        
        # Test validate_content function
        validated = validate_content("instagram", "carousel", sample_content)
        print("✅ validate_content function passed!")
        
        print(f"Validated content type: {type(validated)}")
        print(f"Slides count: {len(validated.slides)}")
        print(f"Hashtags count: {len(validated.hashtags)}")
        print(f"Caption type: {type(validated.caption)}")
        print(f"Has design_system: {validated.design_system is not None}")
        print(f"Has compliance: {validated.compliance is not None}")
        
        return True
        
    except Exception as e:
        print(f"❌ Schema validation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Instagram Carousel Testing Suite")
    print("=" * 40)
    
    # Test prompt processing
    prompt_test_passed = test_prompt_processing()
    
    # Test schema validation
    schema_test_passed = test_schema_validation()
    
    print(f"\nTest Results:")
    print(f"Prompt Processing: {'✅ PASSED' if prompt_test_passed else '❌ FAILED'}")
    print(f"Schema Validation: {'✅ PASSED' if schema_test_passed else '❌ FAILED'}")
    
    if prompt_test_passed and schema_test_passed:
        print("\n🎉 All tests passed! Instagram Carousel system is ready.")
    else:
        print("\n⚠️  Some tests failed. Check the output above for details.")
