"""
Platform-specific routes for content generation service.
"""
from fastapi import APIRouter, HTTPException, Path
from typing import Dict, Any
import logging

from .schemas import PlatformRequest, ContentEnvelope
from .content_generator import ContentGenerator

router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize content generator
content_generator = ContentGenerator()


@router.post("/{platform}/{format}", response_model=ContentEnvelope)
async def generate_platform_content(
    platform: str = Path(..., description="Platform name"),
    format: str = Path(..., description="Format name"),
    request: PlatformRequest = None
):
    """
    Generate content for a specific platform and format.
    """
    try:
        logger.info(f"Content generation request: {platform}/{format}")
        
        # Validate platform:format combination
        valid_combinations = {
            ('instagram', 'reel'), ('instagram', 'carousel'), ('instagram', 'story'), ('instagram', 'post'),
            ('linkedin', 'post'), ('linkedin', 'carousel'),
            ('x_twitter', 'thread'),
            ('youtube', 'short'), ('youtube', 'long_form'),
            ('threads', 'post'),
            ('facebook', 'post'),
            ('medium', 'article'),
            ('substack', 'newsletter'),
            ('reddit', 'post'),
            ('hacker_news', 'item'),
            ('devto', 'article'),
            ('hashnode', 'article'),
            ('github_pages', 'content'),
            ('notion', 'page'),
            ('personal_blog', 'post'),
            ('ghost', 'post'),
            ('telegram', 'post')
        }
        
        if (platform, format) not in valid_combinations:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid platform:format combination: {platform}:{format}"
            )
        
        # Extract request data
        if not request:
            raise HTTPException(status_code=400, detail="Request body is required")
        
        topic_id = request.topicId or "unknown"
        topic_name = request.topicName or "Untitled Topic"
        topic_description = request.topicDescription or f"Learn about {topic_name}"
        
        logger.info(f"Generating content for topic: {topic_name} (ID: {topic_id})")
        
        # Generate content using the integrated content generator
        result = await content_generator.generate_platform_content(
            platform=platform,
            format_type=format,
            topic_id=topic_id,
            topic_name=topic_name,
            topic_description=topic_description
        )
        
        logger.info(f"Content generation completed for {platform}/{format}")
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Content generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Alias routes for hyphenated format
@router.post("/instagram-reel", response_model=ContentEnvelope)
async def generate_instagram_reel(request: PlatformRequest):
    """Generate Instagram reel content."""
    return await generate_platform_content("instagram", "reel", request)


@router.post("/instagram-carousel", response_model=ContentEnvelope)
async def generate_instagram_carousel(request: PlatformRequest):
    """Generate Instagram carousel content."""
    return await generate_platform_content("instagram", "carousel", request)


@router.post("/instagram-story", response_model=ContentEnvelope)
async def generate_instagram_story(request: PlatformRequest):
    """Generate Instagram story content."""
    return await generate_platform_content("instagram", "story", request)


@router.post("/instagram-post", response_model=ContentEnvelope)
async def generate_instagram_post(request: PlatformRequest):
    """Generate Instagram post content."""
    return await generate_platform_content("instagram", "post", request)


@router.post("/linkedin-post", response_model=ContentEnvelope)
async def generate_linkedin_post(request: PlatformRequest):
    """Generate LinkedIn post content."""
    return await generate_platform_content("linkedin", "post", request)


@router.post("/linkedin-carousel", response_model=ContentEnvelope)
async def generate_linkedin_carousel(request: PlatformRequest):
    """Generate LinkedIn carousel content."""
    return await generate_platform_content("linkedin", "carousel", request)


@router.post("/twitter-thread", response_model=ContentEnvelope)
async def generate_twitter_thread(request: PlatformRequest):
    """Generate X/Twitter thread content."""
    return await generate_platform_content("x_twitter", "thread", request)


@router.post("/youtube-short", response_model=ContentEnvelope)
async def generate_youtube_short(request: PlatformRequest):
    """Generate YouTube short content."""
    return await generate_platform_content("youtube", "short", request)


@router.post("/youtube-long", response_model=ContentEnvelope)
async def generate_youtube_long(request: PlatformRequest):
    """Generate YouTube long form content."""
    return await generate_platform_content("youtube", "long_form", request)


@router.post("/threads-post", response_model=ContentEnvelope)
async def generate_threads_post(request: PlatformRequest):
    """Generate Threads post content."""
    return await generate_platform_content("threads", "post", request)


@router.post("/facebook-post", response_model=ContentEnvelope)
async def generate_facebook_post(request: PlatformRequest):
    """Generate Facebook post content."""
    return await generate_platform_content("facebook", "post", request)


@router.post("/medium-article", response_model=ContentEnvelope)
async def generate_medium_article(request: PlatformRequest):
    """Generate Medium article content."""
    return await generate_platform_content("medium", "article", request)


@router.post("/substack-newsletter", response_model=ContentEnvelope)
async def generate_substack_newsletter(request: PlatformRequest):
    """Generate Substack newsletter content."""
    return await generate_platform_content("substack", "newsletter", request)


@router.post("/reddit-post", response_model=ContentEnvelope)
async def generate_reddit_post(request: PlatformRequest):
    """Generate Reddit post content."""
    return await generate_platform_content("reddit", "post", request)


@router.post("/hn-item", response_model=ContentEnvelope)
async def generate_hn_item(request: PlatformRequest):
    """Generate Hacker News item content."""
    return await generate_platform_content("hacker_news", "item", request)


@router.post("/devto-article", response_model=ContentEnvelope)
async def generate_devto_article(request: PlatformRequest):
    """Generate Dev.to article content."""
    return await generate_platform_content("devto", "article", request)


@router.post("/hashnode-article", response_model=ContentEnvelope)
async def generate_hashnode_article(request: PlatformRequest):
    """Generate Hashnode article content."""
    return await generate_platform_content("hashnode", "article", request)


@router.post("/github-pages", response_model=ContentEnvelope)
async def generate_github_pages(request: PlatformRequest):
    """Generate GitHub Pages content."""
    return await generate_platform_content("github_pages", "content", request)


@router.post("/notion-page", response_model=ContentEnvelope)
async def generate_notion_page(request: PlatformRequest):
    """Generate Notion page content."""
    return await generate_platform_content("notion", "page", request)


@router.post("/blog-post", response_model=ContentEnvelope)
async def generate_blog_post(request: PlatformRequest):
    """Generate personal blog post content."""
    return await generate_platform_content("personal_blog", "post", request)


@router.post("/ghost-post", response_model=ContentEnvelope)
async def generate_ghost_post(request: PlatformRequest):
    """Generate Ghost post content."""
    return await generate_platform_content("ghost", "post", request)


@router.post("/telegram-post", response_model=ContentEnvelope)
async def generate_telegram_post(request: PlatformRequest):
    """Generate Telegram post content."""
    return await generate_platform_content("telegram", "post", request)
