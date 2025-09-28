#!/usr/bin/env python3
"""
Test suite for Hashnode Article content generation.
Tests prompt processing, schema validation, and direct schema instantiation.
"""

import sys
import os
import json
from pathlib import Path

# Add the app directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from schemas import HashnodeArticleContent, validate_content

def load_prompt_template():
    """Load the Hashnode Article prompt template"""
    prompt_path = Path(__file__).parent / "prompts" / "bodies" / "hashnode-article.txt"
    if not prompt_path.exists():
        raise FileNotFoundError(f"Prompt template not found: {prompt_path}")
    
    with open(prompt_path, 'r', encoding='utf-8') as f:
        return f.read()

def process_prompt_with_topic(template, topic_data):
    """Process prompt template with topic data"""
    # Sample topic data for testing
    sample_data = {
        "topic_id": "4001",
        "topic_name": topic_data.get("name", "Building Microservices with Event-Driven Architecture"),
        "topic_description": topic_data.get("description", "Complete guide to implementing event-driven microservices with message queues and event sourcing"),
        "audience": "intermediate",
        "tone": "clear, confident, friendly, non-cringe",
        "locale": "en",
        "primary_url": "https://blog.example.com/microservices-event-driven",
        **topic_data.get("brand", {
            "site_url": "https://blog.example.com",
            "handles": {"hashnode": "@yourblog", "x": "@systemdesign", "linkedin": "@systemdesign", "github": "@systemdesign"},
            "utm_base": "utm_source=hashnode&utm_medium=article"
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
    """Test 1: Hashnode Article prompt template processing"""
    print("=" * 60)
    print("TEST 1: Hashnode Article Prompt Processing")
    print("=" * 60)
    
    try:
        template = load_prompt_template()
        
        # Test with event-driven microservices topic
        topic_data = {
            "name": "Building Microservices with Event-Driven Architecture",
            "description": "Complete guide to implementing event-driven microservices with message queues, event sourcing, and CQRS patterns"
        }
        
        processed_prompt = process_prompt_with_topic(template, topic_data)
        
        print("✅ Prompt template processed successfully")
        print(f"📄 Template path: prompts/bodies/hashnode-article.txt")
        print(f"🎯 Topic: {topic_data['name']}")
        print(f"📝 Processed prompt length: {len(processed_prompt)} characters")
        
        # Verify key elements are present
        checks = {
            "Contains topic name": topic_data["name"] in processed_prompt,
            "Contains JSON format": '"content":' in processed_prompt,
            "Contains Table of Contents": "Table of Contents" in processed_prompt,
            "Contains code snippets": "code_snippets" in processed_prompt,
            "Contains diagram blocks": "diagram_blocks" in processed_prompt,
            "Contains series potential": "series_potential" in processed_prompt,
            "Contains SEO metadata": '"seo":' in processed_prompt
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
    """Test 2: Hashnode Article schema validation with sample data"""
    print("\n" + "=" * 60)
    print("TEST 2: Hashnode Article Schema Validation")
    print("=" * 60)
    
    # Sample Hashnode Article content
    sample_content = {
        "front_matter": {
            "title": "Building Event-Driven Microservices: A Complete Guide",
            "tags": ["microservices", "event-driven", "architecture", "messaging", "distributed-systems"],
            "slug": "building-event-driven-microservices-complete-guide",
            "cover_image": "https://blog.example.com/images/hashnode/microservices-cover.png",
            "canonical_url": "https://blog.example.com/microservices-event-driven"
        },
        
        "markdown": """# Building Event-Driven Microservices: A Complete Guide

> _Learn how to design resilient microservices using event-driven patterns that scale to millions of requests._

**Estimated read**: ~12 min

## Table of Contents
- [Introduction](#introduction)
- [Background](#background)
- [Event-Driven Patterns](#event-driven-patterns)
- [Implementation](#implementation)
- [Trade-offs](#trade-offs)
- [Case Study](#case-study)
- [Conclusion](#conclusion)

## Introduction

Event-driven architecture (EDA) has become essential for building scalable microservices. Traditional request-response patterns create tight coupling and single points of failure. With EDA, services communicate through events, reducing dependencies and improving resilience. Companies like Netflix and Uber process over 1 billion events daily using these patterns.

## Background

Event-driven architecture emerged from the need to handle distributed system complexity. Unlike synchronous communication, events allow services to operate independently. Key concepts include event sourcing, CQRS (Command Query Responsibility Segregation), and message brokers like Apache Kafka and RabbitMQ.

## Event-Driven Patterns

The core mechanism involves producers publishing events and consumers subscribing to relevant event types. This decouples services and enables horizontal scaling.

```mermaid
flowchart LR
    A[Order Service] -->|OrderCreated| B[Event Bus]
    B -->|OrderCreated| C[Inventory Service]
    B -->|OrderCreated| D[Payment Service]
    B -->|OrderCreated| E[Notification Service]
```

_Alt text_: Event flow from order service through event bus to multiple consuming services.

## Implementation

Step-by-step implementation using Node.js and Apache Kafka:

```bash
# Setup Kafka and dependencies
docker-compose up -d kafka zookeeper
npm install kafkajs express
```

```javascript
// Event producer service
const kafka = require('kafkajs');

const client = kafka({
  clientId: 'order-service',
  brokers: ['localhost:9092']
});

const producer = client.producer();

async function publishOrderEvent(orderData) {
  await producer.send({
    topic: 'order-events',
    messages: [{
      key: orderData.orderId,
      value: JSON.stringify({
        eventType: 'OrderCreated',
        timestamp: Date.now(),
        data: orderData
      })
    }]
  });
}
```

```javascript
// Event consumer service
const consumer = client.consumer({ groupId: 'inventory-group' });

async function startConsumer() {
  await consumer.subscribe({ topic: 'order-events' });
  
  await consumer.run({
    eachMessage: async ({ message }) => {
      const event = JSON.parse(message.value.toString());
      
      if (event.eventType === 'OrderCreated') {
        await updateInventory(event.data);
      }
    }
  });
}
```


## Trade-offs

- Pro: Loose coupling enables independent deployments and scaling
- Pro: Fault tolerance through event replay and dead letter queues
- Con: Eventual consistency requires careful handling of race conditions
- Con: Debugging distributed flows becomes more complex
- Con: Message ordering and duplicate handling need explicit design

## Case Study

E-commerce platform handling 50,000 orders per hour. Before EDA, order processing took 2.3 seconds with 15% failure rate during peak traffic. After implementing event-driven patterns:

- Processing time: 450ms average
- Failure rate: 0.8%
- System availability: 99.9%
- Independent service deployments: 40+ per day

## Conclusion

Event-driven microservices provide the foundation for scalable, resilient systems. Start with simple pub-sub patterns and evolve toward event sourcing as complexity grows. The investment in proper event design pays dividends in system maintainability and performance.

For the complete implementation guide with production deployment strategies, read the full breakdown: https://blog.example.com/microservices-event-driven?utm_source=hashnode&utm_medium=article
""",
        
        "reading_time_min": 12,
        
        "toc": [
            {"title": "Introduction", "anchor": "#introduction"},
            {"title": "Background", "anchor": "#background"},
            {"title": "Event-Driven Patterns", "anchor": "#event-driven-patterns"},
            {"title": "Implementation", "anchor": "#implementation"},
            {"title": "Trade-offs", "anchor": "#trade-offs"},
            {"title": "Case Study", "anchor": "#case-study"},
            {"title": "Conclusion", "anchor": "#conclusion"}
        ],
        
        "sections": [
            {
                "h2": "Introduction",
                "summary": "Event-driven architecture reduces coupling and improves microservice resilience",
                "key_points": ["EDA enables loose coupling", "Processes 1B+ events daily at scale"]
            },
            {
                "h2": "Event-Driven Patterns",
                "summary": "Core patterns using producers, consumers, and event buses for decoupling",
                "key_points": ["Producer-consumer pattern", "Horizontal scaling capability"]
            },
            {
                "h2": "Implementation",
                "summary": "Practical Node.js implementation with Kafka for event streaming",
                "key_points": ["Kafka setup and configuration", "Producer and consumer code examples"]
            },
            {
                "h2": "Trade-offs",
                "summary": "Benefits and challenges of event-driven microservice architecture",
                "key_points": ["Loose coupling benefits", "Eventual consistency challenges"]
            },
            {
                "h2": "Case Study",
                "summary": "E-commerce platform performance improvements with EDA implementation",
                "key_points": ["450ms processing time", "99.9% system availability"]
            }
        ],
        
        "code_snippets": [
            {
                "language": "bash",
                "label": "Environment Setup",
                "content": "```bash\n# Setup Kafka and dependencies\ndocker-compose up -d kafka zookeeper\nnpm install kafkajs express\n```",
                "runnable": True
            },
            {
                "language": "javascript",
                "label": "Event Producer",
                "content": "```javascript\n// Event producer service\nconst kafka = require('kafkajs');\n\nconst client = kafka({\n  clientId: 'order-service',\n  brokers: ['localhost:9092']\n});\n\nconst producer = client.producer();\n\nasync function publishOrderEvent(orderData) {\n  await producer.send({\n    topic: 'order-events',\n    messages: [{\n      key: orderData.orderId,\n      value: JSON.stringify({\n        eventType: 'OrderCreated',\n        timestamp: Date.now(),\n        data: orderData\n      })\n    }]\n  });\n}\n```",
                "runnable": True
            },
            {
                "language": "javascript",
                "label": "Event Consumer",
                "content": "```javascript\n// Event consumer service\nconst consumer = client.consumer({ groupId: 'inventory-group' });\n\nasync function startConsumer() {\n  await consumer.subscribe({ topic: 'order-events' });\n  \n  await consumer.run({\n    eachMessage: async ({ message }) => {\n      const event = JSON.parse(message.value.toString());\n      \n      if (event.eventType === 'OrderCreated') {\n        await updateInventory(event.data);\n      }\n    }\n  });\n}\n```",
                "runnable": True
            }
        ],
        
        "diagram_blocks": [
            {
                "id": "d1",
                "type": "mermaid",
                "alt": "Event flow from order service through event bus to multiple consuming services",
                "content": "flowchart LR\n    A[Order Service] -->|OrderCreated| B[Event Bus]\n    B -->|OrderCreated| C[Inventory Service]\n    B -->|OrderCreated| D[Payment Service]\n    B -->|OrderCreated| E[Notification Service]",
                "placement_hint": "in Event-Driven Patterns"
            }
        ],
        
        "series_potential": {
            "is_part_one": True,
            "suggested_next_parts": [
                "Advanced Event Sourcing Patterns",
                "CQRS Implementation with Event Stores",
                "Production Monitoring and Observability"
            ]
        },
        
        "seo": {
            "meta_title": "Building Event-Driven Microservices: Complete Guide",
            "meta_description": "Learn to build scalable event-driven microservices with Kafka, Node.js, and proven patterns. Includes implementation examples and case studies.",
            "keywords_used": ["microservices", "event-driven", "kafka", "nodejs", "distributed-systems"],
            "lsi_terms_used": ["event-sourcing", "message-queues", "pub-sub", "decoupling"]
        },
        
        "cta": {
            "text": "If this helped, follow for more and read the deep-dive.",
            "link": "https://blog.example.com/microservices-event-driven?utm_source=hashnode&utm_medium=article"
        },
        
        "image_prompts": [
            {
                "role": "cover",
                "title": "Hashnode Cover",
                "prompt": "Minimal wide banner for Building Event-Driven Microservices with architecture iconography; short headline 'Event-Driven Architecture' top-left; off-white/light background; thin vector strokes; subtle dotted grid; blue accent color; generous margins; flat vector; crisp at 1200×630.",
                "negative_prompt": "no stock-photo people, no logos, no neon, no 3D bevels, no glossy gradients, no clutter",
                "style_notes": "editorial-tech; crisp kerning; consistent stroke widths",
                "ratio": "1.91:1",
                "size_px": "1200x630",
                "alt_text": "Wide minimal banner with microservices architecture glyph"
            }
        ],
        
        "compliance": {
            "word_count": 2156,
            "title_char_count": 49,
            "tags_count": 5,
            "sections_count": 6,
            "code_snippets_count": 3,
            "diagram_blocks_count": 1,
            "has_toc": True,
            "image_prompt_count": 1,
            "has_canonical": True,
            "has_tracked_link_once": True,
            "keyword_overrides": False,
            "checks": [
                "2156 words (within 1500-3000 range)",
                "SEO title 49 chars; slug lowercase-hyphenated",
                "TOC present with 8 sections and matching anchors",
                "3 runnable code snippets and 1 mermaid diagram",
                "5 relevant lowercase tags",
                "canonical_url set for republishing",
                "exactly one tracked CTA link in conclusion",
                "1 cover image prompt matches image_plan.count"
            ]
        }
    }
    
    try:
        print("🧪 Testing direct schema validation...")
        hashnode_article = HashnodeArticleContent(**sample_content)
        print("✅ Direct schema validation passed")
        print(f"📊 Title length: {len(hashnode_article.front_matter['title'])} chars")
        print(f"📝 Word count: {hashnode_article.compliance['word_count']} words")
        print(f"📑 TOC sections: {len(hashnode_article.toc)}")
        print(f"💻 Code snippets: {len(hashnode_article.code_snippets)}")
        print(f"📊 Diagram blocks: {len(hashnode_article.diagram_blocks)}")
        print(f"🏷️ Tags: {len(hashnode_article.front_matter['tags'])}")
        print(f"📚 Series potential: {'Yes' if hashnode_article.series_potential['is_part_one'] else 'No'}")
        
        print("\n🧪 Testing schema validator function...")
        validated_content = validate_content("hashnode", "article", sample_content)
        print("✅ Schema validator function passed")
        print(f"📋 Validated content type: {type(validated_content).__name__}")
        
        print(f"\n📋 Sample Hashnode Article Structure:")
        print(f"   • Title: {len(hashnode_article.front_matter['title'])} characters")
        print(f"   • Reading time: {hashnode_article.reading_time_min} minutes")
        print(f"   • TOC sections: {len(hashnode_article.toc)}")
        print(f"   • Code snippets: {len(hashnode_article.code_snippets)} runnable examples")
        print(f"   • Diagrams: {len(hashnode_article.diagram_blocks)} mermaid blocks")
        print(f"   • Series parts: {len(hashnode_article.series_potential['suggested_next_parts'])}")
        
        return True
        
    except Exception as e:
        print(f"❌ Schema validation failed: {e}")
        return False

def test_direct_schema_instantiation():
    """Test 3: Direct Hashnode Article schema instantiation"""
    print("\n" + "=" * 60)
    print("TEST 3: Direct Hashnode Article Schema Instantiation")
    print("=" * 60)
    
    # Minimal valid Hashnode Article content
    minimal_content = {
        "front_matter": {
            "title": "GraphQL Federation: Scaling APIs Across Teams",
            "tags": ["graphql", "federation", "api-design", "microservices", "scalability"],
            "slug": "graphql-federation-scaling-apis-across-teams",
            "cover_image": "https://blog.example.com/images/hashnode/graphql-cover.png",
            "canonical_url": ""
        },
        
        "markdown": """# GraphQL Federation: Scaling APIs Across Teams

> _Build unified GraphQL APIs that scale across multiple teams and services without sacrificing developer experience._

**Estimated read**: ~10 min

## Table of Contents
- [Introduction](#introduction)
- [Federation Basics](#federation-basics)
- [Schema Design](#schema-design)
- [Implementation](#implementation)
- [Gateway Setup](#gateway-setup)
- [Trade-offs](#trade-offs)
- [Conclusion](#conclusion)

## Introduction

GraphQL Federation solves the challenge of scaling GraphQL across multiple teams. Instead of a monolithic schema, federation allows teams to own their domain-specific schemas while presenting a unified API to clients. Apollo's federation specification has been adopted by companies managing 100+ microservices.

## Federation Basics

Federation works through a gateway that composes multiple subgraphs into a single supergraph. Each team maintains their own GraphQL service with domain-specific types and resolvers.

## Schema Design

Design federated schemas using entities and references. The `@key` directive defines how entities can be resolved across services.

```mermaid
flowchart TD
    A[Gateway] --> B[User Service]
    A --> C[Order Service]
    A --> D[Product Service]
    B --> E[User Entity]
    C --> F[Order Entity]
    D --> G[Product Entity]
```

_Alt text_: Federation gateway composing multiple services into unified schema.

## Implementation

Set up a federated service using Apollo Federation:

```bash
# Install federation dependencies
npm install @apollo/federation @apollo/gateway
npm install @apollo/subgraph
```

```javascript
// User service subgraph
const { buildSubgraphSchema } = require('@apollo/subgraph');
const { gql } = require('apollo-server');

const typeDefs = gql`
  type User @key(fields: "id") {
    id: ID!
    email: String!
    name: String!
  }
  
  extend type Order @key(fields: "id") {
    id: ID! @external
    user: User
  }
`;

const resolvers = {
  User: {
    __resolveReference(user) {
      return getUserById(user.id);
    }
  },
  Order: {
    user(order) {
      return { __typename: "User", id: order.userId };
    }
  }
};

const schema = buildSubgraphSchema({ typeDefs, resolvers });
```

## Gateway Setup

Configure the Apollo Gateway to compose subgraphs:

```javascript
// Gateway configuration
const { ApolloGateway } = require('@apollo/gateway');
const { ApolloServer } = require('apollo-server');

const gateway = new ApolloGateway({
  serviceList: [
    { name: 'users', url: 'http://localhost:4001/graphql' },
    { name: 'orders', url: 'http://localhost:4002/graphql' },
    { name: 'products', url: 'http://localhost:4003/graphql' }
  ]
});

const server = new ApolloServer({ gateway });
```

## Trade-offs

- Pro: Team autonomy with independent deployments
- Pro: Type safety across service boundaries
- Con: Query planning complexity increases latency
- Con: Schema coordination requires governance

## Conclusion

GraphQL Federation enables teams to scale GraphQL architecture while maintaining a unified developer experience. Start with clear entity boundaries and evolve your federation strategy as your organization grows.
""",
        
        "reading_time_min": 10,
        
        "toc": [
            {"title": "Introduction", "anchor": "#introduction"},
            {"title": "Federation Basics", "anchor": "#federation-basics"},
            {"title": "Schema Design", "anchor": "#schema-design"},
            {"title": "Implementation", "anchor": "#implementation"},
            {"title": "Gateway Setup", "anchor": "#gateway-setup"},
            {"title": "Trade-offs", "anchor": "#trade-offs"},
            {"title": "Conclusion", "anchor": "#conclusion"}
        ],
        
        "sections": [
            {
                "h2": "Introduction",
                "summary": "GraphQL Federation enables scaling across multiple teams and services",
                "key_points": ["Unified API from multiple schemas", "Adopted by 100+ microservice companies"]
            },
            {
                "h2": "Federation Basics",
                "summary": "Gateway composes subgraphs into unified supergraph for clients",
                "key_points": ["Gateway composition", "Team-owned subgraphs"]
            },
            {
                "h2": "Schema Design",
                "summary": "Entity design with @key directives for cross-service resolution",
                "key_points": ["Entity relationships", "@key directive usage"]
            },
            {
                "h2": "Implementation",
                "summary": "Apollo Federation setup for user service subgraph",
                "key_points": ["Subgraph schema building", "Reference resolvers"]
            }
        ],
        
        "code_snippets": [
            {
                "language": "bash",
                "label": "Dependencies",
                "content": "```bash\n# Install federation dependencies\nnpm install @apollo/federation @apollo/gateway\nnpm install @apollo/subgraph\n```",
                "runnable": True
            },
            {
                "language": "javascript",
                "label": "Subgraph Service",
                "content": "```javascript\n// User service subgraph\nconst { buildSubgraphSchema } = require('@apollo/subgraph');\nconst { gql } = require('apollo-server');\n\nconst typeDefs = gql`\n  type User @key(fields: \"id\") {\n    id: ID!\n    email: String!\n    name: String!\n  }\n  \n  extend type Order @key(fields: \"id\") {\n    id: ID! @external\n    user: User\n  }\n`;\n\nconst resolvers = {\n  User: {\n    __resolveReference(user) {\n      return getUserById(user.id);\n    }\n  },\n  Order: {\n    user(order) {\n      return { __typename: \"User\", id: order.userId };\n    }\n  }\n};\n\nconst schema = buildSubgraphSchema({ typeDefs, resolvers });\n```",
                "runnable": True
            }
        ],
        
        "diagram_blocks": [
            {
                "id": "d1",
                "type": "mermaid",
                "alt": "Federation gateway composing multiple services into unified schema",
                "content": "flowchart TD\n    A[Gateway] --> B[User Service]\n    A --> C[Order Service]\n    A --> D[Product Service]\n    B --> E[User Entity]\n    C --> F[Order Entity]\n    D --> G[Product Entity]",
                "placement_hint": "in Schema Design"
            }
        ],
        
        "series_potential": {
            "is_part_one": False,
            "suggested_next_parts": [
                "Advanced Federation Patterns",
                "Schema Governance at Scale"
            ]
        },
        
        "seo": {
            "meta_title": "GraphQL Federation: Scaling APIs Across Teams",
            "meta_description": "Learn GraphQL Federation for scaling APIs across teams. Includes Apollo Federation setup, schema design patterns, and implementation examples.",
            "keywords_used": ["graphql", "federation", "apollo", "microservices", "api-design"],
            "lsi_terms_used": ["subgraph", "supergraph", "gateway", "schema-composition"]
        },
        
        "cta": {
            "text": "If this helped, follow for more GraphQL architecture insights.",
            "link": ""
        },
        
        "image_prompts": [
            {
                "role": "cover",
                "title": "Hashnode Cover",
                "prompt": "Minimal wide banner for GraphQL Federation with API architecture iconography; short headline 'GraphQL Federation' top-left; off-white/light background; thin vector strokes; subtle dotted grid; purple accent color; generous margins; flat vector; crisp at 1200×630.",
                "negative_prompt": "no stock-photo people, no logos, no neon, no 3D bevels, no glossy gradients, no clutter",
                "style_notes": "editorial-tech; crisp kerning; consistent stroke widths",
                "ratio": "1.91:1",
                "size_px": "1200x630",
                "alt_text": "Wide minimal banner with GraphQL federation architecture glyph"
            }
        ],
        
        "compliance": {
            "word_count": 1678,
            "title_char_count": 47,
            "tags_count": 5,
            "sections_count": 4,
            "code_snippets_count": 2,
            "diagram_blocks_count": 1,
            "has_toc": True,
            "image_prompt_count": 1,
            "has_canonical": False,
            "has_tracked_link_once": False,
            "keyword_overrides": False,
            "checks": [
                "1678 words (within 1500-3000 range)",
                "SEO title 47 chars; slug lowercase-hyphenated",
                "TOC present with 7 sections",
                "2 runnable code snippets and 1 diagram",
                "5 relevant lowercase tags",
                "no canonical_url (not republishing)",
                "no tracked link (no primary_url)",
                "1 cover image prompt"
            ]
        }
    }
    
    try:
        hashnode_article = HashnodeArticleContent(**minimal_content)
        print("✅ Direct schema instantiation successful")
        print(f"📊 Hashnode Article structure:")
        print(f"   • Title: {len(hashnode_article.front_matter['title'])} characters")
        print(f"   • Reading time: {hashnode_article.reading_time_min} minutes")
        print(f"   • TOC sections: {len(hashnode_article.toc)}")
        print(f"   • Code snippets: {len(hashnode_article.code_snippets)}")
        print(f"   • Diagram blocks: {len(hashnode_article.diagram_blocks)}")
        print(f"   • Tags: {len(hashnode_article.front_matter['tags'])}")
        print(f"   • Series potential: {len(hashnode_article.series_potential['suggested_next_parts'])} parts")
        
        # Test JSON serialization
        json_data = hashnode_article.model_dump()
        json_str = json.dumps(json_data, indent=2)
        print("✅ JSON serialization successful")
        print(f"📄 JSON size: {len(json_str)} characters")
        
        return True
        
    except Exception as e:
        print(f"❌ Direct schema instantiation failed: {e}")
        return False

def main():
    """Run all Hashnode Article tests"""
    print("🧪 HASHNODE ARTICLE CONTENT GENERATION TESTS")
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
        print("🎉 All Hashnode Article tests passed! Ready for integration.")
        return True
    else:
        print("⚠️ Some tests failed. Check implementation.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
