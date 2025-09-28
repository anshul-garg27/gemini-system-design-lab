"""
Pydantic schemas for content generation service.
"""
from typing import Dict, List, Optional, Union, Any
from pydantic import BaseModel, Field, validator
from enum import Enum


class Audience(str, Enum):
    BEGINNERS = "beginners"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class Locale(str, Enum):
    EN = "en"
    HI = "hi"
    EN_HI = "en-hi"


class LengthLevel(str, Enum):
    COMPACT = "compact"
    STANDARD = "standard"
    DETAILED = "detailed"


class JobStatusEnum(str, Enum):
    RUNNING = "running"
    DONE = "done"
    ERROR = "error"


class TaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    ERROR = "error"


# Base schemas
class BrandInfo(BaseModel):
    site_url: str = Field(..., description="Brand website URL", alias="siteUrl")
    handles: Dict[str, str] = Field(..., description="Social media handles")
    utm_base: str = Field(..., description="UTM base for tracking", alias="utmBase")
    
    class Config:
        validate_by_name = True


class GenerationOptions(BaseModel):
    include_images: bool = Field(..., description="Whether to include image prompts")
    max_length_levels: LengthLevel = Field(..., description="Content length level")
    force: bool = Field(False, description="Force regeneration, ignore cache")
    length_hint: int = Field(0, description="Length hint for content")


class ContentMeta(BaseModel):
    topic_id: str
    topic_title: str
    platform: str
    format: str
    content_schema_version: str = "v1.0.0"
    model_version: str = "gemini-2.5-flash"
    prompt_version: str
    audience: Audience
    tone: str
    locale: Locale
    primary_keywords: List[str]
    secondary_keywords: List[str]
    lsi_terms: List[str]
    canonical: str
    brand: BrandInfo
    options: GenerationOptions


# Request schemas
class GenerateAllRequest(BaseModel):
    topicId: str
    topicName: str
    topicDescription: str
    audience: Audience
    tone: str
    locale: Locale
    primaryUrl: str
    brand: BrandInfo
    targetPlatforms: List[str] = Field(..., description="List of platform:format combinations")
    options: GenerationOptions

    @validator('targetPlatforms')
    def validate_platforms(cls, v):
        valid_platforms = {
            'instagram:reel', 'instagram:carousel', 'instagram:story', 'instagram:post',
            'linkedin:post', 'linkedin:carousel',
            'x_twitter:thread',
            'youtube:short', 'youtube:long_form',
            'threads:post',
            'facebook:post',
            'medium:article',
            'substack:newsletter',
            'reddit:post',
            'hacker_news:item',
            'devto:article',
            'hashnode:article',
            'github_pages:content',
            'notion:page',
            'personal_blog:post',
            'ghost:post',
            'telegram:post'
        }
        
        for platform in v:
            if platform not in valid_platforms:
                raise ValueError(f"Invalid platform:format combination: {platform}")
        return v


class PlatformRequest(BaseModel):
    topicId: str
    topicName: str
    topicDescription: str
    audience: Audience
    tone: str
    locale: Locale
    primaryUrl: str
    brand: BrandInfo
    options: GenerationOptions


class RegenerateRequest(BaseModel):
    jobId: str
    targets: List[Dict[str, str]] = Field(..., description="List of platform:format targets")
    reasons: Optional[str] = None
    creativity_delta: float = Field(0.0, ge=0.0, le=1.0)
    force: bool = True


# Response schemas
class JobResponse(BaseModel):
    jobId: str
    status: JobStatusEnum
    selected: List[Dict[str, str]]


class JobStatusResponse(BaseModel):
    jobId: str
    status: JobStatusEnum
    progress: Dict[str, int]
    errors: Optional[List[Dict[str, str]]] = None


class ResultsResponse(BaseModel):
    jobId: str
    status: JobStatusEnum
    results: List[Dict[str, Any]]
    errors: List[Dict[str, Any]] = []


# Platform-specific content schemas
class InstagramReelContent(BaseModel):
    """Instagram Reel content schema"""
    title: str = Field(..., max_length=100)
    hook: str = Field(..., max_length=200)
    content_segments: List[Dict[str, Any]] = Field(..., min_items=2, max_items=8)
    caption: str = Field(..., max_length=2200)
    hashtags: List[str] = Field(..., max_items=30)
    image_prompts: Optional[List[Dict[str, str]]] = None
    call_to_action: str = Field(..., max_length=100)
    music_suggestion: Optional[str] = None


class InstagramCarouselContent(BaseModel):
    """Instagram Carousel content schema"""
    slides: List[Dict[str, Any]] = Field(..., min_items=3, max_items=10)
    caption: Union[str, Dict[str, Any]] = Field(..., description="Caption text or enhanced caption object")
    hashtags: List[str] = Field(..., max_items=30)
    design_system: Optional[Dict[str, Any]] = Field(None, description="Design system specifications")
    image_prompts: Optional[List[Dict[str, str]]] = None
    image_prompts_by_slide: Optional[List[Dict[str, Any]]] = Field(None, description="Per-slide image prompts")
    compliance: Optional[Dict[str, Any]] = Field(None, description="Validation metrics and checks")


class InstagramStoryContent(BaseModel):
    """Instagram Story content schema"""
    frames: List[Dict[str, Any]] = Field(..., min_items=3, max_items=5)
    stickers: Dict[str, Any] = Field(..., description="Interactive stickers configuration")
    image_prompts: Optional[List[Dict[str, str]]] = None
    overlay_hashtags: Optional[List[str]] = Field(None, max_items=6)
    compliance: Optional[Dict[str, Any]] = Field(None, description="Validation metrics and checks")


class InstagramPostContent(BaseModel):
    visual_concept: str = Field(..., description="One-sentence description of the visual idea")
    caption: Dict[str, Any] = Field(..., description="Caption with first_line_hook, text, cta, and seo")
    hashtags: List[str] = Field(..., min_items=30, max_items=30, description="Exactly 30 hashtags")
    hashtags_grouped: Dict[str, List[str]] = Field(..., description="Hashtags grouped by reach tier")
    location_tag_suggestions: List[Dict[str, str]] = Field(default_factory=list, description="Location suggestions with name, type, reason")
    image_prompts: List[Dict[str, Any]] = Field(..., min_items=2, description="Image variant prompts with detailed structure")
    compliance: Dict[str, Any] = Field(..., description="Validation metrics and checks")


class LinkedInPostContent(BaseModel):
    hook: str = Field(..., description="2-3 line opening hook")
    context: str = Field(..., description="2-3 sentences setting stakes and audience")
    key_insights: List[str] = Field(..., min_items=3, max_items=5, description="3-5 scannable insights")
    mini_example: str = Field(..., description="Compact example illustrating one point")
    cta: str = Field(..., description="Comment prompt with optional link")
    question: str = Field(..., description="Thoughtful engagement question")
    body: str = Field(..., max_length=1300, description="Full assembled post with line breaks")
    chars_count: int = Field(..., description="Character count of body")
    hashtags: List[str] = Field(..., min_items=5, max_items=8, description="5-8 professional hashtags")
    hashtags_grouped: Dict[str, List[str]] = Field(..., description="Hashtags grouped by reach tier")
    alt_versions: Dict[str, str] = Field(..., description="Short and long variants")
    image_prompts: List[Dict[str, Any]] = Field(..., min_items=2, description="Image card prompts")
    doc_carousel_outline: Dict[str, Any] = Field(..., description="Optional PDF carousel outline")
    compliance: Dict[str, Any] = Field(..., description="Validation metrics and checks")


class LinkedInCarouselContent(BaseModel):
    doc_title: str = Field(..., max_length=60, description="Concise document title")
    slides: List[Dict[str, Any]] = Field(..., min_items=8, max_items=10, description="8-10 carousel slides")
    description: str = Field(..., max_length=1300, description="LinkedIn post text accompanying document")
    chars_count: int = Field(..., description="Character count of description")
    hashtags: List[str] = Field(..., min_items=5, max_items=8, description="5-8 professional hashtags")
    hashtags_grouped: Dict[str, List[str]] = Field(..., description="Hashtags grouped by reach tier")
    image_prompts: List[Dict[str, Any]] = Field(..., min_items=2, description="Image prompts for slides")
    image_prompts_by_slide: Optional[List[Dict[str, Any]]] = Field(None, description="Per-slide image prompts")
    doc_export: Dict[str, Any] = Field(..., description="PDF export configuration")
    compliance: Dict[str, Any] = Field(..., description="Validation metrics and checks")


class XTwitterThreadContent(BaseModel):
    """X/Twitter Thread content schema"""
    tweets: List[Dict[str, Any]] = Field(..., min_items=5, max_items=9, description="5-9 tweets with structured content")
    engagement_tweet: Dict[str, Any] = Field(..., description="Question or poll for replies")
    hashtags: List[str] = Field(..., min_items=8, max_items=12, description="Global shortlist of professional hashtags")
    mention_suggestions: List[str] = Field(..., min_items=2, max_items=5, description="Relevant handles to mention")
    tweet_media_plan: List[Dict[str, Any]] = Field(..., description="Media attachment plan for tweets")
    image_prompts: List[Dict[str, Any]] = Field(..., min_items=2, description="Image prompts for thread visuals")
    compliance: Dict[str, Any] = Field(..., description="Validation metrics and checks")


class YouTubeShortContent(BaseModel):
    """YouTube Short content schema"""
    title: str = Field(..., max_length=80, description="SEO-optimized title, ≤80 characters")
    beats: List[Dict[str, Any]] = Field(..., min_items=6, max_items=6, description="6 structured beats: Hook, Value-1, Value-2, Value-3, Subscribe, EndScreen")
    script: str = Field(..., description="45-60s voiceover script with timecodes")
    overlay_text_cues: List[Dict[str, Any]] = Field(..., description="On-screen text timing and content")
    b_roll_plan: List[Dict[str, Any]] = Field(..., description="B-roll suggestions by time range")
    music: Dict[str, Any] = Field(..., description="Background music specifications")
    sfx: List[str] = Field(..., description="Sound effects list")
    end_screen: Dict[str, Any] = Field(..., description="End screen CTA and elements")
    description: Dict[str, Any] = Field(..., description="Video description with timestamps")
    tags: List[str] = Field(..., min_items=20, max_items=20, description="Exactly 20 relevant tags")
    image_prompts: List[Dict[str, Any]] = Field(..., min_items=2, description="Vertical cover images and optional diagrams")
    compliance: Dict[str, Any] = Field(..., description="Validation metrics and platform compliance")


class YouTubeLongFormContent(BaseModel):
    """YouTube Long Form content schema"""
    title: str = Field(..., min_length=50, max_length=60, description="Keyword-optimized title, 50-60 characters")
    thumbnail_text: str = Field(..., max_length=20, description="3-4 words max for thumbnail")
    intro: Dict[str, Any] = Field(..., description="0-15s intro with hook, visuals, and music")
    outline: List[Dict[str, Any]] = Field(..., min_items=6, description="6+ structured sections with beats")
    chapters: List[Dict[str, Any]] = Field(..., min_items=6, max_items=10, description="6-10 chapters with timestamps")
    script: List[Dict[str, Any]] = Field(..., description="Detailed script with time ranges and talking points")
    visual_aids: Dict[str, Any] = Field(..., description="B-roll plan, graphics, lower thirds, music, SFX")
    cta: Dict[str, Any] = Field(..., description="Midroll, end CTA, and end screen specifications")
    description: Dict[str, Any] = Field(..., description="500+ word description with chapters and resources")
    tags: List[str] = Field(..., min_items=20, max_items=20, description="Exactly 20 relevant tags")
    image_prompts: List[Dict[str, Any]] = Field(..., min_items=2, description="16:9 thumbnail designs")
    compliance: Dict[str, Any] = Field(..., description="Duration, word count, and validation metrics")


class FacebookPostContent(BaseModel):
    """Facebook Post content schema"""
    headline: str = Field(..., max_length=80, description="Attention-grabbing line, ≤80 characters")
    post: str = Field(..., description="2-4 short lines + single CTA; friendly and clear")
    alt_versions: List[str] = Field(..., min_items=2, max_items=2, description="Two alternative versions")
    long_body: Dict[str, Any] = Field(..., description="500-700 word storytelling post with mini-story")
    link_preview: Dict[str, Any] = Field(..., description="Preview title, description, and OG image role")
    groups_pitch: str = Field(..., description="1-2 lines tailored to FB groups")
    groups_to_share: List[Dict[str, Any]] = Field(..., min_items=5, max_items=10, description="5-10 relevant communities")
    hashtags: List[str] = Field(..., min_items=3, max_items=6, description="3-6 casual/professional tags")
    mention_suggestions: List[str] = Field(..., description="1-3 optional accounts/pages to mention")
    image_prompts: List[Dict[str, Any]] = Field(..., min_items=2, description="Wide and square image cards")
    compliance: Dict[str, Any] = Field(..., description="Post lines, word count, and validation metrics")


class ThreadsPostContent(BaseModel):
    """Threads Post content schema"""
    post: str = Field(..., max_length=500, description="Main post content, ≤500 characters")
    alt_versions: List[str] = Field(..., min_items=2, max_items=3, description="2-3 alternative post versions")
    reply_chain: List[Dict[str, Any]] = Field(default_factory=list, description="0-4 optional reply posts")
    hashtags: List[str] = Field(..., min_items=5, max_items=10, description="5-10 casual hashtags")
    mentions_suggestions: List[str] = Field(default_factory=list, description="1-3 optional mention suggestions")
    link_plan: Dict[str, Any] = Field(..., description="Link placement strategy and URL")
    image_prompts: List[Dict[str, Any]] = Field(..., min_items=2, description="Square image variants (1080x1080)")
    compliance: Dict[str, Any] = Field(..., description="Character counts and validation metrics")


class SubstackNewsletterContent(BaseModel):
    """Substack Newsletter content schema"""
    subject: str = Field(..., min_length=30, max_length=65, description="Email subject line, 30-65 characters")
    preheader: str = Field(..., min_length=50, max_length=90, description="Preheader text, 50-90 characters")
    alt_subject_tests: List[str] = Field(..., min_items=2, max_items=2, description="2 alternative subject lines")
    markdown: str = Field(..., description="Complete newsletter in markdown format with personal opening")
    sections: List[Dict[str, Any]] = Field(..., min_items=3, max_items=6, description="3-6 newsletter sections")
    key_takeaways: List[str] = Field(..., min_items=3, max_items=3, description="Exactly 3 key takeaways")
    resources: List[Dict[str, Any]] = Field(..., min_items=2, max_items=8, description="2-8 resource links")
    subscribe_cta: Dict[str, Any] = Field(..., description="Subscribe call-to-action with link")
    image_prompts: List[Dict[str, Any]] = Field(default_factory=list, description="Optional cover + inline images")
    seo: Dict[str, Any] = Field(..., description="Meta title, description, and keyword usage")
    compliance: Dict[str, Any] = Field(..., description="Word count, character limits, and validation metrics")


class MediumArticleContent(BaseModel):
    """Medium Article content schema"""
    title: str = Field(..., max_length=60, description="SEO-optimized headline, ≤60 characters")
    subtitle: str = Field(..., max_length=120, description="Clarifying promise, ≤120 characters")
    reading_time_min: int = Field(..., ge=3, le=8, description="Estimated reading time in minutes")
    tags: List[str] = Field(..., min_items=5, max_items=7, description="5-7 Medium-style capitalized tags")
    markdown: str = Field(..., description="Complete article in markdown format with headers, code, diagrams")
    sections: List[Dict[str, Any]] = Field(..., min_items=3, max_items=7, description="3-7 H2 sections with summaries")
    code_snippets: List[Dict[str, Any]] = Field(default_factory=list, description="0-3 code blocks with language tags")
    diagram_blocks: List[Dict[str, Any]] = Field(..., min_items=1, description="≥1 mermaid/ascii diagram with alt text")
    pull_quotes: List[str] = Field(..., min_items=1, max_items=2, description="1-2 emphasized lines")
    cta: Dict[str, Any] = Field(..., description="Call-to-action with text and optional link")
    references: List[Dict[str, Any]] = Field(default_factory=list, description="0-6 source references")
    image_prompts: List[Dict[str, Any]] = Field(..., min_items=1, description="Cover + optional inline images")
    seo: Dict[str, Any] = Field(..., description="Slug, meta title, description, and keyword usage")
    compliance: Dict[str, Any] = Field(..., description="Word count, character limits, and validation metrics")


class RedditPostContent(BaseModel):
    """Reddit Post content schema"""
    title: str = Field(..., max_length=300, description="Clear, factual, non-clickbait title, ≤300 characters")
    body: str = Field(..., description="Value-first markdown body with no links in first 2 paragraphs")
    structure: Dict[str, Any] = Field(..., description="Paragraph structure and link placement plan")
    suggested_subreddits: List[Dict[str, Any]] = Field(..., min_items=3, max_items=3, description="Exactly 3 relevant subreddits with rules and timing")
    comment_preparation: Dict[str, Any] = Field(..., description="Top-level comment seeds and FAQ responses")
    image_prompts: List[Dict[str, Any]] = Field(default_factory=list, description="Optional single diagram image")
    moderation_notes: List[str] = Field(..., description="Guidelines for avoiding promotional content")
    compliance: Dict[str, Any] = Field(..., description="Character limits, link placement, and validation metrics")


class HackerNewsItemContent(BaseModel):
    """Hacker News Item content schema"""
    title: str = Field(..., max_length=80, description="Precise, factual title, ≤80 characters, no emojis")
    summary: str = Field(..., description="2-3 neutral sentences with concrete facts/numbers")
    link: str = Field(default="", description="Canonical URL with no tracking parameters")
    text_post: str = Field(default="", description="Text content for Show HN or discussion posts")
    is_show_hn: bool = Field(default=False, description="Whether this is a Show HN submission")
    show_hn_variant: Dict[str, Any] = Field(..., description="Show HN specific fields and metadata")
    comment_preparation: Dict[str, Any] = Field(..., description="Technical details for anticipated questions")
    moderation_notes: List[str] = Field(..., description="Guidelines for HN community standards")
    compliance: Dict[str, Any] = Field(..., description="Character limits, URL validation, and HN rules compliance")


class DevToArticleContent(BaseModel):
    """dev.to Article content schema"""
    front_matter: Dict[str, Any] = Field(..., description="dev.to front matter with title, tags, cover_image, canonical_url")
    markdown: str = Field(..., description="Complete article in dev.to markdown format with front matter")
    reading_time_min: int = Field(..., ge=5, le=15, description="Estimated reading time in minutes")
    code_snippets: List[Dict[str, Any]] = Field(..., min_items=2, max_items=5, description="2-5 runnable code examples with language fences")
    diagram_blocks: List[Dict[str, Any]] = Field(..., min_items=1, description="≥1 mermaid/ascii diagram with alt text")
    resources: List[Dict[str, Any]] = Field(default_factory=list, description="0-5 external resources and references")
    image_prompts: List[Dict[str, Any]] = Field(..., min_items=1, description="Cover image + optional inline diagrams")
    seo: Dict[str, Any] = Field(..., description="Keywords used and SEO metadata")
    compliance: Dict[str, Any] = Field(..., description="Word count, code snippets, tags, and dev.to rules compliance")


class HashnodeArticleContent(BaseModel):
    """Hashnode Article content schema"""
    front_matter: Dict[str, Any] = Field(..., description="Hashnode front matter with title, tags, slug, cover_image, canonical_url")
    markdown: str = Field(..., description="Complete article in markdown format with TOC and structured sections")
    reading_time_min: int = Field(..., ge=7, le=20, description="Estimated reading time in minutes")
    toc: List[Dict[str, Any]] = Field(..., min_items=4, max_items=7, description="Table of contents with titles and anchors")
    sections: List[Dict[str, Any]] = Field(..., min_items=4, max_items=7, description="4-7 H2 sections with summaries and key points")
    code_snippets: List[Dict[str, Any]] = Field(..., min_items=2, max_items=5, description="2-5 runnable code examples")
    diagram_blocks: List[Dict[str, Any]] = Field(..., min_items=1, description="≥1 mermaid/ascii diagram with alt text")
    series_potential: Dict[str, Any] = Field(..., description="Series information and suggested follow-up parts")
    seo: Dict[str, Any] = Field(..., description="SEO metadata with title, description, and keywords")
    cta: Dict[str, Any] = Field(..., description="Call-to-action with text and optional tracked link")
    image_prompts: List[Dict[str, Any]] = Field(default_factory=list, description="Cover + optional inline images")
    compliance: Dict[str, Any] = Field(..., description="Word count, TOC, sections, and Hashnode rules compliance")


class GitHubPagesContent(BaseModel):
    """GitHub Pages content schema"""
    repo_skeleton: List[str] = Field(..., min_items=3, description="Repository structure with key files and directories")
    badges: List[Dict[str, Any]] = Field(..., min_items=2, description="GitHub badges for CI, license, etc.")
    readme_markdown: str = Field(..., description="Complete README.md with all required sections")
    gh_pages: Dict[str, Any] = Field(..., description="GitHub Pages configuration with index.md and _config.yml")
    ci_suggestion: Dict[str, Any] = Field(..., description="GitHub Actions CI workflow configuration")
    discussions_seed: Dict[str, Any] = Field(..., description="GitHub Discussions post template with feedback questions")
    labels_suggestions: List[Dict[str, Any]] = Field(..., min_items=3, max_items=8, description="Repository label suggestions")
    image_prompts: List[Dict[str, Any]] = Field(default_factory=list, description="Repository diagram + optional badge sprite")
    compliance: Dict[str, Any] = Field(..., description="README sections, discussions, and GitHub Pages compliance")


class NotionPageContent(BaseModel):
    """Notion Page content schema"""
    page_title: str = Field(..., max_length=80, description="Page title matching topic_title")
    properties: Dict[str, Any] = Field(..., description="Page properties with tags, status, and canonical_url")
    blocks: List[Dict[str, Any]] = Field(..., min_items=10, description="Notion blocks including H1, TOC, H2 sections, toggles, callouts, code")
    column_layout: Dict[str, Any] = Field(..., description="Two-column layout configuration with children blocks")
    database_inline: Dict[str, Any] = Field(..., description="Inline database definition with schema and sample rows")
    embeds: List[Dict[str, Any]] = Field(..., min_items=1, description="Bookmark and other embeds with tracked links")
    image_prompts: List[Dict[str, Any]] = Field(default_factory=list, description="Cover + optional inline diagrams and quote cards")
    compliance: Dict[str, Any] = Field(..., description="H1/H2 sections, TOC, toggles, callouts, and Notion-specific compliance")


class PersonalBlogPostContent(BaseModel):
    """Personal Blog Post content schema"""
    front_matter: Dict[str, Any] = Field(..., description="YAML front matter with title, description, tags, slug, date, image, canonical")
    open_graph: Dict[str, Any] = Field(..., description="Open Graph metadata for social sharing")
    json_ld: Dict[str, Any] = Field(..., description="JSON-LD Article schema for SEO")
    markdown: str = Field(..., description="Complete blog post in markdown format with front matter")
    reading_time_min: int = Field(..., ge=7, le=15, description="Estimated reading time in minutes")
    sections: List[Dict[str, Any]] = Field(..., min_items=4, max_items=7, description="4-7 H2 sections with summaries and key points")
    code_snippets: List[Dict[str, Any]] = Field(..., min_items=1, max_items=3, description="1-3 code snippets if relevant")
    diagram_blocks: List[Dict[str, Any]] = Field(..., min_items=1, description="≥1 mermaid/ascii diagram with alt text")
    internal_link_opportunities: List[Dict[str, Any]] = Field(..., min_items=3, max_items=8, description="Internal linking suggestions")
    newsletter_cta: Dict[str, Any] = Field(..., description="Newsletter call-to-action with link")
    engagement_prompt: str = Field(..., description="Comment engagement question at the end")
    image_prompts: List[Dict[str, Any]] = Field(default_factory=list, description="Cover + optional inline diagrams and quote cards")
    seo: Dict[str, Any] = Field(..., description="SEO metadata with title, description, and keywords")
    compliance: Dict[str, Any] = Field(..., description="Word count, sections, and blog post compliance")


class GhostPostContent(BaseModel):
    """Ghost CMS Post content schema"""
    post: Dict[str, Any] = Field(..., description="Post fields: title, excerpt, tags, internal_tags, feature_image, visibility, html")
    meta_fields: Dict[str, Any] = Field(..., description="Meta and social fields: meta_title, meta_description, og_*, twitter_*, canonical_url")
    newsletter: Dict[str, Any] = Field(..., description="Newsletter variant: subject, preheader, html")
    image_prompts: List[Dict[str, Any]] = Field(default_factory=list, description="Cover + optional inline diagrams and quote cards")
    compliance: Dict[str, Any] = Field(..., description="Word count, excerpt length, tags count, sections, and Ghost-specific compliance")


class TelegramPostContent(BaseModel):
    """Telegram Post content schema"""
    post: str = Field(..., min_length=90, max_length=160, description="Main post text 90-160 chars with ≤3 emojis")
    alt_versions: List[str] = Field(..., min_items=2, max_items=2, description="Exactly 2 alternative versions ≤160 chars each")
    extended_post: str = Field(default="", description="Optional 300-500 char follow-up message for thread/comments")
    link: Dict[str, Any] = Field(..., description="Link object with url, short, preview, instant_view_hint, fallback")
    hashtags: List[str] = Field(..., min_items=3, max_items=8, description="3-8 compact channel tags lowercase")
    emoji_suggestions: List[str] = Field(..., min_items=1, max_items=3, description="1-3 tasteful emojis")
    image_prompts: List[Dict[str, Any]] = Field(default_factory=list, description="2 square cards (1080x1080) when include_images=true")
    compliance: Dict[str, Any] = Field(..., description="Character counts, link validation, and Telegram-specific compliance")


# Envelope schema
class ContentEnvelope(BaseModel):
    meta: ContentMeta
    content: Union[InstagramReelContent, InstagramCarouselContent, InstagramStoryContent, InstagramPostContent, LinkedInPostContent, LinkedInCarouselContent, XTwitterThreadContent, YouTubeShortContent, YouTubeLongFormContent, FacebookPostContent, ThreadsPostContent, SubstackNewsletterContent, MediumArticleContent, RedditPostContent, HackerNewsItemContent, DevToArticleContent, HashnodeArticleContent, GitHubPagesContent, NotionPageContent, PersonalBlogPostContent, GhostPostContent, TelegramPostContent]


# Schema validator switch
def validate_content(platform: str, format: str, content_data: Dict[str, Any]) -> BaseModel:
    """
    Validate content against platform-specific schema.
    
    Args:
        platform: Platform name (e.g., 'instagram')
        format: Format name (e.g., 'carousel')
        content_data: Raw content data to validate
        
    Returns:
        Validated content model
        
    Raises:
        ValueError: If platform:format combination is not supported
    """
    schema_map = {
        ('instagram', 'reel'): InstagramReelContent,
        ('instagram', 'carousel'): InstagramCarouselContent,
        ('instagram', 'story'): InstagramStoryContent,
        ('instagram', 'post'): InstagramPostContent,
        ('linkedin', 'post'): LinkedInPostContent,
        ('linkedin', 'carousel'): LinkedInCarouselContent,
        ('x_twitter', 'thread'): XTwitterThreadContent,
        ('youtube', 'short'): YouTubeShortContent,
        ('youtube', 'long_form'): YouTubeLongFormContent,
        ('facebook', 'post'): FacebookPostContent,
        ('threads', 'post'): ThreadsPostContent,
        ('substack', 'newsletter'): SubstackNewsletterContent,
        ('medium', 'article'): MediumArticleContent,
        ('reddit', 'post'): RedditPostContent,
        ('hacker_news', 'item'): HackerNewsItemContent,
        ('devto', 'article'): DevToArticleContent,
        ('hashnode', 'article'): HashnodeArticleContent,
        ('github_pages', 'content'): GitHubPagesContent,
        ('notion', 'page'): NotionPageContent,
        ('personal_blog', 'post'): PersonalBlogPostContent,
        ('ghost', 'post'): GhostPostContent,
        ('telegram', 'post'): TelegramPostContent,
    }
    
    key = (platform, format)
    if key not in schema_map:
        raise ValueError(f"Unsupported platform:format combination: {platform}:{format}")
    
    schema_class = schema_map[key]
    return schema_class(**content_data)


# Health check schema
class HealthResponse(BaseModel):
    status: str = "ok"
