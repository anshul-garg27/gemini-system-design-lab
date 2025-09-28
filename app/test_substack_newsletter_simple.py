#!/usr/bin/env python3
"""
Simple test script for Substack Newsletter content generation.
Tests prompt processing, schema validation, and direct schema instantiation.
"""

import sys
import os
import json
from pathlib import Path

# Add the app directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from prompt_processor import PromptProcessor
from schemas import SubstackNewsletterContent, validate_content

def test_prompt_processing():
    """Test Substack Newsletter prompt template processing"""
    print("=" * 60)
    print("TEST 1: Substack Newsletter Prompt Processing")
    print("=" * 60)
    
    try:
        processor = PromptProcessor()
        
        # Test data
        topic_id = "4001"
        topic_name = "API Rate Limiting Strategies"
        topic_description = "Comprehensive guide to implementing rate limiting in APIs including token bucket, sliding window, and fixed window algorithms to prevent abuse and ensure fair usage across distributed systems."
        
        # Process the prompt template
        prompt_path = "prompts/bodies/substack-newsletter.txt"
        processed_prompt = processor.process_prompt_template(
            template_path=prompt_path,
            topic_id=topic_id,
            topic_name=topic_name,
            topic_description=topic_description,
            platform="substack",
            format_type="newsletter"
        )
        
        print(f"✅ Prompt template processed successfully")
        print(f"📄 Template path: {prompt_path}")
        print(f"🎯 Topic: {topic_name}")
        print(f"📝 Processed prompt length: {len(processed_prompt)} characters")
        print(f"🔍 Contains topic name: {'✅' if topic_name in processed_prompt else '❌'}")
        print(f"🔍 Contains JSON format: {'✅' if 'markdown' in processed_prompt else '❌'}")
        print(f"🔍 Contains newsletter structure: {'✅' if 'key_takeaways' in processed_prompt else '❌'}")
        print(f"🔍 Contains subscribe CTA: {'✅' if 'subscribe_cta' in processed_prompt else '❌'}")
        
        # Show first 500 characters of processed prompt
        print(f"\n📋 Prompt preview (first 500 chars):")
        print("-" * 50)
        print(processed_prompt[:500] + "..." if len(processed_prompt) > 500 else processed_prompt)
        print("-" * 50)
        
        return True
        
    except Exception as e:
        print(f"❌ Prompt processing failed: {str(e)}")
        return False

def test_schema_validation():
    """Test Substack Newsletter schema validation with sample data"""
    print("\n" + "=" * 60)
    print("TEST 2: Substack Newsletter Schema Validation")
    print("=" * 60)
    
    # Sample Substack Newsletter content matching the schema
    sample_content = {
        "subject": "The API rate limiting mistake that crashed our startup",
        "preheader": "How we went from 500 errors/sec to bulletproof rate limiting in 48 hours",
        "alt_subject_tests": [
            "Rate limiting: the startup killer nobody talks about",
            "From API chaos to rate limiting mastery in 48 hours"
        ],
        "markdown": """# The API rate limiting mistake that crashed our startup

*How we went from 500 errors/sec to bulletproof rate limiting in 48 hours*

Hi there —

**3 AM on a Tuesday.** Our API was returning 500 errors faster than I could refresh the monitoring dashboard. 50,000 requests per second from a single IP address. Our startup's core service was down, and I had no idea how to stop it.

That's when I learned that rate limiting isn't just a "nice to have" — it's the difference between a scalable business and a 3 AM nightmare.

## What's inside
- The 3 rate limiting algorithms that actually work in production
- Why token bucket saved our startup (and when to avoid it)
- Real implementation examples with performance benchmarks

## The problem with naive rate limiting

Most developers start with the simplest approach: count requests per minute and block when you hit the limit.

```python
# Don't do this
if requests_this_minute[user_id] > 100:
    return "Rate limit exceeded"
```

This breaks down immediately under real traffic. Users get frustrated by hard cutoffs. Legitimate traffic gets blocked alongside abuse.

We learned this the hard way when our mobile app started retrying failed requests, creating a cascade of rate limit violations.

## Token bucket: the algorithm that saved us

Token bucket gives users a "budget" of requests they can spend over time.

**How it works:**
- Each user gets a bucket with N tokens
- Each request consumes 1 token
- Tokens refill at a steady rate (e.g., 10 per minute)
- Burst traffic is allowed until tokens run out

**The magic:** Users can make quick bursts of requests when they have tokens saved up, but sustained abuse gets throttled naturally.

**Implementation:**
```python
class TokenBucket:
    def __init__(self, capacity, refill_rate):
        self.capacity = capacity
        self.tokens = capacity
        self.refill_rate = refill_rate
        self.last_refill = time.time()
    
    def consume(self, tokens=1):
        self._refill()
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False
    
    def _refill(self):
        now = time.time()
        tokens_to_add = (now - self.last_refill) * self.refill_rate
        self.tokens = min(self.capacity, self.tokens + tokens_to_add)
        self.last_refill = now
```

**Results:** API error rate dropped from 15% to 0.1% within hours of deployment.

## Sliding window: precision at scale

For high-traffic APIs, sliding window gives more precise control than fixed time windows.

Instead of "100 requests per hour" (which allows 100 requests in the last second of one hour + 100 in the first second of the next), sliding window tracks "100 requests in any 60-minute period."

**Trade-off:** More memory usage (you need to store timestamps) but much smoother user experience.

**When to use:** High-value APIs where user experience matters more than memory efficiency.

## Fixed window: simple and effective

Sometimes simple is better. Fixed window resets counters at regular intervals (every minute, hour, etc.).

**Pros:**
- Minimal memory usage
- Easy to implement and debug
- Predictable behavior

**Cons:**
- Allows burst traffic at window boundaries
- Less smooth user experience

**Perfect for:** Internal APIs, batch processing systems, or when memory is constrained.

## Key takeaways
- Start with token bucket for user-facing APIs — it provides the best balance of protection and user experience
- Use sliding window when precision matters more than memory efficiency
- Fixed window works great for internal systems where simplicity trumps smoothness

## Resources
- [Redis Rate Limiting Patterns](https://redis.io/docs/manual/patterns/distributed-locks/) — battle-tested implementations
- [GitHub's Rate Limiting](https://docs.github.com/en/rest/overview/resources-in-the-rest-api#rate-limiting) — real-world example of token bucket
- [Stripe's Rate Limiting Guide](https://stripe.com/docs/rate-limits) — sliding window in production
- [Kong Rate Limiting Plugin](https://docs.konghq.com/hub/kong-inc/rate-limiting/) — multiple algorithms in one tool

## Before you go

Rate limiting saved our startup from that 3 AM meltdown. The right algorithm can mean the difference between scaling smoothly and losing customers to downtime.

If this helped, consider subscribing and sharing with your team.

👉 **Read the complete rate limiting implementation guide** (https://systemdesign.com/rate-limiting?utm_source=substack&utm_medium=newsletter)

— @systemdesign""",
        "sections": [
            {
                "h2": "The problem with naive rate limiting",
                "summary": "Simple request counting breaks under real traffic and creates poor user experience",
                "key_points": ["Hard cutoffs frustrate users", "Legitimate traffic gets blocked", "Retry cascades amplify problems"]
            },
            {
                "h2": "Token bucket: the algorithm that saved us",
                "summary": "Gives users a budget of requests with natural burst handling and smooth throttling",
                "key_points": ["Allows burst traffic", "Natural throttling", "15% to 0.1% error rate improvement"]
            },
            {
                "h2": "Sliding window: precision at scale",
                "summary": "More precise control than fixed windows with smoother user experience",
                "key_points": ["Precise time tracking", "Higher memory usage", "Better user experience"]
            },
            {
                "h2": "Fixed window: simple and effective",
                "summary": "Resets counters at regular intervals with minimal memory and complexity",
                "key_points": ["Minimal memory usage", "Easy implementation", "Predictable behavior"]
            }
        ],
        "key_takeaways": [
            "Start with token bucket for user-facing APIs — it provides the best balance of protection and user experience",
            "Use sliding window when precision matters more than memory efficiency", 
            "Fixed window works great for internal systems where simplicity trumps smoothness"
        ],
        "resources": [
            {
                "title": "Redis Rate Limiting Patterns",
                "url": "https://redis.io/docs/manual/patterns/distributed-locks/",
                "note": "battle-tested implementations",
                "tracked": False
            },
            {
                "title": "GitHub's Rate Limiting",
                "url": "https://docs.github.com/en/rest/overview/resources-in-the-rest-api#rate-limiting",
                "note": "real-world example of token bucket",
                "tracked": False
            },
            {
                "title": "Stripe's Rate Limiting Guide", 
                "url": "https://stripe.com/docs/rate-limits",
                "note": "sliding window in production",
                "tracked": False
            },
            {
                "title": "Kong Rate Limiting Plugin",
                "url": "https://docs.konghq.com/hub/kong-inc/rate-limiting/",
                "note": "multiple algorithms in one tool",
                "tracked": False
            }
        ],
        "subscribe_cta": {
            "text": "Read the complete rate limiting implementation guide",
            "link": "https://systemdesign.com/rate-limiting?utm_source=substack&utm_medium=newsletter",
            "placed_in_markdown": True
        },
        "image_prompts": [
            {
                "role": "cover",
                "title": "Email Cover",
                "prompt": "Wide minimal banner for API Rate Limiting Strategies; headline 'Rate Limiting' center; small API throttle diagram motif right side; off-white/light background; thin vector strokes; subtle dotted grid; red accent color; generous margins; flat vector aesthetic; legible across desktop/mobile/email clients.",
                "negative_prompt": "no stock-photo people, no logos, no neon, no 3D bevels, no glossy gradients, no clutter",
                "style_notes": "editorial poster tone; crisp kerning; consistent stroke widths",
                "ratio": "1.91:1",
                "size_px": "1200x630",
                "alt_text": "Wide banner with rate limiting headline and API throttle diagram motif"
            }
        ],
        "seo": {
            "meta_title": "API Rate Limiting: Token Bucket vs Sliding Window Guide",
            "meta_description": "Learn token bucket, sliding window, and fixed window rate limiting algorithms with real implementation examples and performance benchmarks.",
            "keywords_used": ["rate limiting", "token bucket", "sliding window", "API throttling", "system design"],
            "lsi_terms_used": ["API protection", "request throttling", "burst traffic", "distributed systems", "scalability"]
        },
        "compliance": {
            "word_count": 1456,
            "subject_char_count": 54,
            "preheader_char_count": 69,
            "sections_count": 4,
            "resources_count": 4,
            "image_prompt_count": 1,
            "has_tracked_cta": True,
            "checks": [
                "subject 30–65 chars; preheader 50–90",
                "body 1000–2000 words; email-friendly markdown",
                "personal anecdote opening present",
                "3 key takeaways present",
                "resources section with 2–8 items",
                "exactly one primary tracked CTA if primary_url present",
                "image_prompts length == image_plan.count (default 1)"
            ]
        }
    }
    
    try:
        # Test direct schema validation
        print("🧪 Testing direct schema validation...")
        newsletter_content = SubstackNewsletterContent(**sample_content)
        print(f"✅ Direct schema validation passed")
        print(f"📊 Subject length: {len(newsletter_content.subject)} chars")
        print(f"📝 Word count: {newsletter_content.compliance['word_count']} words")
        print(f"📑 Sections count: {len(newsletter_content.sections)}")
        print(f"🎯 Key takeaways: {len(newsletter_content.key_takeaways)}")
        print(f"📚 Resources: {len(newsletter_content.resources)}")
        print(f"🖼️ Image prompts: {len(newsletter_content.image_prompts)}")
        
        # Test schema validator function
        print(f"\n🧪 Testing schema validator function...")
        validated_content = validate_content('substack', 'newsletter', sample_content)
        print(f"✅ Schema validator function passed")
        print(f"📋 Validated content type: {type(validated_content).__name__}")
        
        # Display sample content structure
        print(f"\n📋 Sample Substack Newsletter Structure:")
        print(f"   • Subject: {len(sample_content['subject'])} characters")
        print(f"   • Preheader: {len(sample_content['preheader'])} characters")
        print(f"   • Alt subjects: {len(sample_content['alt_subject_tests'])} variants")
        print(f"   • Sections: {len(sample_content['sections'])} sections")
        print(f"   • Takeaways: {len(sample_content['key_takeaways'])} points")
        print(f"   • Resources: {len(sample_content['resources'])} links")
        
        return True
        
    except Exception as e:
        print(f"❌ Schema validation failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_direct_schema_instantiation():
    """Test direct instantiation of Substack Newsletter schema"""
    print("\n" + "=" * 60)
    print("TEST 3: Direct Substack Newsletter Schema Instantiation")
    print("=" * 60)
    
    try:
        # Create Substack Newsletter content directly
        newsletter_content = SubstackNewsletterContent(
            subject="The caching strategy that 10x'd our performance",
            preheader="From 2-second page loads to 200ms with Redis and smart invalidation",
            alt_subject_tests=[
                "How we cut page load time by 90% with smart caching",
                "The Redis caching pattern that changed everything"
            ],
            markdown="""# The caching strategy that 10x'd our performance

*From 2-second page loads to 200ms with Redis and smart invalidation*

Hi there —

**Our users were leaving.** Page load times averaged 2.3 seconds, and our bounce rate was climbing every week. We knew we had a performance problem, but every optimization felt like putting a band-aid on a broken dam.

Then we implemented a proper caching strategy. Within a week, our average response time dropped to 180ms. User engagement jumped 40%. Here's exactly how we did it.

## What's inside
- The cache-aside pattern that works for 90% of use cases
- Redis configuration that handles millions of requests
- Cache invalidation strategies that prevent stale data

## Cache-aside: the pattern that works

Most caching problems come from trying to be too clever. Cache-aside keeps it simple:

1. Check cache first
2. If miss, fetch from database
3. Store result in cache
4. Return to user

**The key insight:** Let your application control caching logic, not the database.

## Smart invalidation prevents stale data

The hardest part of caching isn't storing data — it's knowing when to remove it.

**Time-based expiration:** Set TTL based on how often data changes
**Event-based invalidation:** Clear cache when underlying data updates
**Version-based keys:** Include version numbers in cache keys

## Redis configuration for scale

Our Redis setup handles 50,000 requests per second:
- Memory optimization with appropriate data structures
- Persistence configuration for durability
- Clustering for horizontal scaling

## Key takeaways
- Start with cache-aside pattern for simplicity and control
- Implement proper invalidation from day one to avoid stale data issues
- Monitor cache hit rates and adjust TTL based on actual usage patterns

## Resources
- [Redis Best Practices](https://redis.io/docs/manual/config/) — production configuration guide
- [Caching Patterns](https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/Strategies.html) — comprehensive pattern overview

## Before you go

Caching transformed our application performance and user experience. The right strategy can turn a slow application into a fast one almost overnight.

👉 **Get the complete caching implementation guide** (https://systemdesign.com/caching?utm_source=substack&utm_medium=newsletter)

— @systemdesign""",
            sections=[
                {
                    "h2": "Cache-aside: the pattern that works",
                    "summary": "Simple caching pattern where application controls cache logic for reliability",
                    "key_points": ["Check cache first", "Application controls logic", "Works for 90% of cases"]
                },
                {
                    "h2": "Smart invalidation prevents stale data",
                    "summary": "Strategies for removing outdated cache entries using time, events, and versioning",
                    "key_points": ["Time-based expiration", "Event-based invalidation", "Version-based keys"]
                },
                {
                    "h2": "Redis configuration for scale",
                    "summary": "Production Redis setup handling 50K requests/second with proper optimization",
                    "key_points": ["Memory optimization", "Persistence configuration", "Horizontal clustering"]
                }
            ],
            key_takeaways=[
                "Start with cache-aside pattern for simplicity and control",
                "Implement proper invalidation from day one to avoid stale data issues",
                "Monitor cache hit rates and adjust TTL based on actual usage patterns"
            ],
            resources=[
                {
                    "title": "Redis Best Practices",
                    "url": "https://redis.io/docs/manual/config/",
                    "note": "production configuration guide",
                    "tracked": False
                },
                {
                    "title": "Caching Patterns",
                    "url": "https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/Strategies.html",
                    "note": "comprehensive pattern overview",
                    "tracked": False
                }
            ],
            subscribe_cta={
                "text": "Get the complete caching implementation guide",
                "link": "https://systemdesign.com/caching?utm_source=substack&utm_medium=newsletter",
                "placed_in_markdown": True
            },
            image_prompts=[
                {
                    "role": "cover",
                    "title": "Email Cover",
                    "prompt": "Wide minimal banner for Caching Strategies; headline 'Smart Caching' center; small cache layer diagram motif; off-white/light background; thin vector strokes; subtle dotted grid; blue accent color; generous margins; flat vector aesthetic; legible across desktop/mobile/email clients.",
                    "negative_prompt": "no stock-photo people, no logos, no neon, no 3D bevels, no glossy gradients, no clutter",
                    "style_notes": "editorial poster tone; crisp kerning; consistent stroke widths",
                    "ratio": "1.91:1",
                    "size_px": "1200x630",
                    "alt_text": "Wide banner with caching headline and cache layer diagram motif"
                }
            ],
            seo={
                "meta_title": "Redis Caching Strategy: Cache-Aside Pattern Guide",
                "meta_description": "Learn cache-aside pattern, Redis configuration, and smart invalidation strategies to improve application performance by 10x.",
                "keywords_used": ["caching strategy", "redis", "cache-aside", "performance optimization", "cache invalidation"],
                "lsi_terms_used": ["application performance", "cache patterns", "data caching", "system optimization", "scalability"]
            },
            compliance={
                "word_count": 1124,
                "subject_char_count": 49,
                "preheader_char_count": 65,
                "sections_count": 3,
                "resources_count": 2,
                "image_prompt_count": 1,
                "has_tracked_cta": True,
                "checks": [
                    "subject 30–65 chars; preheader 50–90",
                    "body 1000–2000 words; email-friendly markdown",
                    "personal anecdote opening present",
                    "3 key takeaways present",
                    "resources section with 2–8 items",
                    "exactly one primary tracked CTA if primary_url present",
                    "image_prompts length == image_plan.count (default 1)"
                ]
            }
        )
        
        print(f"✅ Direct schema instantiation successful")
        print(f"📊 Substack Newsletter structure:")
        print(f"   • Subject: {len(newsletter_content.subject)} characters")
        print(f"   • Preheader: {len(newsletter_content.preheader)} characters")
        print(f"   • Alt subjects: {len(newsletter_content.alt_subject_tests)}")
        print(f"   • Sections: {len(newsletter_content.sections)}")
        print(f"   • Takeaways: {len(newsletter_content.key_takeaways)}")
        print(f"   • Resources: {len(newsletter_content.resources)}")
        print(f"   • Word count: {newsletter_content.compliance['word_count']}")
        
        # Test JSON serialization
        json_output = newsletter_content.model_dump()
        print(f"✅ JSON serialization successful")
        print(f"📄 JSON size: {len(json.dumps(json_output))} characters")
        
        return True
        
    except Exception as e:
        print(f"❌ Direct schema instantiation failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all Substack Newsletter tests"""
    print("🧪 SUBSTACK NEWSLETTER CONTENT GENERATION TESTS")
    print("=" * 60)
    
    results = []
    
    # Run all tests
    results.append(("Prompt Processing", test_prompt_processing()))
    results.append(("Schema Validation", test_schema_validation()))
    results.append(("Direct Schema Instantiation", test_direct_schema_instantiation()))
    
    # Print summary
    print("\n" + "=" * 60)
    print("📋 TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All Substack Newsletter tests passed! Ready for integration.")
    else:
        print("⚠️ Some tests failed. Please review the errors above.")
    
    return passed == len(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)