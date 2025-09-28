#!/usr/bin/env python3
"""
Simple test for LinkedIn Post content generation
Tests prompt processing and schema validation
"""

import sys
import os
import json
from pathlib import Path

# Add the app directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from prompt_processor import PromptProcessor
from schemas import validate_content, LinkedInPostContent

def test_linkedin_post_prompt_processing():
    """Test LinkedIn Post prompt template processing"""
    print("=== Testing LinkedIn Post Prompt Processing ===")
    
    # Initialize processor
    processor = PromptProcessor()
    
    # Test data
    test_topic_name = "Building scalable microservices architecture"
    test_topic_description = "Learn key principles and patterns for designing and implementing scalable microservices systems that can handle enterprise-level traffic"
    
    try:
        # Get template path
        template_path = os.path.join(os.path.dirname(__file__), 'prompts', 'bodies', 'linkedin-post.txt')
        
        # Process prompt
        processed_prompt = processor.process_prompt_template(
            template_path=template_path,
            topic_id="test_linkedin_001",
            topic_name=test_topic_name,
            topic_description=test_topic_description,
            platform="linkedin",
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
            
        # Check for key LinkedIn Post elements
        required_elements = [
            "LinkedIn post",
            "hook",
            "context",
            "key_insights",
            "mini_example",
            "cta",
            "question",
            "body",
            "hashtags_grouped",
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

def test_linkedin_post_schema_validation():
    """Test LinkedIn Post schema validation with sample data"""
    print("\n=== Testing LinkedIn Post Schema Validation ===")
    
    # Sample LinkedIn Post content that matches expected schema
    sample_content = {
        "hook": "🚀 Scaling from 1K to 1M users taught me 3 hard lessons about microservices.\n\nMost teams get the architecture wrong from day one.",
        "context": "When Netflix moved from monolith to microservices, they didn't just split code—they transformed their entire engineering culture. The same principles that work for them can work for your team, but only if you avoid these common pitfalls.",
        "key_insights": [
            "Start with a modular monolith, not microservices",
            "Design for failure from day one—every service will go down",
            "Invest heavily in observability before you need it",
            "Conway's Law is real—your architecture mirrors your org structure",
            "Data consistency is harder than you think—plan for eventual consistency"
        ],
        "mini_example": "Uber's early mistake: They split their monolith too early and spent 2 years rebuilding their service mesh just to handle basic communication between 100+ services.",
        "cta": "What's your biggest microservices challenge? Share in the comments 👇",
        "question": "Have you experienced the pain of premature microservices optimization? What would you do differently?",
        "body": "🚀 Scaling from 1K to 1M users taught me 3 hard lessons about microservices.\n\nMost teams get the architecture wrong from day one.\n\nWhen Netflix moved from monolith to microservices, they didn't just split code—they transformed their entire engineering culture. The same principles that work for them can work for your team, but only if you avoid these common pitfalls.\n\nKey lessons:\n• Start with a modular monolith, not microservices\n• Design for failure from day one—every service will go down\n• Invest heavily in observability before you need it\n• Conway's Law is real—your architecture mirrors your org structure\n• Data consistency is harder than you think—plan for eventual consistency\n\nUber's early mistake: They split their monolith too early and spent 2 years rebuilding their service mesh just to handle basic communication between 100+ services.\n\nWhat's your biggest microservices challenge? Share in the comments 👇\n\nHave you experienced the pain of premature microservices optimization? What would you do differently?\n\nRead more: example.com?utm_source=linkedin&utm_medium=post",
        "chars_count": 1247,
        "hashtags": [
            "#microservices",
            "#systemdesign", 
            "#softwarearchitecture",
            "#scalability",
            "#engineering",
            "#tech"
        ],
        "hashtags_grouped": {
            "broad": ["#systemdesign", "#softwarearchitecture", "#engineering"],
            "niche": ["#microservices", "#scalability", "#distributedystems"],
            "micro_niche": ["#servicemesh", "#observability"],
            "intent": ["#tech"],
            "branded": []
        },
        "alt_versions": {
            "short": "🚀 3 hard lessons from scaling to 1M users:\n\n• Start with modular monolith, not microservices\n• Design for failure from day one\n• Invest in observability early\n\nUber's mistake: Split too early, spent 2 years rebuilding.\n\nWhat's your biggest microservices challenge? 👇",
            "long": "🚀 Scaling from 1K to 1M users taught me 3 hard lessons about microservices.\n\nMost teams get the architecture wrong from day one.\n\nWhen Netflix moved from monolith to microservices, they didn't just split code—they transformed their entire engineering culture. The same principles that work for them can work for your team, but only if you avoid these common pitfalls.\n\nKey lessons:\n• Start with a modular monolith, not microservices\n• Design for failure from day one—every service will go down\n• Invest heavily in observability before you need it\n• Conway's Law is real—your architecture mirrors your org structure\n• Data consistency is harder than you think—plan for eventual consistency\n\nUber's early mistake: They split their monolith too early and spent 2 years rebuilding their service mesh just to handle basic communication between 100+ services.\n\nWhat's your biggest microservices challenge? Share in the comments 👇\n\nHave you experienced the pain of premature microservices optimization? What would you do differently?\n\nRead more: example.com?utm_source=linkedin&utm_medium=post"
        },
        "image_prompts": [
            {
                "role": "card_a",
                "title": "LI Card A — Microservices Insight",
                "prompt": "Corporate-clean insight card for microservices architecture. Short headline 'Start Modular, Scale Smart' top-left; small service diagram motif at right showing connected nodes; off-white background; thin vector strokes; subtle dotted grid; single blue accent color; generous margins; flat vector aesthetic; export sharp for 1200x627.",
                "negative_prompt": "no stock-photo people, no logos, no neon, no 3D, no glossy gradients, no clutter",
                "style_notes": "mobile and desktop legible; clear hierarchy",
                "ratio": "1.91:1",
                "size_px": "1200x627",
                "alt_text": "Insight card about microservices with service diagram"
            },
            {
                "role": "card_b",
                "title": "LI Card B — Architecture Evolution",
                "prompt": "Architecture evolution mini-map showing progression from monolith to microservices: simple flow with 3 stages (Monolith → Modular → Services) with arrows; add 2 metric chips showing scale; off-white background; thin lines; blue accent; subtle grid; generous whitespace; export flat vector for 1350x1080.",
                "negative_prompt": "no 3D, no photoreal elements, no logos",
                "style_notes": "diagram-first; concise labels; high contrast",
                "ratio": "5:4",
                "size_px": "1350x1080",
                "alt_text": "Architecture evolution diagram with scaling metrics"
            }
        ],
        "doc_carousel_outline": {
            "enabled": False,
            "ratio": "4:5",
            "size_px": "1080x1350",
            "slides": []
        },
        "compliance": {
            "hashtags_count": 6,
            "image_prompt_count": 2,
            "body_chars_count": 1247,
            "checks": [
                "hook 2–3 lines",
                "3–5 insights present",
                "one mini example present",
                "single CTA + thoughtful question",
                "5–8 professional hashtags",
                "image_prompts length == image_plan.count",
                "no spammy phrasing or hashtag stuffing"
            ]
        }
    }
    
    try:
        # Test schema validation
        validated_content = validate_content('linkedin', 'post', sample_content)
        
        print(f"✓ Schema validation successful")
        print(f"Content type: {type(validated_content).__name__}")
        
        # Test specific field access
        print(f"✓ Hook: {validated_content.hook[:50]}...")
        print(f"✓ Key insights count: {len(validated_content.key_insights)}")
        print(f"✓ Hashtag count: {len(validated_content.hashtags)}")
        print(f"✓ Character count: {validated_content.chars_count}")
        print(f"✓ Image prompts: {len(validated_content.image_prompts)}")
        
        # Validate compliance data
        if validated_content.compliance:
            compliance = validated_content.compliance
            print(f"✓ Compliance tracking: {len(compliance.get('checks', []))} checks")
        
        return True
        
    except Exception as e:
        print(f"✗ Schema validation failed: {e}")
        return False

def test_direct_schema_instantiation():
    """Test direct LinkedInPostContent schema instantiation"""
    print("\n=== Testing Direct Schema Instantiation ===")
    
    try:
        # Create test hashtags
        test_hashtags = ["#systemdesign", "#microservices", "#architecture", "#scalability", "#engineering", "#tech"]
        
        # Test minimal valid content
        minimal_content = LinkedInPostContent(
            hook="Test hook for LinkedIn post",
            context="Test context setting the stage",
            key_insights=["Insight 1", "Insight 2", "Insight 3"],
            mini_example="Test example illustrating a point",
            cta="Test call to action",
            question="Test engagement question?",
            body="Test body content under 1300 characters",
            chars_count=42,
            hashtags=test_hashtags,
            hashtags_grouped={
                "broad": test_hashtags[:3],
                "niche": test_hashtags[3:5],
                "micro_niche": [],
                "intent": test_hashtags[5:6],
                "branded": []
            },
            alt_versions={
                "short": "Short version",
                "long": "Long version"
            },
            image_prompts=[
                {"role": "card_a", "title": "Test A", "prompt": "Test prompt 1", "ratio": "1.91:1", "size_px": "1200x627"},
                {"role": "card_b", "title": "Test B", "prompt": "Test prompt 2", "ratio": "5:4", "size_px": "1350x1080"}
            ],
            doc_carousel_outline={
                "enabled": False,
                "slides": []
            },
            compliance={
                "hashtags_count": 6,
                "image_prompt_count": 2,
                "body_chars_count": 42,
                "checks": ["test check"]
            }
        )
        
        print(f"✓ Direct schema instantiation successful")
        print(f"✓ Hook: {minimal_content.hook}")
        print(f"✓ Key insights count: {len(minimal_content.key_insights)}")
        print(f"✓ Hashtag groups: {list(minimal_content.hashtags_grouped.keys())}")
        print(f"✓ Character count: {minimal_content.chars_count}")
        
        return True
        
    except Exception as e:
        print(f"✗ Direct schema instantiation failed: {e}")
        return False

def main():
    """Run all tests"""
    print("LinkedIn Post Content Generation Tests")
    print("=" * 50)
    
    tests = [
        test_linkedin_post_prompt_processing,
        test_linkedin_post_schema_validation,
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
        print("🎉 All LinkedIn Post tests passed!")
        return True
    else:
        print("❌ Some tests failed")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
