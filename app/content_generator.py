"""
Content generation service that integrates with the prompt processor and Gemini client.
"""
import os
import json
import logging
import re
from typing import Dict, Any, Optional
from pathlib import Path

from .prompt_processor import PromptProcessor
from .gemini_client import GeminiClient
from .schemas import ContentEnvelope, ContentMeta, validate_content


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
            
            # Save the raw API response for debugging
            self._save_raw_response_to_file(raw_response, platform, format_type, topic_id)
            
            # Parse the JSON response with comprehensive error recovery
            try:
                content_data = json.loads(raw_response)
                self.logger.info("Successfully parsed Gemini response as JSON")
                
                # Save the parsed JSON data for debugging
                self._save_parsed_json_to_file(content_data, platform, format_type, topic_id)
                
                # Process the successfully parsed JSON through validation
                return self._process_content_data(content_data, platform, format_type)
                
            except json.JSONDecodeError as json_error:
                self.logger.error(f"JSON parsing failed: {json_error}")
                self.logger.error(f"Raw response length: {len(raw_response)} characters")
                
                # Log the actual response content for debugging
                self.logger.error(f"Raw response preview: {raw_response[:200]}...")
                self.logger.error(f"Raw response end: ...{raw_response[-200:]}")
                
                # Try multiple JSON fixing strategies
                fixed_response = self._fix_json_response(raw_response)
                if fixed_response != raw_response:
                    self.logger.info("Attempting to parse fixed JSON response")
                    try:
                        content_data = json.loads(fixed_response)
                        self.logger.info("Successfully parsed fixed JSON response")
                        
                        # Save the fixed JSON data for debugging
                        self._save_fixed_json_to_file(fixed_response, content_data, platform, format_type, topic_id)
                        
                        # Process the recovered JSON through validation
                        return self._process_content_data(content_data, platform, format_type)
                        
                    except json.JSONDecodeError as fix_error:
                        self.logger.error(f"Fixed JSON still failed to parse: {fix_error}")
                        # Try advanced JSON recovery
                        self.logger.warning("Attempting advanced JSON recovery")
                        content_data = self._advanced_json_recovery(raw_response)
                        if not content_data:
                            # Try to extract partial data as last resort
                            self.logger.warning("Attempting to extract partial data from malformed JSON")
                            content_data = self._extract_partial_json(raw_response)
                            if not content_data:
                                # Generate fallback content
                                self.logger.warning("All JSON recovery failed, generating fallback content")
                                content_data = self._generate_fallback_content(platform, format_type, topic_id, topic_name, topic_description)
                                if not content_data:
                                    raise Exception(f"Invalid JSON response from Gemini API: {json_error}")
                                
                                # Return fallback content directly without validation
                                self.logger.info("Returning fallback content due to JSON parsing failure")
                                return {
                                    "meta": content_data.get("meta", {}),
                                    "content": content_data.get("content", {})
                                }
                        
                        # Process the recovered JSON through validation
                        return self._process_content_data(content_data, platform, format_type)
                        
                else:
                    # Try advanced JSON recovery
                    self.logger.warning("Attempting advanced JSON recovery")
                    content_data = self._advanced_json_recovery(raw_response)
                    if not content_data:
                        # Try to extract partial data as last resort
                        self.logger.warning("Attempting to extract partial data from malformed JSON")
                        content_data = self._extract_partial_json(raw_response)
                        if not content_data:
                            # Generate fallback content
                            self.logger.warning("All JSON recovery failed, generating fallback content")
                            content_data = self._generate_fallback_content(platform, format_type, topic_id, topic_name, topic_description)
                            if not content_data:
                                raise Exception(f"Invalid JSON response from Gemini API: {json_error}")
                            
                            # Return fallback content directly without validation
                            self.logger.info("Returning fallback content due to JSON parsing failure")
                            return {
                                "meta": content_data.get("meta", {}),
                                "content": content_data.get("content", {})
                            }
                    
                    # Process the recovered JSON through validation
                    return self._process_content_data(content_data, platform, format_type)
                
            except json.JSONDecodeError as e:
                self.logger.error(f"Failed to parse Gemini response as JSON: {e}")
                self.logger.error(f"Raw response: {raw_response}")
                raise Exception(f"Invalid JSON response from Gemini API: {e}")
                
        except Exception as e:
            self.logger.error(f"Content generation failed: {e}")
            raise Exception(f"Content generation failed: {e}")
        
        # This should never be reached - if we get here, there's a bug
        self.logger.error("CRITICAL BUG: Method reached end without returning anything!")
        self.logger.error("This indicates a missing return statement in the validation logic")
        raise Exception("Method reached end without returning - this is a bug")
    
    def _process_content_data(self, content_data: dict, platform: str, format_type: str):
        """
        Process and validate content data, returning a ContentEnvelope or raw data.
        
        Args:
            content_data: Parsed JSON content data
            platform: Platform name (e.g., "instagram")
            format_type: Format type (e.g., "reel", "carousel")
            
        Returns:
            ContentEnvelope or dict with meta/content
        """
        # Validate and create ContentEnvelope using proper schema validation
        from .schemas import ContentEnvelope, ContentMeta, validate_content
        
        self.logger.info(f"Starting validation for {platform}:{format_type}")
        self.logger.info(f"Content data keys: {list(content_data.keys())}")
        self.logger.info(f"Meta keys: {list(content_data.get('meta', {}).keys())}")
        self.logger.info(f"Content keys: {list(content_data.get('content', {}).keys())}")
        
        try:
            # Validate the content against platform-specific schema
            self.logger.info(f"Calling validate_content for {platform}:{format_type}")
            validated_content = validate_content(platform, format_type, content_data.get("content", {}))
            self.logger.info(f"Successfully validated content against {platform}:{format_type} schema")
            
            # Create ContentMeta from meta data with proper field mapping
            meta_data = content_data.get("meta", {})
            
            # Fix brand field mapping
            brand_data = meta_data.get("brand", {})
            if brand_data:
                meta_data["brand"] = {
                    "siteUrl": brand_data.get("site_url", "https://example.com"),
                    "handles": brand_data.get("handles", {}),
                    "utmBase": brand_data.get("utm_base", "utm_source=fallback")
                }
            
            # Fix GenerationOptions if missing required fields
            options_data = meta_data.get("options", {})
            if "max_length_levels" not in options_data:
                self.logger.warning("GenerationOptions missing max_length_levels, adding default")
                options_data["max_length_levels"] = {
                    "short": 100,
                    "medium": 500,
                    "long": 1000
                }
                meta_data["options"] = options_data
            
            content_meta = ContentMeta(**meta_data)
            
            # Create ContentEnvelope with validated content
            envelope = ContentEnvelope(meta=content_meta, content=validated_content)
            self.logger.info("Successfully created validated ContentEnvelope")
            self.logger.info(f"Returning ContentEnvelope with meta type: {type(content_meta).__name__}")
            self.logger.info(f"Returning ContentEnvelope with content type: {type(validated_content).__name__}")
            
            return envelope
            
        except Exception as validation_error:
            self.logger.error(f"Schema validation failed: {validation_error}")
            self.logger.error(f"Validation error type: {type(validation_error).__name__}")
            
            # Try to fix common validation issues
            content_data_copy = content_data.copy()
            content_copy = content_data_copy.get("content", {}).copy()
            
            # Fix LinkedIn Post body length issue
            if platform == "linkedin" and format_type == "post" and "body" in content_copy:
                body = content_copy.get("body", "")
                if len(body) > 1300:
                    self.logger.warning(f"LinkedIn Post body too long ({len(body)} chars), truncating to 1300 chars")
                    # Truncate to 1300 characters, trying to end at a word boundary
                    truncated_body = body[:1300]
                    last_space = truncated_body.rfind(' ')
                    if last_space > 1200:  # Only truncate at word boundary if it's not too short
                        truncated_body = truncated_body[:last_space]
                    content_copy["body"] = truncated_body
                    content_copy["chars_count"] = len(truncated_body)
                    content_data_copy["content"] = content_copy
                    self.logger.info(f"Truncated body to {len(truncated_body)} characters")
            
            # Fix Medium Article validation issues
            if platform == "medium" and format_type == "article":
                # Fix subtitle length if too long
                if "subtitle" in content_copy and len(content_copy["subtitle"]) > 120:
                    self.logger.warning(f"Medium Article subtitle too long ({len(content_copy['subtitle'])} chars), truncating to 120")
                    content_copy["subtitle"] = content_copy["subtitle"][:117] + "..."
                
                # Add missing compliance field if not present
                if "compliance" not in content_copy:
                    self.logger.warning("Medium Article missing compliance field, adding default compliance")
                    content_copy["compliance"] = {
                        "word_count": len(content_copy.get("markdown", "").split()),
                        "title_char_count": len(content_copy.get("title", "")),
                        "subtitle_char_count": len(content_copy.get("subtitle", "")),
                        "tags_count": len(content_copy.get("tags", [])),
                        "sections_count": len(content_copy.get("sections", [])),
                        "code_snippets_count": len(content_copy.get("code_snippets", [])),
                        "diagram_blocks_count": len(content_copy.get("diagram_blocks", [])),
                        "image_prompt_count": len(content_copy.get("image_prompts", [])),
                        "has_tracked_link": bool(content_copy.get("cta", {}).get("link")),
                        "checks": [
                            "800–1500 words",
                            "title ≤60 chars; subtitle ≤120",
                            "3–5 H2 sections (≤7 if length_hint high)",
                            "≥1 diagram block (mermaid/ascii) with alt text",
                            "5–7 tags",
                            "tracked CTA link present"
                        ]
                    }
                
                content_data_copy["content"] = content_copy
                self.logger.info("Applied Medium Article fixes")
            
            # Fix Substack Newsletter validation issues
            if platform == "substack" and format_type == "newsletter":
                # Fix preheader length if too long
                if "preheader" in content_copy and len(content_copy["preheader"]) > 90:
                    self.logger.warning(f"Substack Newsletter preheader too long ({len(content_copy['preheader'])} chars), truncating to 90")
                    content_copy["preheader"] = content_copy["preheader"][:87] + "..."
                
                # Add missing compliance field if not present
                if "compliance" not in content_copy:
                    self.logger.warning("Substack Newsletter missing compliance field, adding default compliance")
                    content_copy["compliance"] = {
                        "word_count": len(content_copy.get("markdown", "").split()),
                        "subject_char_count": len(content_copy.get("subject", "")),
                        "preheader_char_count": len(content_copy.get("preheader", "")),
                        "sections_count": len(content_copy.get("sections", [])),
                        "key_takeaways_count": len(content_copy.get("key_takeaways", [])),
                        "resources_count": len(content_copy.get("resources", [])),
                        "image_prompt_count": len(content_copy.get("image_prompts", [])),
                        "has_subscribe_cta": bool(content_copy.get("subscribe_cta", {}).get("text")),
                        "checks": [
                            "800–2000 words",
                            "subject ≤60 chars; preheader ≤90",
                            "3–6 sections with clear structure",
                            "≥3 key takeaways",
                            "≥2 resources/links",
                            "subscribe CTA present"
                        ]
                    }
                
                content_data_copy["content"] = content_copy
                self.logger.info("Applied Substack Newsletter fixes")
            
            # Fix Hacker News Item validation issues
            if platform == "hacker_news" and format_type == "item":
                # Add missing compliance field if not present
                if "compliance" not in content_copy:
                    self.logger.warning("Hacker News Item missing compliance field, adding default compliance")
                    content_copy["compliance"] = {
                        "title_char_count": len(content_copy.get("title", "")),
                        "summary_word_count": len(content_copy.get("summary", "").split()),
                        "text_post_word_count": len(content_copy.get("text_post", "").split()),
                        "has_link": bool(content_copy.get("link")),
                        "is_show_hn": bool(content_copy.get("is_show_hn", False)),
                        "comment_preparation_count": len(content_copy.get("comment_preparation", [])),
                        "moderation_notes_count": len(content_copy.get("moderation_notes", [])),
                        "checks": [
                            "title ≤80 chars",
                            "summary 2–4 sentences",
                            "text_post ≤500 words if present",
                            "link present for external content",
                            "comment preparation ready",
                            "moderation notes included"
                        ]
                    }
                
                content_data_copy["content"] = content_copy
                self.logger.info("Applied Hacker News Item fixes")
            
            # Fix Hashnode Article validation issues
            if platform == "hashnode" and format_type == "article":
                # Fix TOC length if too long
                if "toc" in content_copy and len(content_copy["toc"]) > 7:
                    self.logger.warning(f"Hashnode Article TOC too long ({len(content_copy['toc'])} items), truncating to 7")
                    content_copy["toc"] = content_copy["toc"][:7]
                
                # Add missing compliance field if not present
                if "compliance" not in content_copy:
                    self.logger.warning("Hashnode Article missing compliance field, adding default compliance")
                    content_copy["compliance"] = {
                        "word_count": len(content_copy.get("markdown", "").split()),
                        "reading_time_min": content_copy.get("reading_time_min", 0),
                        "toc_count": len(content_copy.get("toc", [])),
                        "sections_count": len(content_copy.get("sections", [])),
                        "code_snippets_count": len(content_copy.get("code_snippets", [])),
                        "diagram_blocks_count": len(content_copy.get("diagram_blocks", [])),
                        "has_cta": bool(content_copy.get("cta", {}).get("text")),
                        "has_seo": bool(content_copy.get("seo", {}).get("meta_description")),
                        "checks": [
                            "800–2000 words",
                            "reading time 3–8 minutes",
                            "TOC ≤7 items",
                            "3–6 sections with clear structure",
                            "≥1 code snippet or diagram",
                            "CTA present",
                            "SEO meta description"
                        ]
                    }
                
                content_data_copy["content"] = content_copy
                self.logger.info("Applied Hashnode Article fixes")
            
            # Fix DevTo Article validation issues
            if platform == "devto" and format_type == "article":
                # Add missing image_prompts field if not present
                if "image_prompts" not in content_copy:
                    self.logger.warning("DevTo Article missing image_prompts field, adding default")
                    content_copy["image_prompts"] = []
                
                # Add missing seo field if not present
                if "seo" not in content_copy:
                    self.logger.warning("DevTo Article missing seo field, adding default SEO")
                    content_copy["seo"] = {
                        "meta_description": content_copy.get("front_matter", {}).get("description", "")[:160],
                        "canonical_url": content_copy.get("front_matter", {}).get("canonical_url", ""),
                        "tags": content_copy.get("front_matter", {}).get("tags", []),
                        "published": content_copy.get("front_matter", {}).get("published", True)
                    }
                
                # Add missing compliance field if not present
                if "compliance" not in content_copy:
                    self.logger.warning("DevTo Article missing compliance field, adding default compliance")
                    content_copy["compliance"] = {
                        "word_count": len(content_copy.get("markdown", "").split()),
                        "reading_time_min": content_copy.get("reading_time_min", 0),
                        "code_snippets_count": len(content_copy.get("code_snippets", [])),
                        "diagram_blocks_count": len(content_copy.get("diagram_blocks", [])),
                        "resources_count": len(content_copy.get("resources", [])),
                        "has_front_matter": bool(content_copy.get("front_matter")),
                        "has_seo": bool(content_copy.get("seo", {}).get("meta_description")),
                        "checks": [
                            "800–2000 words",
                            "reading time 3–8 minutes",
                            "front matter with title, description, tags",
                            "≥1 code snippet or diagram",
                            "resources section present",
                            "SEO meta description"
                        ]
                    }
                
                content_data_copy["content"] = content_copy
                self.logger.info("Applied DevTo Article fixes")
            
            # Try validation again with fixed content
            try:
                validated_content = validate_content(platform, format_type, content_data_copy.get("content", {}))
                self.logger.info("Content validation passed after fixes")
                
                # Create ContentMeta from meta data with proper field mapping
                meta_data = content_data_copy.get("meta", {})
                
                # Fix brand field mapping
                brand_data = meta_data.get("brand", {})
                if brand_data:
                    meta_data["brand"] = {
                        "siteUrl": brand_data.get("site_url", "https://example.com"),
                        "handles": brand_data.get("handles", {}),
                        "utmBase": brand_data.get("utm_base", "utm_source=fallback")
                    }
                
                # Fix GenerationOptions if missing required fields
                options_data = meta_data.get("options", {})
                if "max_length_levels" not in options_data:
                    self.logger.warning("GenerationOptions missing max_length_levels, adding default")
                    options_data["max_length_levels"] = {
                        "short": 100,
                        "medium": 500,
                        "long": 1000
                    }
                    meta_data["options"] = options_data
                
                content_meta = ContentMeta(**meta_data)
                
                # Create ContentEnvelope with validated content
                envelope = ContentEnvelope(meta=content_meta, content=validated_content)
                self.logger.info("Successfully created validated ContentEnvelope after fixes")
                self.logger.info(f"Returning fixed ContentEnvelope with meta type: {type(content_meta).__name__}")
                self.logger.info(f"Returning fixed ContentEnvelope with content type: {type(validated_content).__name__}")
                
                return envelope
                
            except Exception as retry_validation_error:
                self.logger.error(f"Schema validation still failed after fixes: {retry_validation_error}")
            
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
                
                # Create BrandInfo with proper field mapping
                brand_data = meta_data.get("brand", {})
                brand_info = BrandInfo(
                    siteUrl=brand_data.get("site_url", "https://example.com"),
                    handles=brand_data.get("handles", {}),
                    utmBase=brand_data.get("utm_base", "utm_source=fallback")
                )
                
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
            self.logger.info(f"Returning raw data with meta keys: {list(content_data.get('meta', {}).keys())}")
            self.logger.info(f"Returning raw data with content keys: {list(content_data.get('content', {}).keys())}")
            return {
                "meta": content_data.get("meta", {}),
                "content": content_data.get("content", {})
            }
                
    def _fix_json_response(self, raw_response: str) -> str:
        """Attempt to fix common JSON parsing issues in Gemini responses."""
        try:
            # Remove any leading/trailing whitespace
            response = raw_response.strip()
            
            # Try to find the JSON object boundaries
            start_idx = response.find('{')
            if start_idx == -1:
                return raw_response
            
            # Find the matching closing brace
            brace_count = 0
            end_idx = start_idx
            for i in range(start_idx, len(response)):
                if response[i] == '{':
                    brace_count += 1
                elif response[i] == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        end_idx = i
                        break
            
            if brace_count != 0:
                # Unmatched braces, try to fix by adding closing braces
                response = response[:end_idx + 1] + '}' * brace_count
            
            # Extract just the JSON part
            json_part = response[start_idx:end_idx + 1]
            
            # Try to fix common JSON issues
            fixed_json = self._fix_json_syntax(json_part)
            
            # Validate that the fixed JSON can be parsed
            json.loads(fixed_json)
            return fixed_json
                
        except Exception as e:
            self.logger.warning(f"Could not fix JSON response: {e}")
            return raw_response
    
    def _advanced_json_recovery(self, raw_response: str) -> Optional[Dict[str, Any]]:
        """Advanced JSON recovery using multiple strategies."""
        try:
            response = raw_response.strip()
            
            # Strategy 1: Remove any text before the first '{'
            start_idx = response.find('{')
            if start_idx > 0:
                self.logger.info(f"Removing {start_idx} characters before JSON start")
                response = response[start_idx:]
                
                # Try to parse the cleaned response
                try:
                    return json.loads(response)
                except json.JSONDecodeError:
                    pass
            
            # Strategy 2: Find the largest valid JSON substring
            json_start = response.find('{')
            json_end = response.rfind('}')
            
            if json_start != -1 and json_end != -1 and json_end > json_start:
                json_candidate = response[json_start:json_end + 1]
                
                # Count braces to ensure they're balanced
                brace_count = 0
                for char in json_candidate:
                    if char == '{':
                        brace_count += 1
                    elif char == '}':
                        brace_count -= 1
                        if brace_count < 0:
                            break
                
                if brace_count == 0:
                    try:
                        return json.loads(json_candidate)
                    except json.JSONDecodeError:
                        pass
            
            # Strategy 3: Try to fix truncated JSON
            if response.endswith('...') or len(response) > 10000:
                # Look for the last complete JSON object
                last_complete = self._find_last_complete_json_object(response)
                if last_complete:
                    try:
                        return json.loads(last_complete)
                    except json.JSONDecodeError:
                        pass
            
            # Strategy 4: Fix unquoted property names
            fixed_response = self._fix_unquoted_properties(response)
            if fixed_response != response:
                try:
                    return json.loads(fixed_response)
                except json.JSONDecodeError:
                    pass
            
            return None
            
        except Exception as e:
            self.logger.warning(f"Advanced JSON recovery failed: {e}")
            return None
    
    def _fix_unquoted_properties(self, json_str: str) -> str:
        """Fix unquoted property names in JSON."""
        try:
            # Pattern to match unquoted property names followed by colon
            # This matches word characters, underscores, and hyphens
            pattern = r'(\s*)([a-zA-Z_][a-zA-Z0-9_-]*)\s*:'
            
            def replace_property(match):
                indent = match.group(1)
                property_name = match.group(2)
                return f'{indent}"{property_name}":'
            
            fixed_json = re.sub(pattern, replace_property, json_str)
            
            # Also fix any remaining unquoted strings that should be quoted
            # Look for patterns like: word: "value" (where word is not quoted)
            pattern2 = r'(\s*)([a-zA-Z_][a-zA-Z0-9_-]*)\s*:\s*"'
            fixed_json = re.sub(pattern2, r'\1"\2": "', fixed_json)
            
            return fixed_json
            
        except Exception as e:
            self.logger.warning(f"Could not fix unquoted properties: {e}")
            return json_str
    
    def _find_last_complete_json_object(self, text: str) -> Optional[str]:
        """Find the last complete JSON object in a string."""
        try:
            # Start from the end and work backwards
            brace_count = 0
            end_pos = len(text) - 1
            
            # Find a potential end position
            while end_pos >= 0:
                if text[end_pos] == '}':
                    break
                end_pos -= 1
            
            if end_pos < 0:
                return None
            
            # Work backwards to find matching start
            start_pos = end_pos
            brace_count = 0
            
            for i in range(end_pos, -1, -1):
                if text[i] == '}':
                    brace_count += 1
                elif text[i] == '{':
                    brace_count -= 1
                    if brace_count == 0:
                        start_pos = i
                        break
            
            if brace_count == 0 and start_pos < end_pos:
                candidate = text[start_pos:end_pos + 1]
                # Quick validation
                try:
                    json.loads(candidate)
                    return candidate
                except json.JSONDecodeError:
                    pass
            
            return None
            
        except Exception:
            return None
    
    def _fix_json_syntax(self, json_str: str) -> str:
        """Fix common JSON syntax issues."""
        try:
            # Split into lines for easier processing
            lines = json_str.split('\n')
            fixed_lines = []
            
            for i, line in enumerate(lines):
                line = line.rstrip()
                
                # Fix missing commas between JSON objects/arrays
                if i < len(lines) - 1:  # Not the last line
                    next_line = lines[i + 1].strip()
                    
                    # Check if current line ends with } or ] and next line starts with " or {
                    if (line.endswith('}') or line.endswith(']')) and next_line.startswith('"'):
                        # Add comma if missing
                        if not line.endswith(','):
                            line += ','
                    
                    # Check if current line ends with a value and next line starts with a key
                    elif (line.endswith('"') or line.endswith('true') or line.endswith('false') or line.endswith('null') or line.endswith(']')) and next_line.startswith('"'):
                        # Add comma if missing
                        if not line.endswith(','):
                            line += ','
                
                # Fix unterminated strings
                if '"' in line:
                    quote_count = line.count('"')
                    if quote_count % 2 == 1:  # Odd number of quotes means unterminated
                        # Find the last quote and add closing quote
                        last_quote_idx = line.rfind('"')
                        if last_quote_idx != -1:
                            # Check if there's content after the last quote
                            after_quote = line[last_quote_idx + 1:].strip()
                            if after_quote and not after_quote.endswith(','):
                                line = line[:last_quote_idx + 1] + '"'
                            elif after_quote and after_quote.endswith(','):
                                line = line[:last_quote_idx + 1] + '",'
                            else:
                                line = line[:last_quote_idx + 1] + '"'
                
                # Fix missing quotes around keys
                if ': ' in line and not line.strip().startswith('"'):
                    # This might be a key without quotes
                    colon_idx = line.find(': ')
                    if colon_idx > 0:
                        key_part = line[:colon_idx].strip()
                        value_part = line[colon_idx:]
                        if not key_part.startswith('"') and not key_part.startswith('{') and not key_part.startswith('['):
                            line = f'"{key_part}"{value_part}'
                
                fixed_lines.append(line)
            
            fixed_json = '\n'.join(fixed_lines)
            
            # Additional fixes for common patterns
            # Fix missing commas between array elements
            fixed_json = re.sub(r'(\])\s*(\")', r'\1,\2', fixed_json)
            # Fix missing commas between object properties
            fixed_json = re.sub(r'(\})\s*(\")', r'\1,\2', fixed_json)
            # Fix missing commas after values
            fixed_json = re.sub(r'(\")\s*(\")', r'\1,\2', fixed_json)
            fixed_json = re.sub(r'(true)\s*(\")', r'\1,\2', fixed_json)
            fixed_json = re.sub(r'(false)\s*(\")', r'\1,\2', fixed_json)
            fixed_json = re.sub(r'(null)\s*(\")', r'\1,\2', fixed_json)
            
            return fixed_json
            
        except Exception as e:
            self.logger.warning(f"Could not fix JSON syntax: {e}")
            return json_str
    
    def _extract_partial_json(self, raw_response: str) -> Optional[Dict[str, Any]]:
        """Extract partial data from malformed JSON as a last resort."""
        try:
            # Try to find and extract basic structure
            response = raw_response.strip()
            
            # First, try to find the complete JSON structure by finding matching braces
            start_idx = response.find('{')
            if start_idx == -1:
                return None
            
            # Find the matching closing brace by counting braces
            brace_count = 0
            end_idx = start_idx
            for i in range(start_idx, len(response)):
                if response[i] == '{':
                    brace_count += 1
                elif response[i] == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        end_idx = i
                        break
            
            # Extract the complete JSON structure
            json_str = response[start_idx:end_idx + 1]
            
            # Try to parse the complete JSON
            try:
                parsed_data = json.loads(json_str)
                self.logger.info(f"Successfully extracted complete JSON structure")
                return parsed_data
            except json.JSONDecodeError:
                pass
            
            # If complete parsing fails, try to extract meta and content sections with proper brace matching
            meta_start = response.find('"meta"')
            if meta_start != -1:
                # Find the opening brace after "meta"
                meta_brace_start = response.find('{', meta_start)
                if meta_brace_start != -1:
                    # Count braces to find the complete meta section
                    brace_count = 0
                    meta_end = meta_brace_start
                    for i in range(meta_brace_start, len(response)):
                        if response[i] == '{':
                            brace_count += 1
                        elif response[i] == '}':
                            brace_count -= 1
                            if brace_count == 0:
                                meta_end = i
                                break
                    
                    meta_str = response[meta_brace_start:meta_end + 1]
                    
                    # Try to parse meta section
                    try:
                        meta_data = json.loads(f"{{{meta_str}}}")
                        self.logger.info(f"Successfully extracted meta section")
                        return {"meta": meta_data, "content": {}}
                    except json.JSONDecodeError:
                        pass
            
            # Fallback: try to extract individual fields using regex
            extracted_data = {"meta": {}, "content": {}}
            
            # Extract common fields
            fields_to_extract = [
                "topic_id", "topic_title", "platform", "format", "title", "subtitle",
                "markdown", "tags", "sections", "image_prompts"
            ]
            
            for field in fields_to_extract:
                pattern = f'"{field}"\\s*:\\s*"([^"]*)"'
                match = re.search(pattern, response)
                if match:
                    if field in ["topic_id", "topic_title", "platform", "format"]:
                        extracted_data["meta"][field] = match.group(1)
                    else:
                        extracted_data["content"][field] = match.group(1)
            
            # If we extracted any data, return it
            if extracted_data["meta"] or extracted_data["content"]:
                self.logger.info(f"Extracted partial data: {len(extracted_data['meta'])} meta fields, {len(extracted_data['content'])} content fields")
                return extracted_data
            
            return None
                
        except Exception as e:
            self.logger.warning(f"Could not extract partial JSON data: {e}")
            return None
    
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
    
    def _save_raw_response_to_file(self, raw_response: str, platform: str, format_type: str, topic_id: str) -> None:
        """Save the raw API response to a file for debugging."""
        try:
            import os
            from datetime import datetime
            
            # Create debug directory if it doesn't exist
            debug_dir = os.path.join(os.path.dirname(__file__), "..", "debug", "responses")
            os.makedirs(debug_dir, exist_ok=True)
            
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{platform}_{format_type}_{topic_id}_{timestamp}_response.json"
            filepath = os.path.join(debug_dir, filename)
            
            # Write raw response to file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(raw_response)
            
            self.logger.info(f"Raw API response saved to: {filepath}")
            
        except Exception as e:
            self.logger.warning(f"Failed to save raw response to file: {e}")
    
    def _save_parsed_json_to_file(self, parsed_data: Dict[str, Any], platform: str, format_type: str, topic_id: str) -> None:
        """Save the parsed JSON data to a file for debugging."""
        try:
            import os
            from datetime import datetime
            
            # Create debug directory if it doesn't exist
            debug_dir = os.path.join(os.path.dirname(__file__), "..", "debug", "parsed")
            os.makedirs(debug_dir, exist_ok=True)
            
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{platform}_{format_type}_{topic_id}_{timestamp}_parsed.json"
            filepath = os.path.join(debug_dir, filename)
            
            # Write parsed data to file with pretty formatting
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(parsed_data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Parsed JSON data saved to: {filepath}")
            
        except Exception as e:
            self.logger.warning(f"Failed to save parsed JSON to file: {e}")
    
    def _save_fixed_json_to_file(self, fixed_response: str, parsed_data: Dict[str, Any], platform: str, format_type: str, topic_id: str) -> None:
        """Save the fixed JSON response and parsed data for debugging."""
        try:
            import os
            from datetime import datetime
            
            # Create debug directory if it doesn't exist
            debug_dir = os.path.join(os.path.dirname(__file__), "..", "debug", "fixed")
            os.makedirs(debug_dir, exist_ok=True)
            
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Save the fixed JSON string
            fixed_filename = f"{platform}_{format_type}_{topic_id}_{timestamp}_fixed.json"
            fixed_filepath = os.path.join(debug_dir, fixed_filename)
            
            with open(fixed_filepath, 'w', encoding='utf-8') as f:
                f.write(fixed_response)
            
            # Save the parsed data
            parsed_filename = f"{platform}_{format_type}_{topic_id}_{timestamp}_fixed_parsed.json"
            parsed_filepath = os.path.join(debug_dir, parsed_filename)
            
            with open(parsed_filepath, 'w', encoding='utf-8') as f:
                json.dump(parsed_data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Fixed JSON saved to: {fixed_filepath}")
            self.logger.info(f"Fixed parsed data saved to: {parsed_filepath}")
            
        except Exception as e:
            self.logger.warning(f"Failed to save fixed JSON to file: {e}")
    
    def _generate_fallback_content(self, platform: str, format_type: str, topic_id: str, topic_name: str, topic_description: str) -> Dict[str, Any]:
        """Generate fallback content when all JSON parsing fails."""
        try:
            self.logger.info(f"Generating fallback content for {platform}:{format_type}")
            
            # Create basic meta information
            meta = {
                    "topic_id": topic_id,
                    "topic_title": topic_name,
                    "platform": platform,
                    "format": format_type,
                    "content_schema_version": "v1.0.0",
                "model_version": "fallback",
                "audience": "intermediate",
                "tone": "clear, confident, non-cringe",
                "locale": "en",
                "primary_keywords": [topic_name.lower().split()[0]],
                "secondary_keywords": [],
                "lsi_terms": [],
                "canonical": f"https://example.com/topic/{topic_id}",
                "brand": {
                    "site_url": f"https://example.com/topic/{topic_id}",
                    "handles": {
                        "youtube": "@systemdesign",
                        "x": "@systemdesign",
                        "linkedin": "@systemdesign",
                        "instagram": "@systemdesign",
                        "github": "@systemdesign"
                    },
                    "utm_base": "utm_source=fallback&utm_medium=post"
                },
                "options": {
                    "include_images": True,
                    "max_length_levels": "standard",
                    "variance_seed": "fallback"
                },
                "keyword_overrides": False,
                "keyword_tiers": {
                    "broad": [],
                    "niche": [],
                    "micro_niche": [],
                    "intent": [],
                    "branded": []
                }
            }
            
            # Generate platform-specific fallback content
            content = self._generate_platform_fallback_content(platform, format_type, topic_name, topic_description)
            
            return {
                "meta": meta,
                "content": content
            }
            
        except Exception as e:
            self.logger.error(f"Fallback content generation failed: {e}")
            # Ultimate fallback
            return {
                "meta": {
                    "topic_id": topic_id,
                    "topic_title": topic_name,
                    "platform": platform,
                    "format": format_type,
                    "model_version": "error-fallback"
                },
                "content": {
                    "title": f"{topic_name} - System Design Guide",
                    "body": f"Learn about {topic_name} and how it applies to system design.",
                    "hashtags": ["#systemdesign", "#tech"],
                    "compliance": {
                        "checks": ["Generated as fallback due to API error"]
                    }
                }
            }
    
    def _generate_platform_fallback_content(self, platform: str, format_type: str, topic_name: str, topic_description: str) -> Dict[str, Any]:
        """Generate platform-specific fallback content."""
        base_title = f"{topic_name} - Complete System Design Guide"
        base_description = f"Comprehensive guide to {topic_name} in system design architecture."
        
        if platform == "youtube" and format_type == "long_form":
            return {
                "title": base_title[:60],  # YouTube title limit
                "thumbnail_text": topic_name.split()[0],
                "intro": {
                    "time_range": "0:00-0:15",
                    "narration": f"Welcome to our comprehensive guide on {topic_name}",
                        "on_screen_text": topic_name,
                    "visuals": "topic diagram",
                    "b_roll": ["screen recording"],
                    "sfx": ["soft music"],
                    "music": {"vibe": ["energetic"], "bpm_range": "90-110"}
                },
                "outline": [
                    {"section": "Introduction", "beats": [f"What is {topic_name}?"]},
                    {"section": "Core Concepts", "beats": ["Key principles", "Best practices"]},
                    {"section": "Implementation", "beats": ["Step by step guide"]},
                    {"section": "Conclusion", "beats": ["Summary", "Next steps"]}
                ],
                "chapters": [
                    {"index": 1, "name": "Introduction", "timestamp": "0:00"},
                    {"index": 2, "name": "Core Concepts", "timestamp": "1:30"},
                    {"index": 3, "name": "Implementation", "timestamp": "5:00"},
                    {"index": 4, "name": "Conclusion", "timestamp": "8:00"}
                ],
                "script": [
                    {
                        "chapter_index": 1,
                        "time_range": "0:00-1:30",
                        "talking_points": [f"Introduction to {topic_name}"],
                        "details": base_description,
                        "screen_recording_notes": ["show diagrams"],
                    }
                ],
                "visual_aids": {
                    "graphics_list": [{"name": "architecture_diagram", "purpose": "explain concept", "appears_at": "2:00"}],
                    "lower_thirds": ["Key Points"],
                    "music": {"vibe": ["professional"], "bpm_range": "80-100"},
                    "sfx": ["click sounds"]
                },
                "cta": {
                    "midroll": "If this helps, hit like!",
                    "end": f"Learn more at example.com/topic/{topic_name.lower().replace(' ', '-')}",
                    "end_screen": {"duration_seconds": 20, "elements": ["subscribe"], "show_handles": True}
                },
                "description": {
                    "text": f"{base_description} Learn the fundamentals and advanced concepts of {topic_name} in this comprehensive tutorial.",
                    "chapters": [
                        {"time": "0:00", "title": "Introduction"},
                        {"time": "1:30", "title": "Core Concepts"}
                    ],
                    "resources": [
                        {"title": "Full Guide", "url": f"https://example.com/topic/{topic_name.lower().replace(' ', '-')}"}
                    ],
                    "hashtags": ["#systemdesign", "#tutorial"]
                },
                "tags": ["system design", "architecture", "tutorial", "guide", "technology"],
                "image_prompts": [],
                "compliance": {
                    "est_duration_minutes": 10,
                    "title_char_count": len(base_title),
                    "chapters_count": 4,
                    "description_word_count": 50,
                    "tags_count": 5,
                    "image_prompt_count": 0,
                    "has_tracked_link": False,
                    "checks": [
                        "Basic structure provided",
                        "Generated as fallback content",
                        "Meets minimum requirements"
                    ]
                }
            }
        
        # Generic fallback for other platforms
            return {
            "title": base_title,
            "content": base_description,
            "hashtags": ["#systemdesign", "#tech"],
            "compliance": {
                "checks": [
                    "Basic fallback content generated",
                    "Platform-specific format not available"
                ]
            }
        }


# Create a global instance for use in routes
content_generator = ContentGenerator()
