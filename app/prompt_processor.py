import json
import os
import logging
from typing import Dict, Any

class PromptProcessor:
    def __init__(self, config_path: str = None):
        if config_path is None:
            config_path = os.path.join(os.path.dirname(__file__), 'prompts', 'config.json')
        
        with open(config_path, 'r') as f:
            self.config = json.load(f)
    
    def process_prompt_template(self, template_path: str, topic_id: str, topic_name: str, topic_description: str, platform: str = "instagram", format_type: str = "reel") -> str:
        """
        Process a prompt template by replacing placeholders with actual config values
        """
        logging.info(f"Processing prompt template: {template_path}")
        logging.info(f"Topic: {topic_name} (ID: {topic_id})")
        logging.info(f"Platform: {platform}, Format: {format_type}")
        
        # Read the template
        with open(template_path, 'r') as f:
            template = f.read()
        
        # Replace basic topic variables
        template = template.replace("{topic_id}", topic_id)
        template = template.replace("{topic_name}", topic_name)
        template = template.replace("{topic_description}", topic_description)
        
        # Check if this is the new direct variable format (carousel v2)
        if "{audience}" in template and "{tone}" in template:
            # New direct variable format - replace with config values directly
            template = self._replace_direct_variables(template, platform, format_type, topic_id)
        else:
            # Legacy config placeholder format
            template = self._replace_config_placeholders(template, platform, format_type, topic_id)
        
        # Log the processed prompt (truncated for readability)
        logging.info("=" * 80)
        logging.info("PROCESSED PROMPT BEING SENT TO AI:")
        logging.info("=" * 80)
        logging.info(template[:1000] + "..." if len(template) > 1000 else template)
        logging.info("=" * 80)
        
        return template
    
    def _replace_direct_variables(self, template: str, platform: str, format_type: str, topic_id: str) -> str:
        """
        Replace direct variables for new carousel v2 format
        """
        default_inputs = self.config.get("default_inputs", {})
        
        # Replace direct variables with config values
        template = template.replace("{audience}", default_inputs.get("audience", "intermediate"))
        template = template.replace("{tone}", default_inputs.get("tone", "clear, confident, non-cringe"))
        template = template.replace("{locale}", default_inputs.get("locale", "en"))
        
        # Replace primary_url with topic_id substitution
        primary_url = default_inputs.get("primary_url", "").replace("{topic_id}", topic_id)
        template = template.replace("{primary_url}", primary_url)
        
        return template
    
    def _replace_config_placeholders(self, template: str, platform: str, format_type: str, topic_id: str) -> str:
        """
        Replace all {config.*} placeholders with actual values
        """
        # Get platform-specific config
        platform_config = self.config.get("platform_specific", {}).get(platform, {}).get(format_type, {})
        
        # Replace platform-specific values dynamically
        template = template.replace(
            f"{{config.platform_specific.{platform}.{format_type}.content_schema_version}}",
            platform_config.get("content_schema_version", "v1.0.0")
        )
        template = template.replace(
            f"{{config.platform_specific.{platform}.{format_type}.model_version}}",
            platform_config.get("model_version", "gemini-2.5-flash")
        )
        template = template.replace(
            f"{{config.platform_specific.{platform}.{format_type}.prompt_version}}",
            platform_config.get("prompt_version", f"ig-{format_type}-1.2")
        )
        
        # Replace default inputs
        default_inputs = self.config.get("default_inputs", {})
        template = template.replace("{config.default_inputs.audience}", default_inputs.get("audience", "intermediate"))
        template = template.replace("{config.default_inputs.tone}", default_inputs.get("tone", "clear, confident, non-cringe"))
        template = template.replace("{config.default_inputs.locale}", default_inputs.get("locale", "en"))
        
        # Replace arrays as JSON strings
        template = template.replace(
            '"{config.default_inputs.primary_keywords}"',
            json.dumps(default_inputs.get("primary_keywords", []))
        )
        template = template.replace(
            '"{config.default_inputs.secondary_keywords}"',
            json.dumps(default_inputs.get("secondary_keywords", []))
        )
        template = template.replace(
            '"{config.default_inputs.lsi_terms}"',
            json.dumps(default_inputs.get("lsi_terms", []))
        )
        
        # Replace URLs with topic_id substitution
        primary_url = default_inputs.get("primary_url", "").replace("{topic_id}", topic_id)
        template = template.replace("{config.default_inputs.primary_url}", primary_url)
        
        # Replace brand info
        brand = default_inputs.get("brand", {})
        site_url = brand.get("siteUrl", "").replace("{topic_id}", topic_id)
        template = template.replace("{config.default_inputs.brand.siteUrl}", site_url)
        
        # Replace brand handles as JSON
        template = template.replace(
            '"{config.default_inputs.brand.handles}"',
            json.dumps(brand.get("handles", {}))
        )
        
        # Replace UTM base with platform/format substitution
        utm_base = brand.get("utmBase", "").replace("{platform}", platform).replace("{format}", format_type)
        template = template.replace("{config.default_inputs.brand.utmBase}", utm_base)
        
        # Replace options as JSON
        template = template.replace(
            '"{config.default_inputs.options}"',
            json.dumps(default_inputs.get("options", {}))
        )
        
        # Replace keyword tiers as JSON dynamically
        keyword_tiers = platform_config.get("keyword_tiers", {})
        template = template.replace(
            f'"{{config.platform_specific.{platform}.{format_type}.keyword_tiers}}"',
            json.dumps(keyword_tiers)
        )
        
        # Replace image plan as JSON dynamically
        image_plan = platform_config.get("image_plan", {})
        template = template.replace(
            f'"{{config.platform_specific.{platform}.{format_type}.image_plan}}"',
            json.dumps(image_plan)
        )
        
        # Replace visual guidelines
        visual_guidelines = self.config.get("visual_guidelines", {})
        template = template.replace("{config.visual_guidelines.background}", visual_guidelines.get("background", "off-white background"))
        template = template.replace("{config.visual_guidelines.strokes}", visual_guidelines.get("strokes", "thin vector strokes"))
        template = template.replace("{config.visual_guidelines.grid}", visual_guidelines.get("grid", "subtle grid"))
        template = template.replace("{config.visual_guidelines.margins}", visual_guidelines.get("margins", "generous margins"))
        template = template.replace("{config.visual_guidelines.accent}", visual_guidelines.get("accent", "one restrained accent color"))
        template = template.replace("{config.visual_guidelines.shadows}", visual_guidelines.get("shadows", "no drop shadows or faux 3D"))
        template = template.replace("{config.visual_guidelines.negative_prompt_baseline}", visual_guidelines.get("negative_prompt_baseline", ""))
        
        # Replace hashtag pools reference
        hashtag_pools = self.config.get("hashtag_pools", {})
        template = template.replace("{config.hashtag_pools}", json.dumps(hashtag_pools))
        
        # Replace brand handles in image prompts
        instagram_handle = brand.get("handles", {}).get("instagram", "@systemdesign")
        template = template.replace("{config.default_inputs.brand.handles.instagram}", instagram_handle)
        
        return template

# Usage example
if __name__ == "__main__":
    processor = PromptProcessor()
    
    # Process Instagram Reel template
    template_path = "prompts/bodies/instagram-reel.txt"
    processed_prompt = processor.process_prompt_template(
        template_path=template_path,
        topic_id="1234",
        topic_name="Load Balancing Strategies",
        topic_description="Learn about different load balancing algorithms and their trade-offs in distributed systems.",
        platform="instagram",
        format_type="reel"
    )
    
    print("Processed prompt ready to send to AI model:")
    print(processed_prompt[:500] + "...")
