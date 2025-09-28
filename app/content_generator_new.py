"""
Content generation service that integrates with the prompt processor and Gemini client.
"""
import os
import json
import logging
from typing import Dict, Any, Optional
from pathlib import Path

from .prompt_processor import PromptProcessor
from .gemini_client import GeminiClient
from .schemas import ContentEnvelope, ContentMeta, validate_content
from .models import PlatformRequest


class ContentGenerator:
    """Main content generation service."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.prompt_processor = PromptProcessor()
        self.gemini_client = None
    
    def _get_gemini_client(self) -> GeminiClient:
        """Get or create Gemini client instance."""
        if not self.gemini_client:
            self.gemini_client = GeminiClient()
        return self.gemini_client
    
    async def generate_platform_content(
        self, 
        platform: str, 
        format_type: str, 
        topic_id: str, 
        topic_name: str, 
        topic_description: str
    ) -> ContentEnvelope:
        """
        Generate content for a specific platform and format.
        
        Args:
            platform: Platform name (e.g., "instagram")
            format_type: Format type (e.g., "reel", "carousel")
            topic_id: Unique topic identifier
            topic_name: Topic title
            topic_description: Topic description
            
        Returns:
            ContentEnvelope with generated content
        """
        try:
            # Get the prompt template path
            template_path = self._get_template_path(platform, format_type)
            
            if not os.path.exists(template_path):
                self.logger.error(f"Template not found: {template_path}")
                raise Exception(f"Template not found: {template_path}")
            
            # Process the prompt template
            self.logger.info(f"Generating {platform} {format_type} content for topic: {topic_name}")
            processed_prompt = self.prompt_processor.process_prompt_template(
                template_path=template_path,
                topic_id=topic_id,
                topic_name=topic_name,
                topic_description=topic_description,
                platform=platform,
                format_type=format_type
            )
            
            # Save the final prompt to a file for debugging
            self._save_prompt_to_file(processed_prompt, platform, format_type, topic_id)
            
            # Generate content using Gemini
            gemini_client = self._get_gemini_client()
            
            self.logger.info("Sending processed prompt to Gemini API...")
            self.logger.debug(f"Processed prompt preview: {processed_prompt[:500]}...")
            
            raw_response = await gemini_client.generate_content(processed_prompt)
            
            self.logger.info("Received response from Gemini API")
            self.logger.debug(f"Raw Gemini response: {raw_response[:500]}...")
            
            # Parse the JSON response
            try:
                content_data = json.loads(raw_response)
                self.logger.info("Successfully parsed Gemini response as JSON")
                
                # Validate and create ContentEnvelope using proper schema validation
                from .schemas import ContentEnvelope, ContentMeta, validate_content
                
                try:
                    # Validate the content against platform-specific schema
                    validated_content = validate_content(platform, format_type, content_data.get("content", {}))
                    self.logger.info(f"Successfully validated content against {platform}:{format_type} schema")
                    
                    # Create ContentMeta from meta data
                    meta_data = content_data.get("meta", {})
                    content_meta = ContentMeta(**meta_data)
                    
                    # Create ContentEnvelope with validated content
                    envelope = ContentEnvelope(meta=content_meta, content=validated_content)
                    self.logger.info("Successfully created validated ContentEnvelope")
                    
                    return envelope
                    
                except Exception as validation_error:
                    self.logger.error(f"Schema validation failed: {validation_error}")
                    self.logger.error(f"Validation error type: {type(validation_error).__name__}")
                    
                    # Try to identify which part of validation is failing
                    try:
                        # Test content validation separately
                        validated_content = validate_content(platform, format_type, content_data.get("content", {}))
                        self.logger.info("Content validation passed, issue is with meta")
                    except Exception as content_error:
                        self.logger.error(f"Content validation failed: {content_error}")
                    
                    try:
                        # Test meta validation separately  
                        from .schemas import ContentMeta, BrandInfo, GenerationOptions, Audience, Locale, LengthLevel
                        meta_data = content_data.get("meta", {})
                        
                        # Create BrandInfo
                        brand_data = meta_data.get("brand", {})
                        brand_info = BrandInfo(**brand_data)
                        
                        # Create GenerationOptions
                        options_data = meta_data.get("options", {})
                        options = GenerationOptions(**options_data)
                        
                        # Update meta_data with proper objects
                        meta_data_copy = meta_data.copy()
                        meta_data_copy["brand"] = brand_info
                        meta_data_copy["options"] = options
                        meta_data_copy["audience"] = Audience(meta_data.get("audience", "intermediate"))
                        meta_data_copy["locale"] = Locale(meta_data.get("locale", "en"))
                        
                        content_meta = ContentMeta(**meta_data_copy)
                        self.logger.info("Meta validation passed, issue is with content")
                    except Exception as meta_error:
                        self.logger.error(f"Meta validation failed: {meta_error}")
                    
                    # Return raw data for debugging while we fix validation issues
                    self.logger.warning("Returning raw data due to validation failure")
                    return {
                        "meta": content_data.get("meta", {}),
                        "content": content_data.get("content", {})
                    }
                
            except json.JSONDecodeError as e:
                self.logger.error(f"Failed to parse Gemini response as JSON: {e}")
                self.logger.error(f"Raw response: {raw_response}")
                raise Exception(f"Invalid JSON response from Gemini API: {e}")
                
        except Exception as e:
            self.logger.error(f"Content generation failed: {e}")
            raise Exception(f"Content generation failed: {e}")
    
    def _get_template_path(self, platform: str, format_type: str) -> str:
        """Get the path to the prompt template file."""
        template_name = f"{platform}-{format_type}.txt"
        template_path = os.path.join(
            os.path.dirname(__file__), 
            "prompts", 
            "bodies", 
            template_name
        )
        return template_path
    
    def _save_prompt_to_file(self, prompt: str, platform: str, format_type: str, topic_id: str) -> None:
        """Save the final processed prompt to a file for debugging."""
        try:
            import os
            from datetime import datetime
            
            # Create debug directory if it doesn't exist
            debug_dir = os.path.join(os.path.dirname(__file__), "..", "debug", "prompts")
            os.makedirs(debug_dir, exist_ok=True)
            
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{platform}_{format_type}_{topic_id}_{timestamp}.txt"
            filepath = os.path.join(debug_dir, filename)
            
            # Write prompt to file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(prompt)
            
            self.logger.info(f"Saved processed prompt to: {filepath}")
            
        except Exception as e:
            self.logger.warning(f"Failed to save prompt to file: {e}")


# Create a global instance for use in routes
content_generator = ContentGenerator()
