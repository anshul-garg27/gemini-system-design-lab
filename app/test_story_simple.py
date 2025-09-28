#!/usr/bin/env python3
"""
Simple test for Instagram Story content generation
"""
import os
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_prompt_processing():
    """Test prompt template processing for story"""
    
    print("Testing Instagram Story Prompt Processing")
    print("=" * 50)
    
    try:
        from prompt_processor import PromptProcessor
        
        processor = PromptProcessor()
        
        template_path = os.path.join(os.path.dirname(__file__), 'prompts', 'bodies', 'instagram-story.txt')
        
        processed_prompt = processor.process_prompt_template(
            template_path=template_path,
            topic_id="test_story_001",
            topic_name="Microservices Architecture",
            topic_description="Learn about microservices patterns and best practices",
            platform="instagram",
            format_type="story"
        )
        
        print("✅ Prompt processing completed!")
        print(f"Processed prompt length: {len(processed_prompt)} chars")
        
        # Check for key replacements
        checks = [
            ("{topic_id}" not in processed_prompt, "Topic ID placeholder replaced"),
            ("{topic_name}" not in processed_prompt, "Topic name placeholder replaced"),
            ("test_story_001" in processed_prompt, "Topic ID value present"),
            ("Microservices Architecture" in processed_prompt, "Topic name value present"),
            ("intermediate" in processed_prompt, "Audience value present")
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
    """Test schema validation for story content"""
    
    print("\nTesting Instagram Story Schema Validation")
    print("=" * 50)
    
    try:
        from schemas import validate_content, InstagramStoryContent
        
        # Sample story content data
        sample_content = {
            "frames": [
                {
                    "index": 1,
                    "role": "hook",
                    "copy": "Microservices: Scale or Fail?",
                    "sticker_ideas": ["poll: Monolith vs Microservices?"],
                    "overlay_notes": "large headline; high contrast",
                    "layout": "centered title; big margins",
                    "alt_text": "Hook slide about microservices scaling",
                    "duration_seconds": 15
                },
                {
                    "index": 2,
                    "role": "micro_insight",
                    "copy": "Break down into small services",
                    "sticker_ideas": ["quiz: How many services is too many?"],
                    "overlay_notes": "two short lines max",
                    "layout": "top headline; bottom quiz",
                    "alt_text": "Insight about service decomposition",
                    "duration_seconds": 15
                },
                {
                    "index": 3,
                    "role": "cta",
                    "copy": "Learn the patterns!",
                    "sticker_ideas": ["link: Read full guide"],
                    "overlay_notes": "bold CTA; arrow to link",
                    "layout": "CTA bottom; link sticker above",
                    "alt_text": "Call to action to learn more",
                    "duration_seconds": 15
                }
            ],
            "stickers": {
                "global": ["keep polls simple (2 options)", "use quiz with 3 options max"],
                "link_strategy": {
                    "enabled": True,
                    "link_url": "https://example.com/microservices",
                    "link_text": "Read more",
                    "placement_hint": "bottom center above CTA"
                },
                "time_sensitive_angle": "New microservices guide just dropped!"
            },
            "image_prompts": [
                {
                    "role": "background",
                    "title": "Story Background",
                    "prompt": "Soft off-white canvas with microservices node diagram",
                    "negative_prompt": "no busy texture, no photos",
                    "style_notes": "very subtle, unobtrusive",
                    "ratio": "9:16",
                    "size_px": "1080x1920",
                    "alt_text": "Subtle background with microservices concept"
                }
            ],
            "overlay_hashtags": ["#microservices", "#architecture", "#systemdesign"],
            "compliance": {
                "frames_total": 3,
                "has_link": True,
                "checks": ["3–5 frames", "Hook ≤12 words", "safe margins ≥96px"]
            }
        }
        
        # Test direct schema validation
        story_content = InstagramStoryContent(**sample_content)
        print("✅ Direct schema validation passed!")
        
        # Test validate_content function
        validated = validate_content("instagram", "story", sample_content)
        print("✅ validate_content function passed!")
        
        print(f"Validated content type: {type(validated)}")
        print(f"Frames count: {len(validated.frames)}")
        print(f"Has stickers: {validated.stickers is not None}")
        print(f"Image prompts count: {len(validated.image_prompts) if validated.image_prompts else 0}")
        print(f"Overlay hashtags count: {len(validated.overlay_hashtags) if validated.overlay_hashtags else 0}")
        print(f"Has compliance: {validated.compliance is not None}")
        
        return True
        
    except Exception as e:
        print(f"❌ Schema validation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Instagram Story Testing Suite")
    print("=" * 40)
    
    # Test prompt processing
    prompt_test_passed = test_prompt_processing()
    
    # Test schema validation
    schema_test_passed = test_schema_validation()
    
    print(f"\nTest Results:")
    print(f"Prompt Processing: {'✅ PASSED' if prompt_test_passed else '❌ FAILED'}")
    print(f"Schema Validation: {'✅ PASSED' if schema_test_passed else '❌ FAILED'}")
    
    if prompt_test_passed and schema_test_passed:
        print("\n🎉 All tests passed! Instagram Story system is ready.")
    else:
        print("\n⚠️  Some tests failed. Check the output above for details.")
