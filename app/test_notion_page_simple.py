#!/usr/bin/env python3
"""
Test suite for Notion Page content generation.
Tests prompt processing, schema validation, and direct schema instantiation.
"""

import sys
import os
import json
from pathlib import Path

# Add the app directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from schemas import NotionPageContent, validate_content

def load_prompt_template():
    """Load the Notion Page prompt template"""
    prompt_path = Path(__file__).parent / "prompts" / "bodies" / "notion-page.txt"
    if not prompt_path.exists():
        raise FileNotFoundError(f"Prompt template not found: {prompt_path}")
    
    with open(prompt_path, 'r', encoding='utf-8') as f:
        return f.read()

def process_prompt_with_topic(template, topic_data):
    """Process prompt template with topic data"""
    # Sample topic data for testing
    sample_data = {
        "topic_id": "6001",
        "topic_name": topic_data.get("name", "Database Connection Pooling"),
        "topic_description": topic_data.get("description", "Optimizing database performance through intelligent connection pooling strategies and configuration"),
        "audience": "intermediate",
        "tone": "clear, confident, friendly, non-cringe",
        "locale": "en",
        "primary_url": "https://blog.example.com/database-connection-pooling",
        **topic_data.get("brand", {
            "site_url": "https://blog.example.com",
            "handles": {"notion": "@yourspace", "x": "@systemdesign", "linkedin": "@systemdesign", "github": "@systemdesign"},
            "utm_base": "utm_source=notion&utm_medium=page"
        })
    }
    
    # Replace template variables
    processed = template
    for key, value in sample_data.items():
        if isinstance(value, dict):
            # Handle nested objects like brand
            for nested_key, nested_value in value.items():
                processed = processed.replace(f"{{{key}.{nested_key}}}", str(nested_value))
        else:
            processed = processed.replace(f"{{{key}}}", str(value))
    
    return processed

def test_prompt_processing():
    """Test 1: Notion Page prompt template processing"""
    print("=" * 60)
    print("TEST 1: Notion Page Prompt Processing")
    print("=" * 60)
    
    try:
        template = load_prompt_template()
        
        # Test with database connection pooling topic
        topic_data = {
            "name": "Database Connection Pooling",
            "description": "Optimizing database performance through intelligent connection pooling strategies and configuration"
        }
        
        processed_prompt = process_prompt_with_topic(template, topic_data)
        
        print("✅ Prompt template processed successfully")
        print(f"📄 Template path: prompts/bodies/notion-page.txt")
        print(f"🎯 Topic: {topic_data['name']}")
        print(f"📝 Processed prompt length: {len(processed_prompt)} characters")
        
        # Verify key elements are present
        checks = {
            "Contains topic name": topic_data["name"] in processed_prompt,
            "Contains JSON format": '"content":' in processed_prompt,
            "Contains blocks structure": '"blocks":' in processed_prompt,
            "Contains toggle blocks": '"toggle"' in processed_prompt,
            "Contains callout blocks": '"callout"' in processed_prompt,
            "Contains database inline": '"database_inline"' in processed_prompt,
            "Contains column layout": '"column_layout"' in processed_prompt
        }
        
        for check, passed in checks.items():
            print(f"🔍 {check}: {'✅' if passed else '❌'}")
        
        print(f"\n📋 Prompt preview (first 500 chars):")
        print("-" * 50)
        print(processed_prompt[:500] + "...")
        print("-" * 50)
        
        return True
        
    except Exception as e:
        print(f"❌ Prompt processing failed: {e}")
        return False

def test_schema_validation():
    """Test 2: Notion Page schema validation with sample data"""
    print("\n" + "=" * 60)
    print("TEST 2: Notion Page Schema Validation")
    print("=" * 60)
    
    # Sample Notion Page content
    sample_content = {
        "page_title": "Database Connection Pooling",
        
        "properties": {
            "tags": ["database", "performance", "optimization", "backend"],
            "status": "published",
            "canonical_url": "https://blog.example.com/database-connection-pooling"
        },
        
        "blocks": [
            {"type": "heading_1", "text": "Database Connection Pooling"},
            {"type": "paragraph", "text": "Database connection pooling is essential for high-performance applications. Instead of creating new connections for each request, connection pools maintain a set of reusable connections, dramatically reducing latency and resource overhead for intermediate developers building scalable systems."},
            {"type": "table_of_contents", "text": ""},
            
            {"type": "heading_2", "text": "Background"},
            {"type": "bulleted_list_item", "text": "Connection Pool — A cache of database connections shared across application threads"},
            {"type": "bulleted_list_item", "text": "Connection Lifecycle — The process of creating, using, and returning connections to the pool"},
            {"type": "bulleted_list_item", "text": "Pool Sizing — Determining optimal min/max connections based on workload patterns"},
            
            {"type": "heading_2", "text": "How it works"},
            {"type": "paragraph", "text": "Connection pooling works by maintaining a pool of pre-established database connections. When your application needs to query the database, it borrows a connection from the pool, executes the query, and returns the connection for reuse."},
            {"type": "code", "language": "python", "text": "# Basic connection pool setup\nfrom sqlalchemy import create_engine\nfrom sqlalchemy.pool import QueuePool\n\nengine = create_engine(\n    'postgresql://user:pass@localhost/db',\n    poolclass=QueuePool,\n    pool_size=10,\n    max_overflow=20,\n    pool_timeout=30\n)"},
            
            {"type": "toggle", "text": "Advanced pool configuration (open if curious)", "children": [
                {"type": "paragraph", "text": "Advanced configurations include connection validation, retry logic, and monitoring. Pool sizing depends on your application's concurrency patterns and database capacity."},
                {"type": "bulleted_list_item", "text": "Connection validation — Test connections before use with SELECT 1"},
                {"type": "bulleted_list_item", "text": "Pool overflow — Allow temporary connections beyond pool_size during spikes"},
                {"type": "bulleted_list_item", "text": "Connection recycling — Refresh connections periodically to avoid timeouts"}
            ]},
            
            {"type": "callout", "emoji": "💡", "text": "Tip: Start with pool_size = 2 * CPU cores and adjust based on monitoring. Most applications need fewer connections than expected."},
            
            {"type": "heading_2", "text": "Architecture"},
            {"type": "code", "language": "mermaid", "text": "flowchart LR\n    App[Application]-->Pool[Connection Pool]\n    Pool-->DB1[(Database 1)]\n    Pool-->DB2[(Database 2)]\n    Pool-->DB3[(Database 3)]\n    Pool-->|Reuse|App"},
            {"type": "quote", "text": "A well-tuned connection pool can reduce database connection overhead by 90% while improving response times."},
            
            {"type": "heading_2", "text": "Implementation"},
            {"type": "paragraph", "text": "Here's a production-ready implementation with monitoring and health checks:"},
            {"type": "code", "language": "python", "text": "import time\nfrom contextlib import contextmanager\nfrom sqlalchemy import create_engine, text\nfrom sqlalchemy.pool import QueuePool\n\nclass DatabasePool:\n    def __init__(self, connection_string):\n        self.engine = create_engine(\n            connection_string,\n            poolclass=QueuePool,\n            pool_size=10,\n            max_overflow=20,\n            pool_timeout=30,\n            pool_pre_ping=True  # Validate connections\n        )\n    \n    @contextmanager\n    def get_connection(self):\n        conn = self.engine.connect()\n        try:\n            yield conn\n        finally:\n            conn.close()\n    \n    def health_check(self):\n        try:\n            with self.get_connection() as conn:\n                result = conn.execute(text('SELECT 1'))\n                return result.scalar() == 1\n        except Exception:\n            return False"},
            
            {"type": "heading_2", "text": "Resources"},
            {"type": "bookmark", "url": "https://blog.example.com/database-connection-pooling?utm_source=notion&utm_medium=page"},
            {"type": "bulleted_list_item", "text": "SQLAlchemy Pool Documentation — https://docs.sqlalchemy.org/en/14/core/pooling.html"},
            {"type": "bulleted_list_item", "text": "HikariCP (Java) Best Practices — https://github.com/brettwooldridge/HikariCP"},
            
            {"type": "divider", "text": ""},
            
            {"type": "heading_2", "text": "Next steps"},
            {"type": "numbered_list_item", "text": "Implement basic connection pooling in your application"},
            {"type": "numbered_list_item", "text": "Add connection pool monitoring and alerting"},
            {"type": "numbered_list_item", "text": "Benchmark performance improvements and share results"}
        ],
        
        "column_layout": {
            "enabled": True,
            "column_list": [
                {
                    "ratio": 0.5,
                    "children": [
                        {"type": "callout", "emoji": "🧪", "text": "Test idea: Benchmark connection creation vs pool retrieval time. Expect 10-100x improvement with pooling."}
                    ]
                },
                {
                    "ratio": 0.5,
                    "children": [
                        {"type": "code", "language": "bash", "text": "# Quick benchmark script\ntime python -c \"import psycopg2; [psycopg2.connect('...') for _ in range(100)]\"\n# vs pooled connections"}
                    ]
                }
            ]
        },
        
        "database_inline": {
            "enabled": True,
            "name": "Connection Pool Resources",
            "schema": [
                {"name": "Title", "type": "title"},
                {"name": "Type", "type": "select", "options": ["doc", "video", "tool", "benchmark"]},
                {"name": "Link", "type": "url"},
                {"name": "Status", "type": "select", "options": ["to read", "reading", "done"]},
                {"name": "Tags", "type": "multi_select", "options": ["performance", "database", "optimization"]},
                {"name": "Added", "type": "date"}
            ],
            "initial_rows": [
                {
                    "Title": "Primary deep-dive article",
                    "Type": "doc",
                    "Link": "https://blog.example.com/database-connection-pooling?utm_source=notion&utm_medium=page",
                    "Status": "to read",
                    "Tags": ["performance", "database"],
                    "Added": "2024-01-15"
                },
                {
                    "Title": "SQLAlchemy Pool Docs",
                    "Type": "doc",
                    "Link": "https://docs.sqlalchemy.org/en/14/core/pooling.html",
                    "Status": "done",
                    "Tags": ["database"],
                    "Added": "2024-01-15"
                }
            ]
        },
        
        "embeds": [
            {"type": "bookmark", "url": "https://blog.example.com/database-connection-pooling?utm_source=notion&utm_medium=page"},
            {"type": "github_gist", "url": ""},
            {"type": "youtube", "url": ""}
        ],
        
        "image_prompts": [
            {
                "role": "cover",
                "title": "Notion Cover",
                "prompt": "Wide, minimalist cover for Database Connection Pooling: subtle abstract tech pattern with light geometric lines representing connection flows; off-white background; faint grid; blue accent color; generous margins; flat vector aesthetic; composition leaves negative space for overlay title in Notion.",
                "negative_prompt": "no stock-photo people, no logos, no neon, no 3D bevels, no glossy gradients, no clutter",
                "style_notes": "editorial-tech; calm contrast; crisp kerning potential",
                "ratio": "1.91:1",
                "size_px": "1200x630",
                "alt_text": "Subtle abstract tech pattern cover with connection flow lines"
            }
        ],
        
        "compliance": {
            "has_h1": True,
            "h2_sections_count": 5,
            "has_toc": True,
            "toggle_blocks_count": 1,
            "callout_blocks_count": 2,
            "code_blocks_count": 3,
            "embed_count": 1,
            "database_enabled": True,
            "image_prompt_count": 1,
            "has_tracked_bookmark_once": True,
            "checks": [
                "H1 equals topic_title: Database Connection Pooling",
                "TOC placed after intro paragraph",
                "5 H2 sections present (Background, How it works, Architecture, Implementation, Resources, Next steps)",
                "1 toggle with children for advanced configuration",
                "2 callouts (tip + test idea)",
                "3 code blocks (Python setup, mermaid diagram, full implementation)",
                "1 bookmark embed with tracked link",
                "Database inline enabled with schema + 2 sample rows",
                "1 cover image prompt matches image_plan.count"
            ]
        }
    }
    
    try:
        print("🧪 Testing direct schema validation...")
        notion_page = NotionPageContent(**sample_content)
        print("✅ Direct schema validation passed")
        print(f"📄 Page title: {notion_page.page_title}")
        print(f"🏷️ Tags: {len(notion_page.properties['tags'])}")
        print(f"🧱 Blocks: {len(notion_page.blocks)}")
        print(f"📊 H2 sections: {notion_page.compliance['h2_sections_count']}")
        print(f"🔄 Toggle blocks: {notion_page.compliance['toggle_blocks_count']}")
        print(f"💡 Callout blocks: {notion_page.compliance['callout_blocks_count']}")
        print(f"💻 Code blocks: {notion_page.compliance['code_blocks_count']}")
        print(f"🗃️ Database enabled: {notion_page.database_inline['enabled']}")
        
        print("\n🧪 Testing schema validator function...")
        validated_content = validate_content("notion", "page", sample_content)
        print("✅ Schema validator function passed")
        print(f"📋 Validated content type: {type(validated_content).__name__}")
        
        print(f"\n📋 Sample Notion Page Structure:")
        print(f"   • Page title: {len(notion_page.page_title)} characters")
        print(f"   • Properties: {len(notion_page.properties)} fields")
        print(f"   • Blocks: {len(notion_page.blocks)} total blocks")
        print(f"   • Column layout: {'✅' if notion_page.column_layout['enabled'] else '❌'}")
        print(f"   • Inline database: {'✅' if notion_page.database_inline['enabled'] else '❌'}")
        print(f"   • Embeds: {len(notion_page.embeds)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Schema validation failed: {e}")
        return False

def test_direct_schema_instantiation():
    """Test 3: Direct Notion Page schema instantiation"""
    print("\n" + "=" * 60)
    print("TEST 3: Direct Notion Page Schema Instantiation")
    print("=" * 60)
    
    # Minimal valid Notion Page content
    minimal_content = {
        "page_title": "API Rate Limiting Strategies",
        
        "properties": {
            "tags": ["api", "rate-limiting", "backend"],
            "status": "draft",
            "canonical_url": ""
        },
        
        "blocks": [
            {"type": "heading_1", "text": "API Rate Limiting Strategies"},
            {"type": "paragraph", "text": "Rate limiting protects APIs from abuse and ensures fair resource allocation. This guide covers implementation strategies for intermediate developers building production APIs."},
            {"type": "table_of_contents", "text": ""},
            
            {"type": "heading_2", "text": "Background"},
            {"type": "bulleted_list_item", "text": "Rate Limiting — Controlling the number of requests per time window"},
            {"type": "bulleted_list_item", "text": "Token Bucket — Algorithm allowing burst traffic within limits"},
            
            {"type": "heading_2", "text": "Implementation"},
            {"type": "paragraph", "text": "Token bucket algorithm provides flexible rate limiting with burst capacity."},
            {"type": "code", "language": "python", "text": "import time\nfrom collections import defaultdict\n\nclass TokenBucket:\n    def __init__(self, capacity, refill_rate):\n        self.capacity = capacity\n        self.tokens = capacity\n        self.refill_rate = refill_rate\n        self.last_refill = time.time()\n    \n    def consume(self, tokens=1):\n        self._refill()\n        if self.tokens >= tokens:\n            self.tokens -= tokens\n            return True\n        return False\n    \n    def _refill(self):\n        now = time.time()\n        tokens_to_add = (now - self.last_refill) * self.refill_rate\n        self.tokens = min(self.capacity, self.tokens + tokens_to_add)\n        self.last_refill = now"},
            
            {"type": "toggle", "text": "Advanced rate limiting patterns", "children": [
                {"type": "paragraph", "text": "Production systems often combine multiple strategies: per-user limits, endpoint-specific limits, and global throttling."},
                {"type": "bulleted_list_item", "text": "Sliding window — More accurate but memory intensive"},
                {"type": "bulleted_list_item", "text": "Distributed limiting — Using Redis for multi-instance coordination"}
            ]},
            
            {"type": "callout", "emoji": "⚠️", "text": "Warning: Always return meaningful error messages with rate limit headers (X-RateLimit-Remaining, X-RateLimit-Reset)."},
            
            {"type": "heading_2", "text": "Architecture"},
            {"type": "code", "language": "mermaid", "text": "flowchart LR\n    Client-->Middleware[Rate Limit Middleware]\n    Middleware-->|Allow|API[API Endpoint]\n    Middleware-->|Block|Error[429 Too Many Requests]\n    Middleware-->Redis[(Redis Cache)]"},
            {"type": "quote", "text": "Good rate limiting is invisible to normal users but essential for system stability."},
            
            {"type": "heading_2", "text": "Resources"},
            {"type": "bulleted_list_item", "text": "RFC 6585 — HTTP Status Code 429"},
            {"type": "bulleted_list_item", "text": "Redis Rate Limiting — https://redis.io/commands/incr"},
            
            {"type": "heading_2", "text": "Next steps"},
            {"type": "numbered_list_item", "text": "Implement token bucket rate limiter"},
            {"type": "numbered_list_item", "text": "Add rate limit headers to responses"},
            {"type": "numbered_list_item", "text": "Monitor rate limit hit rates"}
        ],
        
        "column_layout": {
            "enabled": True,
            "column_list": [
                {
                    "ratio": 0.5,
                    "children": [
                        {"type": "callout", "emoji": "🧪", "text": "Test idea: Benchmark different rate limiting algorithms under load to compare memory usage and accuracy."}
                    ]
                },
                {
                    "ratio": 0.5,
                    "children": [
                        {"type": "code", "language": "bash", "text": "# Load test rate limiter\nab -n 1000 -c 10 http://localhost:8000/api/endpoint\n# Check 429 responses"}
                    ]
                }
            ]
        },
        
        "database_inline": {
            "enabled": True,
            "name": "Rate Limiting Resources",
            "schema": [
                {"name": "Title", "type": "title"},
                {"name": "Type", "type": "select", "options": ["doc", "tool", "library"]},
                {"name": "Link", "type": "url"},
                {"name": "Status", "type": "select", "options": ["to read", "done"]},
                {"name": "Tags", "type": "multi_select", "options": []},
                {"name": "Added", "type": "date"}
            ],
            "initial_rows": [
                {
                    "Title": "RFC 6585 - HTTP 429",
                    "Type": "doc",
                    "Link": "https://tools.ietf.org/html/rfc6585",
                    "Status": "done",
                    "Tags": [],
                    "Added": ""
                }
            ]
        },
        
        "embeds": [
            {"type": "bookmark", "url": "https://tools.ietf.org/html/rfc6585"},
            {"type": "github_gist", "url": ""},
            {"type": "youtube", "url": ""}
        ],
        
        "image_prompts": [
            {
                "role": "cover",
                "title": "Notion Cover",
                "prompt": "Wide, minimalist cover for API Rate Limiting Strategies: subtle abstract tech pattern with light geometric lines representing API request flows; off-white background; faint grid; orange accent color; generous margins; flat vector aesthetic; composition leaves negative space for overlay title in Notion.",
                "negative_prompt": "no stock-photo people, no logos, no neon, no 3D bevels, no glossy gradients, no clutter",
                "style_notes": "editorial-tech; calm contrast; crisp kerning potential",
                "ratio": "1.91:1",
                "size_px": "1200x630",
                "alt_text": "Subtle abstract tech pattern cover with API flow lines"
            }
        ],
        
        "compliance": {
            "has_h1": True,
            "h2_sections_count": 5,
            "has_toc": True,
            "toggle_blocks_count": 1,
            "callout_blocks_count": 2,
            "code_blocks_count": 2,
            "embed_count": 1,
            "database_enabled": True,
            "image_prompt_count": 1,
            "has_tracked_bookmark_once": False,
            "checks": [
                "H1 equals topic_title",
                "TOC placed after intro",
                "5 H2 sections present",
                "1 toggle with children",
                "2 callouts (warning + test idea)",
                "2 code blocks (Python implementation + mermaid)",
                "1 bookmark embed (no tracked link - no primary_url)",
                "Database inline enabled with schema + 1 sample row",
                "1 cover image prompt"
            ]
        }
    }
    
    try:
        notion_page = NotionPageContent(**minimal_content)
        print("✅ Direct schema instantiation successful")
        print(f"📊 Notion Page structure:")
        print(f"   • Page title: {len(notion_page.page_title)} characters")
        print(f"   • Properties: {len(notion_page.properties)} fields")
        print(f"   • Blocks: {len(notion_page.blocks)} total")
        print(f"   • H2 sections: {notion_page.compliance['h2_sections_count']}")
        print(f"   • Toggle blocks: {notion_page.compliance['toggle_blocks_count']}")
        print(f"   • Callout blocks: {notion_page.compliance['callout_blocks_count']}")
        print(f"   • Code blocks: {notion_page.compliance['code_blocks_count']}")
        print(f"   • Database enabled: {notion_page.database_inline['enabled']}")
        
        # Test JSON serialization
        json_data = notion_page.model_dump()
        json_str = json.dumps(json_data, indent=2)
        print("✅ JSON serialization successful")
        print(f"📄 JSON size: {len(json_str)} characters")
        
        return True
        
    except Exception as e:
        print(f"❌ Direct schema instantiation failed: {e}")
        return False

def main():
    """Run all Notion Page tests"""
    print("🧪 NOTION PAGE CONTENT GENERATION TESTS")
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
    
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)
    
    print(f"\n🎯 Overall: {passed_count}/{total_count} tests passed")
    
    if passed_count == total_count:
        print("🎉 All Notion Page tests passed! Ready for integration.")
        return True
    else:
        print("⚠️ Some tests failed. Check implementation.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
