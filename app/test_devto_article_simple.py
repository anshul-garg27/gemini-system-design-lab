#!/usr/bin/env python3
"""
Test suite for dev.to Article content generation.
Tests prompt processing, schema validation, and direct schema instantiation.
"""

import sys
import os
import json
from pathlib import Path

# Add the app directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from schemas import DevToArticleContent, validate_content

def load_prompt_template():
    """Load the dev.to Article prompt template"""
    prompt_path = Path(__file__).parent / "prompts" / "bodies" / "devto-article.txt"
    if not prompt_path.exists():
        raise FileNotFoundError(f"Prompt template not found: {prompt_path}")
    
    with open(prompt_path, 'r', encoding='utf-8') as f:
        return f.read()

def process_prompt_with_topic(template, topic_data):
    """Process prompt template with topic data"""
    # Sample topic data for testing
    sample_data = {
        "topic_id": "3001",
        "topic_name": topic_data.get("name", "Building a Real-time WebSocket Chat with Node.js"),
        "topic_description": topic_data.get("description", "Step-by-step guide to building a scalable real-time chat application"),
        "audience": "intermediate",
        "tone": "clear, confident, friendly, non-cringe",
        "locale": "en",
        "primary_url": "https://blog.example.com/websocket-chat-nodejs",
        **topic_data.get("brand", {
            "site_url": "https://blog.example.com",
            "handles": {"x": "@systemdesign", "linkedin": "@systemdesign", "github": "@systemdesign"},
            "utm_base": "utm_source=devto&utm_medium=article"
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
    """Test 1: dev.to Article prompt template processing"""
    print("=" * 60)
    print("TEST 1: dev.to Article Prompt Processing")
    print("=" * 60)
    
    try:
        template = load_prompt_template()
        
        # Test with WebSocket chat topic
        topic_data = {
            "name": "Building a Real-time WebSocket Chat with Node.js",
            "description": "Step-by-step guide to building a scalable real-time chat application with Socket.io and Express"
        }
        
        processed_prompt = process_prompt_with_topic(template, topic_data)
        
        print("✅ Prompt template processed successfully")
        print(f"📄 Template path: prompts/bodies/devto-article.txt")
        print(f"🎯 Topic: {topic_data['name']}")
        print(f"📝 Processed prompt length: {len(processed_prompt)} characters")
        
        # Verify key elements are present
        checks = {
            "Contains topic name": topic_data["name"] in processed_prompt,
            "Contains JSON format": '"content":' in processed_prompt,
            "Contains front matter": "front_matter" in processed_prompt,
            "Contains code snippets": "code_snippets" in processed_prompt,
            "Contains diagram blocks": "diagram_blocks" in processed_prompt,
            "Contains cover image requirement": "cover_image" in processed_prompt
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
    """Test 2: dev.to Article schema validation with sample data"""
    print("\n" + "=" * 60)
    print("TEST 2: dev.to Article Schema Validation")
    print("=" * 60)
    
    # Sample dev.to Article content
    sample_content = {
        "front_matter": {
            "title": "Building Real-time Chat with WebSockets and Node.js",
            "published": True,
            "tags": ["javascript", "nodejs", "websockets", "tutorial"],
            "cover_image": "https://blog.example.com/images/devto/3001-cover.png",
            "canonical_url": "https://blog.example.com/websocket-chat-nodejs"
        },
        
        "markdown": """---
title: Building Real-time Chat with WebSockets and Node.js
published: true
tags: [javascript, nodejs, websockets, tutorial]
cover_image: https://blog.example.com/images/devto/3001-cover.png
canonical_url: https://blog.example.com/websocket-chat-nodejs
---

# Building Real-time Chat with WebSockets and Node.js

_Who this helps_: intermediate. _Time to read_: ~8 min.

## Why this matters

Real-time communication is essential for modern web applications. Traditional HTTP polling creates unnecessary server load and introduces latency. WebSockets provide persistent connections that enable instant bidirectional communication, reducing server requests by up to 95%.

## Quick start

Follow these steps to get a minimal working chat application.

```bash
# Create project and install dependencies
mkdir websocket-chat
cd websocket-chat
npm init -y
npm install express socket.io
```

```javascript
// server.js - Basic Express server with Socket.io
const express = require('express');
const http = require('http');
const socketIo = require('socket.io');

const app = express();
const server = http.createServer(app);
const io = socketIo(server);

app.use(express.static('public'));

io.on('connection', (socket) => {
  console.log('User connected:', socket.id);
  
  socket.on('chat message', (msg) => {
    io.emit('chat message', {
      id: socket.id,
      message: msg,
      timestamp: Date.now()
    });
  });
  
  socket.on('disconnect', () => {
    console.log('User disconnected:', socket.id);
  });
});

server.listen(3000, () => {
  console.log('Server running on http://localhost:3000');
});
```

```html
<!-- public/index.html - Simple chat interface -->
<!DOCTYPE html>
<html>
<head>
    <title>WebSocket Chat</title>
    <script src="/socket.io/socket.io.js"></script>
</head>
<body>
    <div id="messages"></div>
    <form id="form">
        <input id="input" autocomplete="off" />
        <button>Send</button>
    </form>
    
    <script>
        const socket = io();
        const form = document.getElementById('form');
        const input = document.getElementById('input');
        const messages = document.getElementById('messages');
        
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            if (input.value) {
                socket.emit('chat message', input.value);
                input.value = '';
            }
        });
        
        socket.on('chat message', (data) => {
            const item = document.createElement('li');
            item.textContent = `${data.id}: ${data.message}`;
            messages.appendChild(item);
        });
    </script>
</body>
</html>
```

## How it works

The architecture uses Socket.io for WebSocket management with automatic fallbacks.

```mermaid
flowchart LR
    A[Client] -->|WebSocket| B[Socket.io Server]
    B -->|Broadcast| C[All Connected Clients]
    B -->|Store| D[Message History]
    D -->|Retrieve| B
```

## Trade-offs & pitfalls

- Pro: Real-time communication with minimal latency
- Pro: Automatic connection management and fallbacks
- Con: Stateful connections require sticky sessions in load balancers
- Con: Memory usage scales with concurrent connections

## Benchmarks / Results

- Connection establishment: ~50ms
- Message broadcast latency: ~2ms
- Memory per connection: ~4KB
- Tested with 1000 concurrent connections on 2GB RAM

## Wrap-up & next steps

You now have a working real-time chat application. For production use, consider adding authentication, message persistence, and rate limiting.

If you want the deeper dive with scaling strategies and production deployment, read the full breakdown: https://blog.example.com/websocket-chat-nodejs?utm_source=devto&utm_medium=article
""",
        
        "reading_time_min": 8,
        
        "code_snippets": [
            {
                "language": "bash",
                "label": "Project Setup",
                "content": "```bash\n# Create project and install dependencies\nmkdir websocket-chat\ncd websocket-chat\nnpm init -y\nnpm install express socket.io\n```",
                "runnable": True
            },
            {
                "language": "javascript",
                "label": "Server Implementation",
                "content": "```javascript\n// server.js - Basic Express server with Socket.io\nconst express = require('express');\nconst http = require('http');\nconst socketIo = require('socket.io');\n\nconst app = express();\nconst server = http.createServer(app);\nconst io = socketIo(server);\n\napp.use(express.static('public'));\n\nio.on('connection', (socket) => {\n  console.log('User connected:', socket.id);\n  \n  socket.on('chat message', (msg) => {\n    io.emit('chat message', {\n      id: socket.id,\n      message: msg,\n      timestamp: Date.now()\n    });\n  });\n  \n  socket.on('disconnect', () => {\n    console.log('User disconnected:', socket.id);\n  });\n});\n\nserver.listen(3000, () => {\n  console.log('Server running on http://localhost:3000');\n});\n```",
                "runnable": True
            },
            {
                "language": "html",
                "label": "Client Interface",
                "content": "```html\n<!-- public/index.html - Simple chat interface -->\n<!DOCTYPE html>\n<html>\n<head>\n    <title>WebSocket Chat</title>\n    <script src=\"/socket.io/socket.io.js\"></script>\n</head>\n<body>\n    <div id=\"messages\"></div>\n    <form id=\"form\">\n        <input id=\"input\" autocomplete=\"off\" />\n        <button>Send</button>\n    </form>\n    \n    <script>\n        const socket = io();\n        const form = document.getElementById('form');\n        const input = document.getElementById('input');\n        const messages = document.getElementById('messages');\n        \n        form.addEventListener('submit', (e) => {\n            e.preventDefault();\n            if (input.value) {\n                socket.emit('chat message', input.value);\n                input.value = '';\n            }\n        });\n        \n        socket.on('chat message', (data) => {\n            const item = document.createElement('li');\n            item.textContent = `${data.id}: ${data.message}`;\n            messages.appendChild(item);\n        });\n    </script>\n</body>\n</html>\n```",
                "runnable": True
            }
        ],
        
        "diagram_blocks": [
            {
                "id": "d1",
                "type": "mermaid",
                "alt": "WebSocket chat architecture flow",
                "content": "flowchart LR\n    A[Client] -->|WebSocket| B[Socket.io Server]\n    B -->|Broadcast| C[All Connected Clients]\n    B -->|Store| D[Message History]\n    D -->|Retrieve| B",
                "placement_hint": "after How it works"
            }
        ],
        
        "resources": [
            {
                "title": "Socket.io Documentation",
                "url": "https://socket.io/docs/v4/",
                "note": "Official documentation with advanced features"
            },
            {
                "title": "WebSocket MDN Guide",
                "url": "https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API",
                "note": "Browser WebSocket API reference"
            }
        ],
        
        "image_prompts": [
            {
                "role": "cover",
                "title": "Dev.to Cover",
                "prompt": "Widescreen minimal cover for Building Real-time Chat with WebSockets. Clean typographic title 'WebSocket Chat' top-left; small network diagram glyph to the right showing connected nodes; off-white/light background; thin vector strokes; subtle dotted grid; blue accent color; generous margins; flat vector; export crisp 1200×630.",
                "negative_prompt": "no stock-photo people, no logos, no neon, no 3D bevels, no glossy gradients, no clutter",
                "style_notes": "editorial poster tone; crisp kerning; consistent stroke widths",
                "ratio": "1.91:1",
                "size_px": "1200x630",
                "alt_text": "Wide cover with WebSocket Chat title and network diagram glyph"
            }
        ],
        
        "seo": {
            "keywords_used": ["websockets", "nodejs", "real-time", "chat", "socket.io"],
            "lsi_terms_used": ["bidirectional", "persistent", "connection", "broadcast"]
        },
        
        "compliance": {
            "word_count": 1456,
            "code_snippets_count": 3,
            "diagram_blocks_count": 1,
            "tags_count": 4,
            "has_cover_image": True,
            "image_prompt_count": 1,
            "has_tracked_link_once": True,
            "keyword_overrides": False,
            "checks": [
                "1000–2500 words",
                "≥2 runnable code snippets with language fences",
                "≥1 diagram block (mermaid) with alt text",
                "≤4 tags, lowercase, topic-appropriate",
                "front_matter.cover_image is a full URL",
                "exactly one tracked link in body",
                "image_prompts length matches image_plan.count"
            ]
        }
    }
    
    try:
        print("🧪 Testing direct schema validation...")
        devto_article = DevToArticleContent(**sample_content)
        print("✅ Direct schema validation passed")
        print(f"📊 Title length: {len(devto_article.front_matter['title'])} chars")
        print(f"📝 Word count: {devto_article.compliance['word_count']} words")
        print(f"💻 Code snippets: {len(devto_article.code_snippets)}")
        print(f"📊 Diagram blocks: {len(devto_article.diagram_blocks)}")
        print(f"🏷️ Tags: {len(devto_article.front_matter['tags'])}")
        print(f"🖼️ Cover image: {'Yes' if devto_article.front_matter['cover_image'] else 'No'}")
        
        print("\n🧪 Testing schema validator function...")
        validated_content = validate_content("devto", "article", sample_content)
        print("✅ Schema validator function passed")
        print(f"📋 Validated content type: {type(validated_content).__name__}")
        
        print(f"\n📋 Sample dev.to Article Structure:")
        print(f"   • Title: {len(devto_article.front_matter['title'])} characters")
        print(f"   • Reading time: {devto_article.reading_time_min} minutes")
        print(f"   • Code snippets: {len(devto_article.code_snippets)} runnable examples")
        print(f"   • Diagrams: {len(devto_article.diagram_blocks)} mermaid blocks")
        print(f"   • Resources: {len(devto_article.resources)} external links")
        
        return True
        
    except Exception as e:
        print(f"❌ Schema validation failed: {e}")
        return False

def test_direct_schema_instantiation():
    """Test 3: Direct dev.to Article schema instantiation"""
    print("\n" + "=" * 60)
    print("TEST 3: Direct dev.to Article Schema Instantiation")
    print("=" * 60)
    
    # Minimal valid dev.to Article content
    minimal_content = {
        "front_matter": {
            "title": "Docker Multi-stage Builds: Reduce Image Size by 80%",
            "published": True,
            "tags": ["docker", "devops", "optimization"],
            "cover_image": "https://blog.example.com/images/devto/docker-cover.png",
            "canonical_url": ""
        },
        
        "markdown": """---
title: Docker Multi-stage Builds: Reduce Image Size by 80%
published: true
tags: [docker, devops, optimization]
cover_image: https://blog.example.com/images/devto/docker-cover.png
---

# Docker Multi-stage Builds: Reduce Image Size by 80%

_Who this helps_: intermediate. _Time to read_: ~6 min.

## Why this matters

Docker images can quickly become bloated with build tools and dependencies. A typical Node.js image with build tools can be 1.2GB, but production only needs the runtime. Multi-stage builds can reduce this to 200MB - an 80% reduction.

## Quick start

Here's how to implement multi-stage builds for a Node.js application.

```dockerfile
# Multi-stage Dockerfile
# Stage 1: Build stage
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

# Stage 2: Production stage  
FROM node:18-alpine AS production
WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY . .
EXPOSE 3000
CMD ["node", "server.js"]
```

```bash
# Build and compare sizes
docker build -t app-multistage .
docker images | grep app
```

## How it works

Multi-stage builds use multiple FROM statements to create intermediate images.

```mermaid
flowchart TD
    A[Source Code] --> B[Build Stage]
    B --> C[Install Dependencies]
    B --> D[Compile Assets]
    C --> E[Production Stage]
    D --> E
    E --> F[Final Image]
```

## Trade-offs & pitfalls

- Pro: Dramatically smaller production images
- Pro: Cleaner separation of build and runtime environments
- Con: Slightly more complex Dockerfile syntax
- Con: Build cache invalidation affects all stages

## Benchmarks / Results

- Before: 1.2GB (full Node.js with build tools)
- After: 240MB (runtime only)
- Build time: +15% (due to multi-stage overhead)
- Deploy time: -60% (smaller image transfers)

## Wrap-up & next steps

Multi-stage builds are essential for production Docker images. Next, explore distroless images and security scanning for even better optimization.
""",
        
        "reading_time_min": 6,
        
        "code_snippets": [
            {
                "language": "dockerfile",
                "label": "Multi-stage Dockerfile",
                "content": "```dockerfile\n# Multi-stage Dockerfile\n# Stage 1: Build stage\nFROM node:18-alpine AS builder\nWORKDIR /app\nCOPY package*.json ./\nRUN npm ci --only=production\n\n# Stage 2: Production stage  \nFROM node:18-alpine AS production\nWORKDIR /app\nCOPY --from=builder /app/node_modules ./node_modules\nCOPY . .\nEXPOSE 3000\nCMD [\"node\", \"server.js\"]\n```",
                "runnable": True
            },
            {
                "language": "bash",
                "label": "Build Commands",
                "content": "```bash\n# Build and compare sizes\ndocker build -t app-multistage .\ndocker images | grep app\n```",
                "runnable": True
            }
        ],
        
        "diagram_blocks": [
            {
                "id": "d1",
                "type": "mermaid",
                "alt": "Multi-stage build process flow",
                "content": "flowchart TD\n    A[Source Code] --> B[Build Stage]\n    B --> C[Install Dependencies]\n    B --> D[Compile Assets]\n    C --> E[Production Stage]\n    D --> E\n    E --> F[Final Image]",
                "placement_hint": "after How it works"
            }
        ],
        
        "resources": [
            {
                "title": "Docker Multi-stage Builds Documentation",
                "url": "https://docs.docker.com/develop/dev-best-practices/",
                "note": "Official Docker best practices guide"
            }
        ],
        
        "image_prompts": [
            {
                "role": "cover",
                "title": "Dev.to Cover",
                "prompt": "Widescreen minimal cover for Docker Multi-stage Builds. Clean typographic title 'Docker Optimization' top-left; small layered container diagram glyph to the right; off-white/light background; thin vector strokes; subtle dotted grid; blue accent color; generous margins; flat vector; export crisp 1200×630.",
                "negative_prompt": "no stock-photo people, no logos, no neon, no 3D bevels, no glossy gradients, no clutter",
                "style_notes": "editorial poster tone; crisp kerning; consistent stroke widths",
                "ratio": "1.91:1",
                "size_px": "1200x630",
                "alt_text": "Wide cover with Docker title and container layers diagram"
            }
        ],
        
        "seo": {
            "keywords_used": ["docker", "multi-stage", "optimization", "devops"],
            "lsi_terms_used": ["container", "image", "build", "production"]
        },
        
        "compliance": {
            "word_count": 1124,
            "code_snippets_count": 2,
            "diagram_blocks_count": 1,
            "tags_count": 3,
            "has_cover_image": True,
            "image_prompt_count": 1,
            "has_tracked_link_once": False,
            "keyword_overrides": False,
            "checks": [
                "1000+ words",
                "2 runnable code snippets",
                "1 mermaid diagram",
                "3 relevant tags",
                "cover image URL provided",
                "no tracked link (canonical_url empty)"
            ]
        }
    }
    
    try:
        devto_article = DevToArticleContent(**minimal_content)
        print("✅ Direct schema instantiation successful")
        print(f"📊 dev.to Article structure:")
        print(f"   • Title: {len(devto_article.front_matter['title'])} characters")
        print(f"   • Reading time: {devto_article.reading_time_min} minutes")
        print(f"   • Code snippets: {len(devto_article.code_snippets)}")
        print(f"   • Diagram blocks: {len(devto_article.diagram_blocks)}")
        print(f"   • Tags: {len(devto_article.front_matter['tags'])}")
        print(f"   • Resources: {len(devto_article.resources)}")
        
        # Test JSON serialization
        json_data = devto_article.model_dump()
        json_str = json.dumps(json_data, indent=2)
        print("✅ JSON serialization successful")
        print(f"📄 JSON size: {len(json_str)} characters")
        
        return True
        
    except Exception as e:
        print(f"❌ Direct schema instantiation failed: {e}")
        return False

def main():
    """Run all dev.to Article tests"""
    print("🧪 DEV.TO ARTICLE CONTENT GENERATION TESTS")
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
        print("🎉 All dev.to Article tests passed! Ready for integration.")
        return True
    else:
        print("⚠️ Some tests failed. Check implementation.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
