#!/usr/bin/env python3
"""
Simple test script for Medium Article content generation.
Tests prompt processing, schema validation, and direct schema instantiation.
"""

import sys
import os
import json
from pathlib import Path

# Add the app directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from prompt_processor import PromptProcessor
from schemas import MediumArticleContent, validate_content

def test_prompt_processing():
    """Test Medium Article prompt template processing"""
    print("=" * 60)
    print("TEST 1: Medium Article Prompt Processing")
    print("=" * 60)
    
    try:
        processor = PromptProcessor()
        
        # Test data
        topic_id = "2001"
        topic_name = "Microservices Communication Patterns"
        topic_description = "Deep dive into synchronous and asynchronous communication patterns between microservices, including REST APIs, message queues, event streaming, and service mesh architectures for building resilient distributed systems."
        
        # Process the prompt template
        prompt_path = "prompts/bodies/medium-article.txt"
        processed_prompt = processor.process_prompt_template(
            template_path=prompt_path,
            topic_id=topic_id,
            topic_name=topic_name,
            topic_description=topic_description,
            platform="medium",
            format_type="article"
        )
        
        print(f"✅ Prompt template processed successfully")
        print(f"📄 Template path: {prompt_path}")
        print(f"🎯 Topic: {topic_name}")
        print(f"📝 Processed prompt length: {len(processed_prompt)} characters")
        print(f"🔍 Contains topic name: {'✅' if topic_name in processed_prompt else '❌'}")
        print(f"🔍 Contains JSON format: {'✅' if 'markdown' in processed_prompt else '❌'}")
        print(f"🔍 Contains diagram blocks: {'✅' if 'diagram_blocks' in processed_prompt else '❌'}")
        print(f"🔍 Contains SEO structure: {'✅' if 'meta_title' in processed_prompt else '❌'}")
        
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
    """Test Medium Article schema validation with sample data"""
    print("\n" + "=" * 60)
    print("TEST 2: Medium Article Schema Validation")
    print("=" * 60)
    
    # Sample Medium Article content matching the schema
    sample_content = {
        "title": "Microservices Communication: The Complete Guide",
        "subtitle": "Master synchronous and asynchronous patterns for resilient distributed systems",
        "reading_time_min": 6,
        "tags": ["Microservices", "System Design", "Distributed Systems", "Architecture", "Backend Engineering"],
        "markdown": """# Microservices Communication: The Complete Guide

> _Master synchronous and asynchronous patterns for resilient distributed systems_

Building microservices is like orchestrating a symphony. Each service plays its part, but the magic happens in how they communicate. After architecting distributed systems for Fortune 500 companies, I've learned that communication patterns make or break your microservices architecture.

In this guide, we'll explore the essential patterns that power systems like Netflix, Uber, and Amazon. You'll learn when to use each approach and avoid the pitfalls that cost companies millions.

## Synchronous Communication — When Services Talk Directly

The most intuitive approach: Service A calls Service B and waits for a response.

### REST APIs: The Foundation
```javascript
// Order Service calling Inventory Service
const checkInventory = async (productId, quantity) => {
  const response = await fetch(`${INVENTORY_SERVICE}/check`, {
    method: 'POST',
    body: JSON.stringify({ productId, quantity })
  });
  return response.json();
};
```

**Pros:**
- Simple to understand and debug
- Immediate consistency
- Easy error handling

**Cons:**
- Tight coupling between services
- Cascading failures
- Higher latency

### GraphQL Federation
```graphql
# User service schema
type User {
  id: ID!
  name: String!
  orders: [Order!]! # Resolved by Order service
}
```

## Asynchronous Communication — Decoupled and Resilient

Services communicate through intermediaries without waiting for responses.

### Message Queues: Reliable Delivery

| Pattern | Use Case | Example |
|---------|----------|---------|
| Point-to-Point | Task processing | Order → Payment Queue |
| Publish-Subscribe | Event broadcasting | User Created → Multiple Subscribers |

```python
# Producer
import pika

def publish_order_event(order_data):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    
    channel.queue_declare(queue='order_processing')
    channel.basic_publish(
        exchange='',
        routing_key='order_processing',
        body=json.dumps(order_data)
    )
    connection.close()
```

> "Asynchronous communication is not just about performance—it's about building systems that can evolve independently."

```mermaid
flowchart TD
    A[Order Service] -->|Publishes| B[Message Broker]
    B -->|Consumes| C[Payment Service]
    B -->|Consumes| D[Inventory Service]
    B -->|Consumes| E[Notification Service]
    
    C -->|Updates| F[Payment DB]
    D -->|Updates| G[Inventory DB]
    E -->|Sends| H[Email/SMS]
```

## Event Streaming — Real-time Data Flow

Apache Kafka and similar platforms enable continuous data streams.

### Event Sourcing Pattern
```sql
-- Event Store Table
CREATE TABLE events (
    id UUID PRIMARY KEY,
    aggregate_id UUID,
    event_type VARCHAR(100),
    event_data JSONB,
    version INTEGER,
    created_at TIMESTAMP
);
```

**Benefits:**
- Complete audit trail
- Time-travel debugging
- Multiple read models

## Service Mesh — Infrastructure-level Communication

Istio, Linkerd, and Consul Connect handle communication concerns at the infrastructure layer.

### Traffic Management
```yaml
# Istio VirtualService
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: user-service
spec:
  http:
  - match:
    - headers:
        canary:
          exact: "true"
    route:
    - destination:
        host: user-service
        subset: v2
      weight: 100
  - route:
    - destination:
        host: user-service
        subset: v1
      weight: 100
```

## Choosing the Right Pattern

**Use Synchronous when:**
- You need immediate consistency
- Simple request-response workflows
- Low-latency requirements

**Use Asynchronous when:**
- High throughput needed
- Services can work independently
- Fault tolerance is critical

**Use Event Streaming when:**
- Real-time analytics required
- Complex event processing
- Multiple downstream consumers

## Conclusion — Building Communication That Scales

The best microservices architectures combine multiple patterns strategically. Start with synchronous communication for simplicity, then introduce asynchronous patterns as your system grows.

Remember: communication patterns are not just technical decisions—they shape your team structure, deployment processes, and system evolution.

[Get the complete microservices communication playbook](https://systemdesign.com/microservices-communication?utm_source=medium&utm_medium=article)""",
        "sections": [
            {
                "h2": "Synchronous Communication — When Services Talk Directly",
                "summary": "Direct service-to-service calls with immediate responses using REST APIs and GraphQL",
                "key_points": ["REST API foundations", "GraphQL federation patterns", "Immediate consistency benefits"]
            },
            {
                "h2": "Asynchronous Communication — Decoupled and Resilient", 
                "summary": "Message queues and event-driven patterns for fault-tolerant distributed systems",
                "key_points": ["Message queue patterns", "Publish-subscribe models", "Decoupling benefits"]
            },
            {
                "h2": "Event Streaming — Real-time Data Flow",
                "summary": "Continuous data streams using Kafka and event sourcing for real-time processing",
                "key_points": ["Apache Kafka patterns", "Event sourcing implementation", "Real-time analytics"]
            },
            {
                "h2": "Service Mesh — Infrastructure-level Communication",
                "summary": "Istio and Linkerd for handling cross-cutting communication concerns at infrastructure layer",
                "key_points": ["Traffic management", "Security policies", "Observability features"]
            },
            {
                "h2": "Choosing the Right Pattern",
                "summary": "Decision framework for selecting appropriate communication patterns based on requirements",
                "key_points": ["Synchronous use cases", "Asynchronous benefits", "Event streaming scenarios"]
            }
        ],
        "code_snippets": [
            {
                "language": "javascript",
                "label": "REST API call example",
                "content": "```javascript\nconst checkInventory = async (productId, quantity) => {\n  const response = await fetch(`${INVENTORY_SERVICE}/check`, {\n    method: 'POST',\n    body: JSON.stringify({ productId, quantity })\n  });\n  return response.json();\n};\n```"
            },
            {
                "language": "python", 
                "label": "Message queue producer",
                "content": "```python\nimport pika\n\ndef publish_order_event(order_data):\n    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))\n    channel = connection.channel()\n    \n    channel.queue_declare(queue='order_processing')\n    channel.basic_publish(\n        exchange='',\n        routing_key='order_processing',\n        body=json.dumps(order_data)\n    )\n    connection.close()\n```"
            },
            {
                "language": "yaml",
                "label": "Istio traffic management",
                "content": "```yaml\napiVersion: networking.istio.io/v1alpha3\nkind: VirtualService\nmetadata:\n  name: user-service\nspec:\n  http:\n  - match:\n    - headers:\n        canary:\n          exact: \"true\"\n    route:\n    - destination:\n        host: user-service\n        subset: v2\n      weight: 100\n```"
            }
        ],
        "diagram_blocks": [
            {
                "id": "d1",
                "type": "mermaid",
                "alt": "Asynchronous communication flow with message broker",
                "content": "flowchart TD\n    A[Order Service] -->|Publishes| B[Message Broker]\n    B -->|Consumes| C[Payment Service]\n    B -->|Consumes| D[Inventory Service]\n    B -->|Consumes| E[Notification Service]\n    \n    C -->|Updates| F[Payment DB]\n    D -->|Updates| G[Inventory DB]\n    E -->|Sends| H[Email/SMS]",
                "placement_hint": "after Section 2"
            }
        ],
        "pull_quotes": [
            "Asynchronous communication is not just about performance—it's about building systems that can evolve independently."
        ],
        "cta": {
            "text": "If this helped, clap 👏 and follow for more system design deep dives.",
            "link": "https://systemdesign.com/microservices-communication?utm_source=medium&utm_medium=article"
        },
        "references": [
            {
                "title": "Building Microservices - Sam Newman",
                "url": "https://www.oreilly.com/library/view/building-microservices/9781491950340/",
                "note": "Comprehensive guide to microservices architecture patterns"
            },
            {
                "title": "Apache Kafka Documentation",
                "url": "https://kafka.apache.org/documentation/",
                "note": "Official documentation for event streaming platform"
            },
            {
                "title": "Istio Service Mesh",
                "url": "https://istio.io/latest/docs/",
                "note": "Service mesh platform for microservices communication"
            }
        ],
        "image_prompts": [
            {
                "role": "cover",
                "title": "Medium Cover",
                "prompt": "Widescreen minimal cover for Microservices Communication Patterns: bold headline 'Service Communication' + small network diagram glyph showing connected nodes; off-white background; thin vector strokes; subtle dotted grid; blue accent color; generous margins; flat vector; desktop & mobile legible.",
                "negative_prompt": "no stock-photo people, no logos, no neon, no 3D bevels, no glossy gradients, no clutter",
                "style_notes": "editorial poster tone; crisp kerning; consistent stroke widths",
                "ratio": "1.91:1",
                "size_px": "1200x630",
                "alt_text": "Widescreen minimal cover with service communication headline and network diagram glyph"
            }
        ],
        "seo": {
            "slug": "microservices-communication-patterns-complete-guide",
            "meta_title": "Microservices Communication: The Complete Guide",
            "meta_description": "Master synchronous and asynchronous communication patterns for microservices. Learn REST APIs, message queues, event streaming, and service mesh with real examples.",
            "keywords_used": ["microservices", "communication patterns", "distributed systems", "REST API", "message queues"],
            "lsi_terms_used": ["service mesh", "event streaming", "asynchronous", "synchronous", "system architecture"]
        },
        "compliance": {
            "word_count": 1247,
            "title_char_count": 47,
            "subtitle_char_count": 78,
            "tags_count": 5,
            "sections_count": 5,
            "code_snippets_count": 3,
            "diagram_blocks_count": 1,
            "image_prompt_count": 1,
            "has_tracked_link": True,
            "checks": [
                "800–1500 words",
                "title ≤60 chars; subtitle ≤120",
                "3–5 H2 sections (≤7 if length_hint high)",
                "≥1 diagram block (mermaid/ascii) with alt text",
                "1–3 code snippets when relevant",
                "5–7 Medium tags",
                "exactly one tracked link if primary_url present",
                "image_prompts length == image_plan.count (default 1)"
            ]
        }
    }
    
    try:
        # Test direct schema validation
        print("🧪 Testing direct schema validation...")
        medium_article_content = MediumArticleContent(**sample_content)
        print(f"✅ Direct schema validation passed")
        print(f"📊 Title length: {len(medium_article_content.title)} chars")
        print(f"📝 Word count: {medium_article_content.compliance['word_count']} words")
        print(f"🏷️ Tags count: {len(medium_article_content.tags)}")
        print(f"📑 Sections count: {len(medium_article_content.sections)}")
        print(f"💻 Code snippets: {len(medium_article_content.code_snippets)}")
        print(f"📊 Diagram blocks: {len(medium_article_content.diagram_blocks)}")
        print(f"🖼️ Image prompts: {len(medium_article_content.image_prompts)}")
        
        # Test schema validator function
        print(f"\n🧪 Testing schema validator function...")
        validated_content = validate_content('medium', 'article', sample_content)
        print(f"✅ Schema validator function passed")
        print(f"📋 Validated content type: {type(validated_content).__name__}")
        
        # Display sample content structure
        print(f"\n📋 Sample Medium Article Structure:")
        print(f"   • Title: {len(sample_content['title'])} characters")
        print(f"   • Subtitle: {len(sample_content['subtitle'])} characters")
        print(f"   • Reading time: {sample_content['reading_time_min']} minutes")
        print(f"   • Sections: {len(sample_content['sections'])} H2 sections")
        print(f"   • Code examples: {len(sample_content['code_snippets'])} snippets")
        print(f"   • Diagrams: {len(sample_content['diagram_blocks'])} blocks")
        print(f"   • References: {len(sample_content['references'])} sources")
        
        return True
        
    except Exception as e:
        print(f"❌ Schema validation failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_direct_schema_instantiation():
    """Test direct instantiation of Medium Article schema"""
    print("\n" + "=" * 60)
    print("TEST 3: Direct Medium Article Schema Instantiation")
    print("=" * 60)
    
    try:
        # Create Medium Article content directly
        medium_article_content = MediumArticleContent(
            title="Database Indexing Strategies That Actually Work",
            subtitle="Boost query performance by 10x with the right indexing approach",
            reading_time_min=5,
            tags=["Database", "Performance", "SQL", "Indexing", "Backend"],
            markdown="""# Database Indexing Strategies That Actually Work

> _Boost query performance by 10x with the right indexing approach_

Slow database queries are the silent killer of application performance. I've seen startups crash under load because they ignored indexing until it was too late.

After optimizing databases for companies processing billions of records, here's what I've learned about indexing strategies that actually work in production.

## B-Tree Indexes — The Workhorse

Most databases use B-Tree indexes by default. They're perfect for equality and range queries.

```sql
-- Create a B-Tree index
CREATE INDEX idx_user_email ON users(email);

-- Optimizes queries like:
SELECT * FROM users WHERE email = 'john@example.com';
SELECT * FROM users WHERE created_at BETWEEN '2023-01-01' AND '2023-12-31';
```

**When to use:**
- Equality searches (=)
- Range queries (<, >, BETWEEN)
- ORDER BY operations

## Hash Indexes — Lightning Fast Equality

Hash indexes excel at exact matches but can't handle ranges.

```sql
-- PostgreSQL hash index
CREATE INDEX idx_user_id_hash ON users USING HASH(id);
```

| Index Type | Equality | Range | Memory |
|------------|----------|-------|---------|
| B-Tree | Good | Excellent | Medium |
| Hash | Excellent | No | Low |

## Composite Indexes — Order Matters

Multiple columns in a single index. Column order is crucial.

```sql
-- Good for: WHERE status = 'active' AND created_at > '2023-01-01'
CREATE INDEX idx_status_created ON orders(status, created_at);

-- Bad for: WHERE created_at > '2023-01-01' AND status = 'active'
-- (Can't use the index efficiently)
```

> "The leftmost prefix rule: composite indexes work left-to-right, never right-to-left."

```mermaid
graph TD
    A[Query: status + created_at] --> B{Index: status, created_at}
    B -->|✅ Can use| C[Fast lookup]
    
    D[Query: created_at only] --> B
    B -->|❌ Can't use efficiently| E[Slow scan]
```

## Partial Indexes — Smart Filtering

Index only the rows you actually query.

```sql
-- Only index active users
CREATE INDEX idx_active_users ON users(email) WHERE status = 'active';
```

**Benefits:**
- Smaller index size
- Faster updates
- Reduced storage

## Covering Indexes — Include Everything

Include non-key columns to avoid table lookups.

```sql
-- Covers the entire query
CREATE INDEX idx_user_profile ON users(email) INCLUDE (name, created_at);

-- This query never touches the main table
SELECT name, created_at FROM users WHERE email = 'john@example.com';
```

## Conclusion — Index Like a Pro

Start with single-column B-Tree indexes on frequently queried columns. Add composite indexes for multi-column WHERE clauses. Use partial indexes for filtered queries.

Remember: every index speeds up reads but slows down writes. Find the balance that works for your workload.

[Get the complete database optimization guide](https://systemdesign.com/database-indexing?utm_source=medium&utm_medium=article)""",
            sections=[
                {
                    "h2": "B-Tree Indexes — The Workhorse",
                    "summary": "Default index type perfect for equality and range queries with excellent versatility",
                    "key_points": ["Equality searches", "Range queries", "ORDER BY optimization"]
                },
                {
                    "h2": "Hash Indexes — Lightning Fast Equality",
                    "summary": "Specialized indexes for exact matches with minimal memory overhead",
                    "key_points": ["Perfect equality performance", "No range support", "Low memory usage"]
                },
                {
                    "h2": "Composite Indexes — Order Matters",
                    "summary": "Multi-column indexes where column order determines query optimization effectiveness",
                    "key_points": ["Leftmost prefix rule", "Column order importance", "Multi-condition queries"]
                },
                {
                    "h2": "Partial Indexes — Smart Filtering",
                    "summary": "Conditional indexes that only include relevant rows to reduce size and improve performance",
                    "key_points": ["Filtered indexing", "Reduced storage", "Faster updates"]
                },
                {
                    "h2": "Covering Indexes — Include Everything",
                    "summary": "Indexes that include all query columns to eliminate table lookups entirely",
                    "key_points": ["Include non-key columns", "Avoid table access", "Query optimization"]
                }
            ],
            code_snippets=[
                {
                    "language": "sql",
                    "label": "B-Tree index creation",
                    "content": "```sql\nCREATE INDEX idx_user_email ON users(email);\n\nSELECT * FROM users WHERE email = 'john@example.com';\n```"
                },
                {
                    "language": "sql",
                    "label": "Composite index example",
                    "content": "```sql\nCREATE INDEX idx_status_created ON orders(status, created_at);\n```"
                }
            ],
            diagram_blocks=[
                {
                    "id": "d1",
                    "type": "mermaid",
                    "alt": "Composite index usage pattern showing leftmost prefix rule",
                    "content": "graph TD\n    A[Query: status + created_at] --> B{Index: status, created_at}\n    B -->|✅ Can use| C[Fast lookup]\n    \n    D[Query: created_at only] --> B\n    B -->|❌ Can't use efficiently| E[Slow scan]",
                    "placement_hint": "after Section 3"
                }
            ],
            pull_quotes=[
                "The leftmost prefix rule: composite indexes work left-to-right, never right-to-left."
            ],
            cta={
                "text": "If this helped, clap 👏 and follow for more database optimization tips.",
                "link": "https://systemdesign.com/database-indexing?utm_source=medium&utm_medium=article"
            },
            references=[
                {
                    "title": "PostgreSQL Index Documentation",
                    "url": "https://www.postgresql.org/docs/current/indexes.html",
                    "note": "Official PostgreSQL indexing guide"
                }
            ],
            image_prompts=[
                {
                    "role": "cover",
                    "title": "Medium Cover",
                    "prompt": "Widescreen minimal cover for Database Indexing Strategies: bold headline 'Index Strategies' + small database table diagram glyph; off-white background; thin vector strokes; subtle dotted grid; green accent color; generous margins; flat vector; desktop & mobile legible.",
                    "negative_prompt": "no stock-photo people, no logos, no neon, no 3D bevels, no glossy gradients, no clutter",
                    "style_notes": "editorial poster tone; crisp kerning; consistent stroke widths",
                    "ratio": "1.91:1",
                    "size_px": "1200x630",
                    "alt_text": "Widescreen minimal cover with database indexing headline and table diagram glyph"
                }
            ],
            seo={
                "slug": "database-indexing-strategies-that-actually-work",
                "meta_title": "Database Indexing Strategies That Actually Work",
                "meta_description": "Learn B-Tree, Hash, Composite, Partial, and Covering indexes to boost database query performance by 10x with real SQL examples.",
                "keywords_used": ["database indexing", "query performance", "SQL optimization", "B-Tree index", "composite index"],
                "lsi_terms_used": ["database performance", "query optimization", "index strategies", "SQL tuning", "database design"]
            },
            compliance={
                "word_count": 892,
                "title_char_count": 49,
                "subtitle_char_count": 59,
                "tags_count": 5,
                "sections_count": 5,
                "code_snippets_count": 2,
                "diagram_blocks_count": 1,
                "image_prompt_count": 1,
                "has_tracked_link": True,
                "checks": [
                    "800–1500 words",
                    "title ≤60 chars; subtitle ≤120",
                    "3–5 H2 sections (≤7 if length_hint high)",
                    "≥1 diagram block (mermaid/ascii) with alt text",
                    "1–3 code snippets when relevant",
                    "5–7 Medium tags",
                    "exactly one tracked link if primary_url present",
                    "image_prompts length == image_plan.count (default 1)"
                ]
            }
        )
        
        print(f"✅ Direct schema instantiation successful")
        print(f"📊 Medium Article structure:")
        print(f"   • Title: {len(medium_article_content.title)} characters")
        print(f"   • Subtitle: {len(medium_article_content.subtitle)} characters")
        print(f"   • Reading time: {medium_article_content.reading_time_min} minutes")
        print(f"   • Tags: {len(medium_article_content.tags)}")
        print(f"   • Sections: {len(medium_article_content.sections)}")
        print(f"   • Code snippets: {len(medium_article_content.code_snippets)}")
        print(f"   • Diagram blocks: {len(medium_article_content.diagram_blocks)}")
        print(f"   • Word count: {medium_article_content.compliance['word_count']}")
        
        # Test JSON serialization
        json_output = medium_article_content.model_dump()
        print(f"✅ JSON serialization successful")
        print(f"📄 JSON size: {len(json.dumps(json_output))} characters")
        
        return True
        
    except Exception as e:
        print(f"❌ Direct schema instantiation failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all Medium Article tests"""
    print("🧪 MEDIUM ARTICLE CONTENT GENERATION TESTS")
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
        print("🎉 All Medium Article tests passed! Ready for integration.")
    else:
        print("⚠️ Some tests failed. Please review the errors above.")
    
    return passed == len(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)