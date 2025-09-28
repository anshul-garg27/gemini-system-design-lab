#!/usr/bin/env python3
"""
Test suite for Telegram Post content generation format.
Tests prompt processing, schema validation, and direct schema instantiation.
"""

import json
import sys
import os
from pathlib import Path

# Add the app directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent))

from schemas import validate_content, TelegramPostContent


def load_prompt_template():
    """Load the Telegram post prompt template."""
    prompt_path = Path(__file__).parent / "prompts" / "bodies" / "telegram-post.txt"
    with open(prompt_path, 'r', encoding='utf-8') as f:
        return f.read()


def test_prompt_processing():
    """Test that the prompt template loads and processes correctly."""
    print("=== Test 1: Prompt Template Processing ===")
    
    try:
        prompt_template = load_prompt_template()
        
        # Verify key sections exist
        assert "Telegram channel post" in prompt_template
        assert "platform=\"telegram\"" in prompt_template
        assert "format=\"post\"" in prompt_template
        assert "prompt_version=\"tg-post-1.2\"" in prompt_template
        
        # Verify Telegram-specific requirements
        assert "90–160 characters" in prompt_template
        assert "extended variant (300–500 chars)" in prompt_template
        assert "short URL with UTM" in prompt_template
        assert "rich link preview" in prompt_template
        assert "1–3 tasteful emojis" in prompt_template
        assert "3–8 compact channel tags" in prompt_template
        assert "exactly **2** square prompts" in prompt_template
        
        # Verify compliance requirements
        assert "instant_view_hint" in prompt_template
        assert "1080×1080" in prompt_template
        assert "square_headline" in prompt_template
        assert "square_checklist" in prompt_template
        
        print("✓ Prompt template loaded successfully")
        print(f"✓ Template length: {len(prompt_template)} characters")
        print("✓ All required Telegram sections present")
        
    except Exception as e:
        print(f"✗ Prompt processing failed: {e}")
        return False
    
    return True


def test_schema_validation():
    """Test schema validation with realistic Telegram post content."""
    print("\n=== Test 2: Schema Validation ===")
    
    # Realistic Telegram post sample data
    sample_content = {
        "post": "🚀 Docker containers scale better with proper resource limits. Quick setup guide inside! https://t.ly/docker-limits",
        "alt_versions": [
            "⚙️ Set Docker memory & CPU limits for stable scaling. Essential config tips here: https://t.ly/docker-limits",
            "🧠 Docker resource management made simple. Prevent container crashes with these settings: https://t.ly/docker-limits"
        ],
        "extended_post": "Most Docker crashes happen because of unlimited resource usage. Here's the fix: Set memory limits with --memory=512m and CPU limits with --cpus=1.5 in your docker run commands. For docker-compose, use mem_limit and cpus_limit in your service definitions. This prevents one container from consuming all system resources and crashing your entire stack. Pro tip: Monitor with docker stats to find optimal limits for your specific workloads.",
        "link": {
            "url": "https://systemdesign.com/docker-resources?utm_source=telegram&utm_medium=post",
            "short": "https://t.ly/docker-limits",
            "preview": {
                "title_hint": "Docker Resource Limits: Complete Setup Guide",
                "description_hint": "Learn to set memory and CPU limits for Docker containers. Prevent crashes and improve stability with proper resource management.",
                "enable_preview": True
            },
            "instant_view_hint": "likely",
            "fallback": "If no IV, pin the key quote: 'Set memory limits with --memory=512m and CPU limits with --cpus=1.5'"
        },
        "hashtags": ["#docker", "#containers", "#devops", "#scaling", "#performance"],
        "emoji_suggestions": ["🚀", "⚙️", "🧠"],
        "image_prompts": [
            {
                "role": "square_headline",
                "title": "TG Square A",
                "prompt": "1:1 minimalist insight card for Docker Resource Limits. Big 2–4 word headline 'Resource Limits' centered; small container diagram glyph in bottom-right corner; off-white background; subtle dotted grid; thin vector strokes; blue accent color for headline underline; generous margins; flat vector aesthetic; mobile-first legibility.",
                "negative_prompt": "no photos, no faces, no logos, no neon, no 3D bevels, no glossy gradients, no clutter",
                "style_notes": "editorial poster; strong kerning; bold but airy",
                "ratio": "1:1",
                "size_px": "1080x1080",
                "alt_text": "Square headline card with tiny container diagram glyph"
            },
            {
                "role": "square_checklist",
                "title": "TG Square B",
                "prompt": "1:1 checklist motif for Docker Resource Limits. Three short ticks with labels: 'Memory Limit', 'CPU Limit', 'Monitor Usage'; thin vector check icons; off-white background; subtle grid; blue accent color for ticks; keep padding generous; flat vector; high contrast text.",
                "negative_prompt": "no busy patterns, no gradients >5%, no photos, no logos",
                "style_notes": "calm minimal; readable at small sizes",
                "ratio": "1:1",
                "size_px": "1080x1080",
                "alt_text": "Square checklist with three Docker resource management ticks"
            }
        ],
        "compliance": {
            "post_char_count": 118,
            "alt_versions_count": 2,
            "extended_post_char_count": 456,
            "has_single_tracked_link": True,
            "hashtags_count": 5,
            "emoji_count_main": 1,
            "image_prompt_count": 2,
            "checks": [
                "main post 90–160 chars with ≤3 emojis",
                "exactly one short link appended (uses tracked url in `link.url`)",
                "3–8 hashtags, lowercase, concise",
                "extended_post 300–500 chars if included; no extra links",
                "image_prompts length == image_plan.count (default 2 squares)",
                "link preview enabled with title/description hints",
                "instant_view_hint set and fallback provided"
            ]
        }
    }
    
    try:
        # Test schema validation
        validated_content = validate_content('telegram', 'post', sample_content)
        
        print("✓ Schema validation passed")
        print(f"✓ Main post: {validated_content.post}")
        print(f"✓ Post length: {len(validated_content.post)} chars")
        print(f"✓ Alt versions count: {len(validated_content.alt_versions)}")
        print(f"✓ Extended post length: {len(validated_content.extended_post)} chars")
        print(f"✓ Hashtags count: {len(validated_content.hashtags)}")
        
        # Verify Telegram-specific constraints
        assert 90 <= len(validated_content.post) <= 160
        assert len(validated_content.alt_versions) == 2
        assert all(len(alt) <= 160 for alt in validated_content.alt_versions)
        if validated_content.extended_post:
            assert 300 <= len(validated_content.extended_post) <= 500
        assert 3 <= len(validated_content.hashtags) <= 8
        assert 1 <= len(validated_content.emoji_suggestions) <= 3
        assert len(validated_content.image_prompts) == 2
        
        print("✓ All Telegram constraints validated")
        
    except Exception as e:
        print(f"✗ Schema validation failed: {e}")
        return False
    
    return True


def test_direct_schema_instantiation():
    """Test direct schema instantiation and JSON serialization."""
    print("\n=== Test 3: Direct Schema Instantiation ===")
    
    # Minimal valid Telegram post data
    minimal_data = {
        "post": "🔧 Quick Docker tip: Use --memory=512m to prevent container crashes. More tips: https://t.ly/tips",
        "alt_versions": [
            "⚡ Docker memory limits prevent system crashes. Essential setup guide: https://t.ly/tips",
            "🛠️ Set Docker resource limits for stable deployments. Quick tutorial: https://t.ly/tips"
        ],
        "extended_post": "",
        "link": {
            "url": "https://example.com/docker-tips?utm_source=telegram&utm_medium=post",
            "short": "https://t.ly/tips",
            "preview": {
                "title_hint": "Docker Tips: Resource Management",
                "description_hint": "Essential Docker resource management tips for stable container deployments.",
                "enable_preview": True
            },
            "instant_view_hint": "unknown",
            "fallback": "If no IV, attach the square checklist image."
        },
        "hashtags": ["#docker", "#devops", "#tips"],
        "emoji_suggestions": ["🔧", "⚡", "🛠️"],
        "image_prompts": [],
        "compliance": {
            "post_char_count": 95,
            "alt_versions_count": 2,
            "extended_post_char_count": 0,
            "has_single_tracked_link": True,
            "hashtags_count": 3,
            "emoji_count_main": 1,
            "image_prompt_count": 0,
            "checks": []
        }
    }
    
    try:
        # Test direct instantiation
        telegram_post = TelegramPostContent(**minimal_data)
        
        print("✓ Direct schema instantiation successful")
        print(f"✓ Main post: {telegram_post.post}")
        print(f"✓ Link URL: {telegram_post.link['url']}")
        
        # Test JSON serialization
        json_output = telegram_post.model_dump_json(indent=2)
        parsed_back = json.loads(json_output)
        
        print("✓ JSON serialization successful")
        print(f"✓ JSON length: {len(json_output)} characters")
        
        # Verify structure preservation
        assert parsed_back['post'] == minimal_data['post']
        assert parsed_back['alt_versions'] == minimal_data['alt_versions']
        assert parsed_back['link']['url'] == minimal_data['link']['url']
        assert parsed_back['hashtags'] == minimal_data['hashtags']
        
        print("✓ JSON structure preserved correctly")
        
    except Exception as e:
        print(f"✗ Direct instantiation failed: {e}")
        return False
    
    return True


def main():
    """Run all tests for Telegram post format."""
    print("Telegram Post Format - Test Suite")
    print("=" * 50)
    
    tests = [
        test_prompt_processing,
        test_schema_validation,
        test_direct_schema_instantiation
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        else:
            print("Test failed, stopping execution.")
            break
    
    print(f"\n=== Test Results ===")
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! Telegram post format is ready for use.")
        return True
    else:
        print("❌ Some tests failed. Please check the implementation.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
