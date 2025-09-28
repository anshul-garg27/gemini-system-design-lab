#!/usr/bin/env python3
"""
Test suite for Ghost CMS Post content generation format.
Tests prompt processing, schema validation, and direct schema instantiation.
"""

import json
import sys
import os
from pathlib import Path

# Add the app directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent))

from schemas import validate_content, GhostPostContent


def load_prompt_template():
    """Load the Ghost post prompt template."""
    prompt_path = Path(__file__).parent / "prompts" / "bodies" / "ghost-post.txt"
    with open(prompt_path, 'r', encoding='utf-8') as f:
        return f.read()


def test_prompt_processing():
    """Test that the prompt template loads and processes correctly."""
    print("=== Test 1: Prompt Template Processing ===")
    
    try:
        prompt_template = load_prompt_template()
        
        # Verify key sections exist
        assert "Ghost CMS post" in prompt_template
        assert "platform=\"ghost\"" in prompt_template
        assert "format=\"post\"" in prompt_template
        assert "prompt_version=\"ghost-post-1.2\"" in prompt_template
        
        # Verify Ghost-specific requirements
        assert "excerpt (≤150 chars)" in prompt_template
        assert "internal_tags" in prompt_template
        assert "feature_image" in prompt_template
        assert "member_teaser_html" in prompt_template
        assert "newsletter_html" in prompt_template
        
        # Verify compliance requirements
        assert "4–7 H2 sections" in prompt_template
        assert "≥1 code block" in prompt_template
        assert "≥1 diagram" in prompt_template
        assert "canonical_url" in prompt_template
        
        print("✓ Prompt template loaded successfully")
        print(f"✓ Template length: {len(prompt_template)} characters")
        print("✓ All required Ghost CMS sections present")
        
    except Exception as e:
        print(f"✗ Prompt processing failed: {e}")
        return False
    
    return True


def test_schema_validation():
    """Test schema validation with realistic Ghost post content."""
    print("\n=== Test 2: Schema Validation ===")
    
    # Realistic Ghost post sample data
    sample_content = {
        "post": {
            "title": "Building Scalable Microservices with Docker Compose",
            "excerpt": "Learn how to orchestrate multiple services using Docker Compose for local development and testing environments.",
            "tags": ["docker", "microservices", "devops", "containers"],
            "internal_tags": ["#tutorial", "#backend"],
            "feature_image": "https://systemdesign.com/images/ghost/1234-cover.png",
            "feature_image_alt": "Docker containers orchestrated with compose showing service connections",
            "visibility": "public",
            "html": "<h1>Building Scalable Microservices with Docker Compose</h1>\n<p class=\"intro\">Microservices architecture has become the gold standard for building scalable applications. In this comprehensive guide, we'll explore how Docker Compose simplifies the orchestration of multiple services, making local development and testing environments more manageable and production-like.</p>\n<h2>Background</h2>\n<p>Over 85% of enterprises now use containerized microservices for their core applications.</p>\n<h2>How it works</h2>\n<p>Docker Compose uses YAML configuration files to define multi-container applications.</p>\n<pre><code class=\"language-mermaid\">flowchart LR\nA[API Gateway]-->B[User Service]\nA-->C[Order Service]\nB-->D[Database]\nC-->D\n</code></pre>\n<p class=\"kg-card-caption\">Alt: Microservices flow from API gateway to individual services and shared database.</p>\n<h2>Implementation</h2>\n<pre><code class=\"language-bash\"># Start all services\ndocker-compose up -d\n</code></pre>\n<pre><code class=\"language-yaml\">version: '3.8'\nservices:\n  api:\n    build: ./api\n    ports:\n      - \"3000:3000\"\n  db:\n    image: postgres:13\n    environment:\n      POSTGRES_DB: myapp\n</code></pre>\n<h2>Trade-offs & pitfalls</h2>\n<ul><li>Pro: Simplified local development</li><li>Con: Network complexity in production</li></ul>\n<h2>Case study</h2>\n<p>Spotify reduced deployment time by 60% using containerized microservices.</p>\n<h2>Conclusion</h2>\n<p>Docker Compose provides an excellent foundation for microservices development. For production deployment strategies, check out our <a href=\"https://systemdesign.com/microservices-production?utm_source=ghost&utm_medium=post\">advanced guide</a>.</p>",
            "member_teaser_html": "<p>Members get exclusive access to our production deployment checklist, including Kubernetes manifests, monitoring setup, and security configurations that we use for enterprise clients.</p>",
            "newsletter_html": "<h1>Building Scalable Microservices with Docker Compose</h1><p><em>Your weekly dose of system design insights.</em></p><p>This week we're diving into Docker Compose for microservices orchestration. It's a game-changer for local development workflows.</p><p>Key takeaway: Start simple with compose, then graduate to Kubernetes for production.</p><p><a href=\"https://systemdesign.com/microservices-production?utm_source=ghost&utm_medium=post\">Read the full breakdown</a></p>"
        },
        "meta_fields": {
            "meta_title": "Docker Compose for Microservices | System Design Guide",
            "meta_description": "Learn to build scalable microservices with Docker Compose. Complete guide covering orchestration, local development, and production deployment strategies.",
            "og_title": "Building Scalable Microservices with Docker Compose",
            "og_description": "Learn to build scalable microservices with Docker Compose. Complete guide covering orchestration, local development, and production deployment strategies.",
            "og_image": "https://systemdesign.com/images/ghost/1234-cover.png",
            "twitter_title": "Building Scalable Microservices with Docker Compose",
            "twitter_description": "Learn to build scalable microservices with Docker Compose. Complete guide covering orchestration, local development, and production deployment strategies.",
            "twitter_image": "https://systemdesign.com/images/ghost/1234-cover.png",
            "canonical_url": "https://systemdesign.com/microservices-production"
        },
        "newsletter": {
            "subject": "Docker Compose for Microservices: Complete Guide",
            "preheader": "Orchestrate multiple services like a pro",
            "html": "<h1>Building Scalable Microservices with Docker Compose</h1><p><em>Your weekly dose of system design insights.</em></p><p>This week we're diving into Docker Compose for microservices orchestration. It's a game-changer for local development workflows.</p><p>Key takeaway: Start simple with compose, then graduate to Kubernetes for production.</p><p><a href=\"https://systemdesign.com/microservices-production?utm_source=ghost&utm_medium=post\">Read the full breakdown</a></p>"
        },
        "image_prompts": [
            {
                "role": "cover",
                "title": "Ghost Cover",
                "prompt": "Widescreen minimal banner for Docker microservices: bold short headline area (4–7 words) top-left; small container diagram glyph on right; off-white/light background; thin vector strokes; subtle dotted grid; blue accent color; generous margins; flat vector; crisp at 1200×630.",
                "negative_prompt": "no stock-photo people, no logos, no neon, no 3D bevels, no glossy gradients, no clutter",
                "style_notes": "editorial-tech; crisp kerning; consistent stroke widths",
                "ratio": "1.91:1",
                "size_px": "1200x630",
                "alt_text": "Wide banner with Docker headline space and container diagram glyph"
            }
        ],
        "compliance": {
            "word_count": 1650,
            "excerpt_char_count": 142,
            "tags_count": 4,
            "internal_tags_count": 2,
            "sections_count": 6,
            "code_blocks_count": 2,
            "diagram_blocks_count": 1,
            "has_member_teaser": True,
            "has_newsletter_html": True,
            "has_canonical": True,
            "has_tracked_link_once": True,
            "image_prompt_count": 1,
            "keyword_overrides": False,
            "checks": [
                "excerpt ≤150 chars, plain language",
                "4–7 H2 sections; intro 150–200 words",
                "≥1 code block and ≥1 diagram with caption",
                "3–6 public tags; 0–3 internal #tags",
                "feature image URL + alt provided if cover used",
                "canonical URL set iff primary_url present (no tracking)",
                "exactly one tracked deep link if primary_url present",
                "newsletter subject ≤65 & preheader 50–90; email-safe HTML",
                "image_prompts length == image_plan.count (default 1 cover)"
            ]
        }
    }
    
    try:
        # Test schema validation
        validated_content = validate_content('ghost', 'post', sample_content)
        
        print("✓ Schema validation passed")
        print(f"✓ Post title: {validated_content.post['title']}")
        print(f"✓ Excerpt length: {len(validated_content.post['excerpt'])} chars")
        print(f"✓ Tags count: {len(validated_content.post['tags'])}")
        print(f"✓ Internal tags count: {len(validated_content.post['internal_tags'])}")
        print(f"✓ Word count: {validated_content.compliance['word_count']}")
        
        # Verify Ghost-specific constraints
        assert len(validated_content.post['excerpt']) <= 150
        assert 3 <= len(validated_content.post['tags']) <= 6
        assert len(validated_content.post['internal_tags']) <= 3
        assert all(tag.startswith('#') for tag in validated_content.post['internal_tags'])
        assert validated_content.compliance['sections_count'] >= 4
        assert validated_content.compliance['code_blocks_count'] >= 1
        assert validated_content.compliance['diagram_blocks_count'] >= 1
        
        print("✓ All Ghost CMS constraints validated")
        
    except Exception as e:
        print(f"✗ Schema validation failed: {e}")
        return False
    
    return True


def test_direct_schema_instantiation():
    """Test direct schema instantiation and JSON serialization."""
    print("\n=== Test 3: Direct Schema Instantiation ===")
    
    # Minimal valid Ghost post data
    minimal_data = {
        "post": {
            "title": "Quick Docker Tips",
            "excerpt": "Essential Docker commands every developer should know for faster container workflows.",
            "tags": ["docker", "tips", "devops"],
            "internal_tags": ["#quicktips"],
            "feature_image": "https://example.com/docker-tips.png",
            "feature_image_alt": "Docker command line interface showing essential commands",
            "visibility": "public",
            "html": "<h1>Quick Docker Tips</h1>\n<p class=\"intro\">Docker has revolutionized how we deploy applications. These essential commands will speed up your container workflows and make you more productive with containerized development.</p>\n<h2>Essential Commands</h2>\n<p>Start with these core Docker commands.</p>\n<h2>Image Management</h2>\n<p>Learn to build and manage images efficiently.</p>\n<pre><code class=\"language-bash\">docker build -t myapp .\ndocker images\n</code></pre>\n<h2>Container Operations</h2>\n<p>Running and managing containers.</p>\n<pre><code class=\"language-mermaid\">flowchart LR\nA[Build]-->B[Run]\nB-->C[Deploy]\n</code></pre>\n<p class=\"kg-card-caption\">Alt: Docker workflow from build to deployment.</p>\n<h2>Debugging</h2>\n<p>Troubleshoot container issues.</p>\n<h2>Conclusion</h2>\n<p>Master these commands for Docker success.</p>",
            "member_teaser_html": "<p>Members get our complete Docker cheat sheet with advanced networking and volume management commands.</p>",
            "newsletter_html": "<h1>Quick Docker Tips</h1><p><em>Weekly container insights.</em></p><p>Essential Docker commands to boost your productivity.</p>"
        },
        "meta_fields": {
            "meta_title": "Quick Docker Tips | Essential Commands",
            "meta_description": "Essential Docker commands every developer should know for faster container workflows and improved productivity.",
            "og_title": "Quick Docker Tips",
            "og_description": "Essential Docker commands every developer should know for faster container workflows and improved productivity.",
            "og_image": "https://example.com/docker-tips.png",
            "twitter_title": "Quick Docker Tips",
            "twitter_description": "Essential Docker commands every developer should know for faster container workflows and improved productivity.",
            "twitter_image": "https://example.com/docker-tips.png",
            "canonical_url": ""
        },
        "newsletter": {
            "subject": "Docker Tips: Essential Commands",
            "preheader": "Boost your container productivity",
            "html": "<h1>Quick Docker Tips</h1><p><em>Weekly container insights.</em></p><p>Essential Docker commands to boost your productivity.</p>"
        },
        "image_prompts": [],
        "compliance": {
            "word_count": 850,
            "excerpt_char_count": 89,
            "tags_count": 3,
            "internal_tags_count": 1,
            "sections_count": 5,
            "code_blocks_count": 1,
            "diagram_blocks_count": 1,
            "has_member_teaser": True,
            "has_newsletter_html": True,
            "has_canonical": False,
            "has_tracked_link_once": False,
            "image_prompt_count": 0,
            "keyword_overrides": False,
            "checks": []
        }
    }
    
    try:
        # Test direct instantiation
        ghost_post = GhostPostContent(**minimal_data)
        
        print("✓ Direct schema instantiation successful")
        print(f"✓ Post title: {ghost_post.post['title']}")
        print(f"✓ Newsletter subject: {ghost_post.newsletter['subject']}")
        
        # Test JSON serialization
        json_output = ghost_post.model_dump_json(indent=2)
        parsed_back = json.loads(json_output)
        
        print("✓ JSON serialization successful")
        print(f"✓ JSON length: {len(json_output)} characters")
        
        # Verify structure preservation
        assert parsed_back['post']['title'] == minimal_data['post']['title']
        assert parsed_back['meta_fields']['meta_title'] == minimal_data['meta_fields']['meta_title']
        assert parsed_back['newsletter']['subject'] == minimal_data['newsletter']['subject']
        
        print("✓ JSON structure preserved correctly")
        
    except Exception as e:
        print(f"✗ Direct instantiation failed: {e}")
        return False
    
    return True


def main():
    """Run all tests for Ghost post format."""
    print("Ghost CMS Post Format - Test Suite")
    print("=" * 50)
    
    tests = [
        test_prompt_processing,
        test_schema_validation,
        test_direct_schema_instantiation
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        else:
            print("Test failed, stopping execution.")
            break
    
    print(f"\n=== Test Results ===")
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! Ghost post format is ready for use.")
        return True
    else:
        print("❌ Some tests failed. Please check the implementation.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
