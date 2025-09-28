#!/usr/bin/env python3
"""
Test script for Instagram Carousel content generation
"""
import sys
import os
import logging

# Add the app directory to the Python path
app_dir = os.path.join(os.path.dirname(__file__), 'app')
sys.path.insert(0, app_dir)

# Import with absolute paths to avoid relative import issues
import content_generator
import prompt_processor
import schemas

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_carousel_generation():
    """Test Instagram Carousel content generation"""
    
    # Initialize components
    content_gen = content_generator.ContentGenerator()
    
    # Test data
    topic_id = "test_carousel_001"
    topic_name = "Load Balancing Strategies"
    topic_description = "Learn about different load balancing algorithms including round-robin, weighted round-robin, least connections, and consistent hashing. Understand their trade-offs in distributed systems."
    platform = "instagram"
    format_type = "carousel"
    
    print(f"Testing Instagram Carousel generation for: {topic_name}")
    print("=" * 60)
    
    try:
        # Generate content
        result = content_gen.generate_platform_content(
            topic_id=topic_id,
            topic_name=topic_name,
            topic_description=topic_description,
            platform=platform,
            format_type=format_type
        )
        
        print("✅ Content generation completed successfully!")
        print(f"Result type: {type(result)}")
        
        # Check if result has the expected structure
        if hasattr(result, 'meta') and hasattr(result, 'content'):
            print(f"✅ Result has proper envelope structure")
            print(f"Meta platform: {result.meta.platform}")
            print(f"Meta format: {result.meta.format}")
            
            # Check content fields
            content = result.content
            print(f"Content type: {type(content)}")
            
            if hasattr(content, 'title'):
                print(f"✅ Title: {content.title[:50]}...")
            
            if hasattr(content, 'slides'):
                print(f"✅ Slides count: {len(content.slides)}")
                if content.slides:
                    first_slide = content.slides[0]
                    print(f"First slide keys: {list(first_slide.keys()) if isinstance(first_slide, dict) else 'Not a dict'}")
            
            if hasattr(content, 'caption'):
                print(f"✅ Caption length: {len(content.caption)} chars")
            
            if hasattr(content, 'hashtags'):
                print(f"✅ Hashtags count: {len(content.hashtags)}")
            
            if hasattr(content, 'call_to_action'):
                print(f"✅ CTA: {content.call_to_action}")
            
            if hasattr(content, 'compliance'):
                print(f"✅ Compliance field present: {content.compliance is not None}")
            
            # Test schema validation
            try:
                content_dict = content.dict() if hasattr(content, 'dict') else content
                validated_content = schemas.validate_content(platform, format_type, content_dict)
                print("✅ Schema validation passed!")
            except Exception as validation_error:
                print(f"❌ Schema validation failed: {validation_error}")
        
        else:
            print("❌ Result does not have expected envelope structure")
            print(f"Result: {result}")
        
    except Exception as e:
        print(f"❌ Content generation failed: {e}")
        import traceback
        traceback.print_exc()

def test_prompt_processing():
    """Test prompt template processing for carousel"""
    
    print("\nTesting Prompt Processing")
    print("=" * 30)
    
    try:
        processor = prompt_processor.PromptProcessor()
        
        template_path = os.path.join(os.path.dirname(__file__), 'app', 'prompts', 'bodies', 'instagram-carousel.txt')
        
        processed_prompt = processor.process_prompt_template(
            template_path=template_path,
            topic_id="test_001",
            topic_name="Load Balancing",
            topic_description="Test description",
            platform="instagram",
            format_type="carousel"
        )
        
        print("✅ Prompt processing completed!")
        print(f"Processed prompt length: {len(processed_prompt)} chars")
        
        # Check for key replacements
        if "{topic_id}" not in processed_prompt:
            print("✅ Topic ID placeholder replaced")
        else:
            print("❌ Topic ID placeholder not replaced")
        
        if "{topic_name}" not in processed_prompt:
            print("✅ Topic name placeholder replaced")
        else:
            print("❌ Topic name placeholder not replaced")
        
        if "config.platform_specific.instagram.carousel" in processed_prompt:
            print("✅ Platform-specific config placeholders found")
        else:
            print("❌ Platform-specific config placeholders not found")
        
    except Exception as e:
        print(f"❌ Prompt processing failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("Instagram Carousel Content Generation Test")
    print("=" * 50)
    
    # Test prompt processing first
    test_prompt_processing()
    
    # Test content generation
    test_carousel_generation()
    
    print("\nTest completed!")
