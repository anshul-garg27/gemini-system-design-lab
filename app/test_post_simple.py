#!/usr/bin/env python3
"""
Simple test for Instagram Post content generation
Tests prompt processing and schema validation
"""

import sys
import os
import json
from pathlib import Path

# Add the app directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from prompt_processor import PromptProcessor
from schemas import validate_content, InstagramPostContent

def test_instagram_post_prompt_processing():
    """Test Instagram Post prompt template processing"""
    print("=== Testing Instagram Post Prompt Processing ===")
    
    # Initialize processor
    processor = PromptProcessor()
    
    # Test data
    test_topic_name = "How to build a personal brand on social media in 2024"
    test_topic_description = "Learn effective strategies for building and maintaining a strong personal brand across social media platforms in 2024"
    
    try:
        # Get template path
        template_path = os.path.join(os.path.dirname(__file__), 'prompts', 'bodies', 'instagram-post.txt')
        
        # Process prompt
        processed_prompt = processor.process_prompt_template(
            template_path=template_path,
            topic_id="test_post_001",
            topic_name=test_topic_name,
            topic_description=test_topic_description,
            platform="instagram",
            format_type="post"
        )
        
        print(f"✓ Prompt processed successfully")
        print(f"Topic: {test_topic_name}")
        print(f"Processed prompt length: {len(processed_prompt)} characters")
        
        # Check that topic was replaced
        if test_topic_name in processed_prompt:
            print(f"✓ Topic replacement successful")
        else:
            print(f"✗ Topic replacement failed")
            return False
            
        # Check for key Instagram Post elements
        required_elements = [
            "Instagram Post",
            "visual_concept",
            "caption",
            "hashtags",
            "hashtags_grouped", 
            "location_tag_suggestions",
            "image_prompts",
            "compliance"
        ]
        
        missing_elements = []
        for element in required_elements:
            if element not in processed_prompt:
                missing_elements.append(element)
        
        if missing_elements:
            print(f"✗ Missing required elements: {missing_elements}")
            return False
        else:
            print(f"✓ All required elements present")
            
        return True
        
    except Exception as e:
        print(f"✗ Error processing prompt: {e}")
        return False

def test_instagram_post_schema_validation():
    """Test Instagram Post schema validation with sample data"""
    print("\n=== Testing Instagram Post Schema Validation ===")
    
    # Sample Instagram Post content that matches expected schema
    sample_content = {
        "visual_concept": "Minimalist diagram focused on personal brand building with central hub and connected elements.",
        "caption": {
            "first_line_hook": "Your personal brand is your most valuable asset in 2024 💡",
            "text": "Building a strong personal brand isn't about being perfect—it's about being authentic and consistent. Here are 5 key strategies that transformed my online presence:\n\n1. Define your unique value proposition\n2. Share your expertise consistently\n3. Engage genuinely with your community\n4. Tell your story through visuals\n5. Stay true to your values\n\nRemember: People don't just buy products, they buy into people and stories. Your personal brand is what people say about you when you're not in the room.",
            "cta": "Save & read more → example.com?utm_source=instagram&utm_medium=post",
            "seo": {
                "keywords_used": ["personal brand", "social media", "brand building"],
                "lsi_terms_used": ["online presence", "content strategy"]
            }
        },
        "hashtags": [
            "#PersonalBranding", "#SocialMediaStrategy", "#ContentCreator", "#DigitalMarketing",
            "#PersonalBrand", "#OnlinePresence", "#SocialMedia2024", "#BrandBuilding",
            "#ContentStrategy", "#InfluencerMarketing", "#PersonalDevelopment", "#BusinessTips",
            "#MarketingTips", "#SocialMediaTips", "#BrandStrategy", "#OnlineBusiness",
            "#ContentMarketing", "#DigitalBranding", "#SocialMediaGrowth", "#PersonalGrowth",
            "#BrandYourself", "#SocialMediaInfluencer", "#ContentCreation", "#MarketingStrategy",
            "#BrandAwareness", "#SocialMediaExpert", "#DigitalInfluencer", "#OnlineMarketing",
            "#PersonalBrandTips", "#SocialMediaSuccess"
        ],
        "hashtags_grouped": {
            "broad": [
                "#PersonalBranding", "#SocialMediaStrategy", "#ContentCreator", "#DigitalMarketing",
                "#PersonalBrand", "#OnlinePresence", "#SocialMedia2024", "#BrandBuilding"
            ],
            "niche": [
                "#ContentStrategy", "#InfluencerMarketing", "#PersonalDevelopment", "#BusinessTips",
                "#MarketingTips", "#SocialMediaTips", "#BrandStrategy", "#OnlineBusiness",
                "#ContentMarketing", "#DigitalBranding"
            ],
            "micro_niche": [
                "#SocialMediaGrowth", "#PersonalGrowth", "#BrandYourself", "#SocialMediaInfluencer",
                "#ContentCreation", "#MarketingStrategy", "#BrandAwareness", "#SocialMediaExpert"
            ],
            "intent": [
                "#DigitalInfluencer", "#OnlineMarketing", "#PersonalBrandTips", "#SocialMediaSuccess"
            ],
            "branded": []
        },
        "location_tag_suggestions": [
            {
                "name": "New York, NY",
                "type": "city",
                "reason": "Major business hub for personal branding"
            },
            {
                "name": "San Francisco, CA",
                "type": "city", 
                "reason": "Tech industry center"
            },
            {
                "name": "Social Media Week",
                "type": "event",
                "reason": "Relevant industry event"
            }
        ],
        "image_prompts": [
            {
                "role": "visual_diagram",
                "title": "Post Visual A — Minimal Diagram",
                "prompt": "Minimalist 4:5 diagram for personal brand building focused on central hub with connected elements. Composition: central circle labeled 'YOU' with 5 connected nodes for key strategies; off-white background; thin vector strokes; subtle dotted grid; single blue accent color; generous margins; flat vector aesthetic; mobile legible.",
                "negative_prompt": "no photos, no faces, no logos, no neon, no 3D bevels, no gradients >5%, no clutter",
                "style_notes": "diagram-first; clear hierarchy; tight labels",
                "ratio": "4:5",
                "size_px": "1080x1350",
                "alt_text": "Diagram visual emphasizing personal brand building strategy"
            },
            {
                "role": "visual_typography",
                "title": "Post Visual B — Typographic Insight Card",
                "prompt": "Typographic 4:5 insight card for personal brand building. Bold headline 'BUILD YOUR BRAND 2024'; small inset micro-diagram (tiny network motif) at bottom corner; off-white background; single blue accent underline; generous whitespace; flat vector; high legibility on mobile.",
                "negative_prompt": "no photos, no heavy gradients, no logos",
                "style_notes": "editorial poster feel; crisp kerning",
                "ratio": "4:5",
                "size_px": "1080x1350",
                "alt_text": "Typographic card with small diagram inset"
            }
        ],
        "compliance": {
            "caption_word_count": 156,
            "first_line_hook_char_count": 54,
            "hashtag_count": 30,
            "image_prompt_count": 2,
            "checks": [
                "caption 120–200 words (150–200 preferred)",
                "strong first line; no 'click more' bait",
                "exactly 30 hashtags (unique; tier-mixed)",
                "image_prompts length == image_plan.count (default 2)",
                "safe margins ≥64px",
                "CTA present once"
            ]
        }
    }
    
    try:
        # Test schema validation
        validated_content = validate_content('instagram', 'post', sample_content)
        
        print(f"✓ Schema validation successful")
        print(f"Content type: {type(validated_content).__name__}")
        
        # Test specific field access
        print(f"✓ Visual concept: {validated_content.visual_concept[:50]}...")
        print(f"✓ Caption hook: {validated_content.caption['first_line_hook']}")
        print(f"✓ Hashtag count: {len(validated_content.hashtags)}")
        print(f"✓ Location tags: {len(validated_content.location_tag_suggestions)}")
        print(f"✓ Image variants: {len(validated_content.image_prompts)}")
        
        # Validate compliance data
        if validated_content.compliance:
            compliance = validated_content.compliance
            print(f"✓ Compliance tracking: {len(compliance.get('checks', []))} checks")
        
        return True
        
    except Exception as e:
        print(f"✗ Schema validation failed: {e}")
        return False

def test_direct_schema_instantiation():
    """Test direct InstagramPostContent schema instantiation"""
    print("\n=== Testing Direct Schema Instantiation ===")
    
    try:
        # Create 30 hashtags for testing
        test_hashtags = [f"#test{i}" for i in range(1, 31)]
        
        # Test minimal valid content
        minimal_content = InstagramPostContent(
            visual_concept="Test visual concept",
            caption={
                "first_line_hook": "Test hook",
                "text": "Test content",
                "cta": "Test CTA",
                "seo": {"keywords_used": [], "lsi_terms_used": []}
            },
            hashtags=test_hashtags,
            hashtags_grouped={
                "broad": test_hashtags[:8],
                "niche": test_hashtags[8:18], 
                "micro_niche": test_hashtags[18:26],
                "intent": test_hashtags[26:30],
                "branded": []
            },
            location_tag_suggestions=[
                {"name": "Test Location", "type": "city", "reason": "test"}
            ],
            image_prompts=[
                {"role": "visual_diagram", "title": "Test A", "prompt": "Test prompt 1", "ratio": "4:5", "size_px": "1080x1350"},
                {"role": "visual_typography", "title": "Test B", "prompt": "Test prompt 2", "ratio": "4:5", "size_px": "1080x1350"}
            ],
            compliance={
                "caption_word_count": 10,
                "first_line_hook_char_count": 9,
                "hashtag_count": 30,
                "image_prompt_count": 2,
                "checks": ["test check"]
            }
        )
        
        print(f"✓ Direct schema instantiation successful")
        print(f"✓ Visual concept: {minimal_content.visual_concept}")
        print(f"✓ Caption keys: {list(minimal_content.caption.keys())}")
        print(f"✓ Hashtag groups: {list(minimal_content.hashtags_grouped.keys())}")
        
        return True
        
    except Exception as e:
        print(f"✗ Direct schema instantiation failed: {e}")
        return False

def main():
    """Run all tests"""
    print("Instagram Post Content Generation Tests")
    print("=" * 50)
    
    tests = [
        test_instagram_post_prompt_processing,
        test_instagram_post_schema_validation,
        test_direct_schema_instantiation
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"✗ Test {test.__name__} failed with exception: {e}")
            results.append(False)
    
    # Summary
    print(f"\n{'='*50}")
    print(f"Test Results: {sum(results)}/{len(results)} passed")
    
    if all(results):
        print("🎉 All Instagram Post tests passed!")
        return True
    else:
        print("❌ Some tests failed")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
