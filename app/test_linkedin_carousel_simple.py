#!/usr/bin/env python3
"""
Simple test for LinkedIn Carousel content generation
Tests prompt processing and schema validation
"""

import sys
import os
import json
from pathlib import Path

# Add the app directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from prompt_processor import PromptProcessor
from schemas import validate_content, LinkedInCarouselContent

def test_linkedin_carousel_prompt_processing():
    """Test LinkedIn Carousel prompt template processing"""
    print("=== Testing LinkedIn Carousel Prompt Processing ===")
    
    # Initialize processor
    processor = PromptProcessor()
    
    # Test data
    test_topic_name = "Database Sharding Strategies for Scale"
    test_topic_description = "Learn proven database sharding techniques and patterns for scaling distributed systems to handle millions of users and petabytes of data"
    
    try:
        # Get template path
        template_path = os.path.join(os.path.dirname(__file__), 'prompts', 'bodies', 'linkedin-carousel.txt')
        
        # Process prompt
        processed_prompt = processor.process_prompt_template(
            template_path=template_path,
            topic_id="test_carousel_001",
            topic_name=test_topic_name,
            topic_description=test_topic_description,
            platform="linkedin",
            format_type="carousel"
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
            
        # Check for key LinkedIn Carousel elements
        required_elements = [
            "LinkedIn Document/Carousel",
            "doc_title",
            "slides",
            "description",
            "hashtags_grouped",
            "image_prompts",
            "doc_export",
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

def test_linkedin_carousel_schema_validation():
    """Test LinkedIn Carousel schema validation with sample data"""
    print("\n=== Testing LinkedIn Carousel Schema Validation ===")
    
    # Sample LinkedIn Carousel content that matches expected schema
    sample_content = {
        "doc_title": "Database Sharding: Scale to Millions",
        "slides": [
            {
                "index": 1,
                "role": "cover",
                "title": "Database Sharding Strategies",
                "subtitle": "Scale to millions of users",
                "bullets": ["Proven techniques", "Real-world examples"],
                "overlay_text": "Swipe →",
                "design_note": "Bold cover hierarchy; micro-glyph only",
                "layout": "title top; subtitle under; small glyph bottom-right; generous whitespace",
                "iconography": "database cluster glyph",
                "contrast_notes": "max contrast headline; micro-type for subtitle",
                "alt_text": "Cover slide for database sharding strategies guide"
            },
            {
                "index": 2,
                "role": "problem",
                "title": "The Scale Problem",
                "subtitle": "Single databases hit limits",
                "bullets": ["Performance degrades at 10M+ records", "Query times increase exponentially"],
                "overlay_text": "Problem →",
                "design_note": "light red underline on pain metric",
                "layout": "two-column bullets",
                "iconography": "alert/bottleneck",
                "contrast_notes": "accent only on number",
                "alt_text": "Problem slide showing database scaling challenges"
            },
            {
                "index": 3,
                "role": "core_idea",
                "title": "Horizontal Partitioning",
                "subtitle": "Split data across multiple databases",
                "bullets": ["Distribute load", "Maintain performance"],
                "overlay_text": "Approach",
                "design_note": "calm tone; green check motif",
                "layout": "headline left, bullets right",
                "iconography": "process glyph",
                "contrast_notes": "short labels",
                "alt_text": "Core concept of horizontal database partitioning"
            },
            {
                "index": 4,
                "role": "diagram",
                "title": "Sharding Architecture",
                "subtitle": "How data flows through shards",
                "bullets": ["Shard key routing", "Load balancer distribution"],
                "overlay_text": "Diagram",
                "design_note": "diagram-first; labeled arrows",
                "layout": "block diagram area with side notes",
                "iconography": "nodes/edges representing database shards",
                "contrast_notes": "thin lines; crisp labels; no shadows",
                "alt_text": "Architecture diagram showing database sharding flow"
            },
            {
                "index": 5,
                "role": "metrics_roi",
                "title": "Performance Impact",
                "subtitle": "Concrete improvements from sharding",
                "bullets": ["Query time: 2s → 200ms", "Throughput: 1K → 50K QPS"],
                "overlay_text": "Numbers",
                "design_note": "stat chips/sparklines; 1 hero metric",
                "layout": "stat grid",
                "iconography": "tiny chart marks",
                "contrast_notes": "highlight one hero metric",
                "alt_text": "Performance metrics showing sharding improvements",
                "data_points": [{"label": "P95", "value": "200", "unit": "ms"}]
            },
            {
                "index": 6,
                "role": "mini_case",
                "title": "Instagram's Journey",
                "subtitle": "From single DB to 1000+ shards",
                "bullets": ["before: 1 PostgreSQL instance", "after: 1000+ shards, 100M+ users"],
                "overlay_text": "Case",
                "design_note": "before/after arrows",
                "layout": "left before / right after",
                "iconography": "arrow transform",
                "contrast_notes": "accent on delta",
                "alt_text": "Instagram case study of database sharding evolution"
            },
            {
                "index": 7,
                "role": "steps",
                "title": "Implementation Steps",
                "subtitle": "How to shard your database",
                "bullets": ["Step 1: Choose shard key", "Step 2: Plan data distribution", "Step 3: Implement routing logic"],
                "overlay_text": "Playbook",
                "design_note": "checklist motif",
                "layout": "numbered list",
                "iconography": "checklist",
                "contrast_notes": "consistent spacing",
                "alt_text": "Step-by-step implementation guide for database sharding"
            },
            {
                "index": 8,
                "role": "risks",
                "title": "Common Pitfalls",
                "subtitle": "What to watch out for",
                "bullets": ["Risk: Hot shards", "Mitigation: Better key distribution"],
                "overlay_text": "Risks",
                "design_note": "two-column risk/mitigation",
                "layout": "left risks / right mitigation",
                "iconography": "shield/balance",
                "contrast_notes": "neutral palette",
                "alt_text": "Risk mitigation strategies for database sharding"
            },
            {
                "index": 9,
                "role": "cta",
                "title": "Start Your Sharding Journey",
                "subtitle": "Take the next step",
                "bullets": ["Download the full guide", "Share with your team"],
                "overlay_text": "CTA",
                "design_note": "end-card with handle & short URL",
                "layout": "big CTA; small handle @systemdesign",
                "iconography": "chevron arrow",
                "contrast_notes": "clear hierarchy",
                "alt_text": "Call-to-action slide with next steps"
            }
        ],
        "description": "Database sharding transformed how we scale at enterprise level 🚀\n\nKey insights from this guide:\n• Choose the right shard key (affects everything)\n• Plan for hot shard scenarios\n• Implement proper routing logic\n• Monitor cross-shard queries\n\nInstagram went from 1 DB to 1000+ shards serving 100M+ users. The principles are the same whether you're at 1M or 100M users.\n\nWhat's your biggest database scaling challenge? Download the full implementation guide: example.com?utm_source=linkedin&utm_medium=doc",
        "chars_count": 567,
        "hashtags": [
            "#systemdesign",
            "#databases", 
            "#sharding",
            "#scalability",
            "#architecture",
            "#performance"
        ],
        "hashtags_grouped": {
            "broad": ["#systemdesign", "#databases", "#architecture"],
            "niche": ["#sharding", "#scalability", "#performance"],
            "micro_niche": [],
            "intent": [],
            "branded": []
        },
        "image_prompts": [
            {
                "role": "cover",
                "title": "Doc Cover",
                "prompt": "Bold 5:4 cover for Database Sharding Strategies for Scale. Composition: strong title 'Database Sharding' top-left; subtitle 'Scale to Millions'; small database cluster glyph (abstract metaphor); subtle dotted grid; off-white background; thin vector strokes; blue accent color; generous whitespace; flat vector aesthetic.",
                "negative_prompt": "no stock-photo people, no logos, no neon, no 3D bevels, no glossy gradients, no clutter",
                "style_notes": "corporate-clean; crisp kerning; consistent stroke widths",
                "ratio": "5:4",
                "size_px": "1350x1080",
                "alt_text": "Cover slide with bold title and database cluster glyph"
            },
            {
                "role": "diagram_slide",
                "title": "Diagram Slide",
                "prompt": "Clear 5:4 concept diagram for database sharding; central load balancer connecting to 4 database shards with labeled arrows; shard key routing logic shown; metric chips showing performance; off-white background; thin strokes; subtle grid; blue accent color; generous margins; flat vector; mobile/desktop legible.",
                "negative_prompt": "no 3D, no photoreal elements, no logos",
                "style_notes": "diagram-first; legible labels; high contrast",
                "ratio": "5:4",
                "size_px": "1350x1080",
                "alt_text": "Database sharding architecture diagram with routing flow"
            }
        ],
        "image_prompts_by_slide": [],
        "doc_export": {
            "filename_suggestion": "li-doc-test_carousel_001-database-sharding-strategies.pdf",
            "ratio": "5:4",
            "size_px": "1350x1080",
            "safe_margins_px": 64,
            "page_count": 9
        },
        "compliance": {
            "slides_total": 9,
            "numbers_slides_count": 3,
            "hashtags_count": 6,
            "image_prompt_count": 2,
            "description_chars_count": 567,
            "checks": [
                "8–10 slides total",
                "titles ≤10 words; subtitles ≤14; bullets ≤14 words",
                "≥3 slides include concrete numbers",
                "includes mini_case and metrics/ROI slide",
                "single CTA in description",
                "5–8 professional hashtags (from keyword_tiers; unique)",
                "image_prompts length == image_plan.count (default 2)",
                "safe margins ≥64px"
            ]
        }
    }
    
    try:
        # Test schema validation
        validated_content = validate_content('linkedin', 'carousel', sample_content)
        
        print(f"✓ Schema validation successful")
        print(f"Content type: {type(validated_content).__name__}")
        
        # Test specific field access
        print(f"✓ Document title: {validated_content.doc_title}")
        print(f"✓ Slides count: {len(validated_content.slides)}")
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
    """Test direct LinkedInCarouselContent schema instantiation"""
    print("\n=== Testing Direct Schema Instantiation ===")
    
    try:
        # Create test hashtags
        test_hashtags = ["#systemdesign", "#databases", "#sharding", "#scalability", "#architecture", "#performance"]
        
        # Create minimal slide data
        test_slides = [
            {
                "index": i,
                "role": f"slide_{i}",
                "title": f"Test Slide {i}",
                "subtitle": f"Test subtitle {i}",
                "bullets": [f"Bullet 1 for slide {i}", f"Bullet 2 for slide {i}"],
                "overlay_text": f"Slide {i}",
                "design_note": "test design",
                "layout": "test layout",
                "iconography": "test icon",
                "contrast_notes": "test contrast",
                "alt_text": f"Test alt text for slide {i}"
            }
            for i in range(1, 9)  # 8 slides minimum
        ]
        
        # Test minimal valid content
        minimal_content = LinkedInCarouselContent(
            doc_title="Test Document Title",
            slides=test_slides,
            description="Test description for LinkedIn carousel document",
            chars_count=50,
            hashtags=test_hashtags,
            hashtags_grouped={
                "broad": test_hashtags[:3],
                "niche": test_hashtags[3:6],
                "micro_niche": [],
                "intent": [],
                "branded": []
            },
            image_prompts=[
                {"role": "cover", "title": "Test Cover", "prompt": "Test cover prompt", "ratio": "5:4", "size_px": "1350x1080"},
                {"role": "diagram_slide", "title": "Test Diagram", "prompt": "Test diagram prompt", "ratio": "5:4", "size_px": "1350x1080"}
            ],
            doc_export={
                "filename_suggestion": "test-doc.pdf",
                "ratio": "5:4",
                "size_px": "1350x1080",
                "safe_margins_px": 64,
                "page_count": 8
            },
            compliance={
                "slides_total": 8,
                "numbers_slides_count": 3,
                "hashtags_count": 6,
                "image_prompt_count": 2,
                "description_chars_count": 50,
                "checks": ["test check"]
            }
        )
        
        print(f"✓ Direct schema instantiation successful")
        print(f"✓ Document title: {minimal_content.doc_title}")
        print(f"✓ Slides count: {len(minimal_content.slides)}")
        print(f"✓ Hashtag groups: {list(minimal_content.hashtags_grouped.keys())}")
        print(f"✓ Character count: {minimal_content.chars_count}")
        
        return True
        
    except Exception as e:
        print(f"✗ Direct schema instantiation failed: {e}")
        return False

def main():
    """Run all tests"""
    print("LinkedIn Carousel Content Generation Tests")
    print("=" * 50)
    
    tests = [
        test_linkedin_carousel_prompt_processing,
        test_linkedin_carousel_schema_validation,
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
        print("🎉 All LinkedIn Carousel tests passed!")
        return True
    else:
        print("❌ Some tests failed")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)