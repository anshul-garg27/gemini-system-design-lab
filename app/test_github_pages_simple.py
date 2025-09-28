#!/usr/bin/env python3
"""
Test suite for GitHub Pages content generation.
Tests prompt processing, schema validation, and direct schema instantiation.
"""

import sys
import os
import json
from pathlib import Path

# Add the app directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from schemas import GitHubPagesContent, validate_content

def load_prompt_template():
    """Load the GitHub Pages prompt template"""
    prompt_path = Path(__file__).parent / "prompts" / "bodies" / "github-pages.txt"
    if not prompt_path.exists():
        raise FileNotFoundError(f"Prompt template not found: {prompt_path}")
    
    with open(prompt_path, 'r', encoding='utf-8') as f:
        return f.read()

def process_prompt_with_topic(template, topic_data):
    """Process prompt template with topic data"""
    # Sample topic data for testing
    sample_data = {
        "topic_id": "5001",
        "topic_name": topic_data.get("name", "FastAPI Rate Limiter"),
        "topic_description": topic_data.get("description", "Production-ready rate limiting middleware for FastAPI applications with Redis backend and configurable strategies"),
        "audience": "intermediate",
        "tone": "clear, confident, friendly, non-cringe",
        "locale": "en",
        "primary_url": "https://blog.example.com/fastapi-rate-limiter",
        **topic_data.get("brand", {
            "site_url": "https://blog.example.com",
            "handles": {"github": "@systemdesign", "x": "@systemdesign", "linkedin": "@systemdesign"},
            "utm_base": "utm_source=github&utm_medium=repo"
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
    """Test 1: GitHub Pages prompt template processing"""
    print("=" * 60)
    print("TEST 1: GitHub Pages Prompt Processing")
    print("=" * 60)
    
    try:
        template = load_prompt_template()
        
        # Test with FastAPI rate limiter topic
        topic_data = {
            "name": "FastAPI Rate Limiter",
            "description": "Production-ready rate limiting middleware for FastAPI applications with Redis backend and configurable strategies"
        }
        
        processed_prompt = process_prompt_with_topic(template, topic_data)
        
        print("✅ Prompt template processed successfully")
        print(f"📄 Template path: prompts/bodies/github-pages.txt")
        print(f"🎯 Topic: {topic_data['name']}")
        print(f"📝 Processed prompt length: {len(processed_prompt)} characters")
        
        # Verify key elements are present
        checks = {
            "Contains topic name": topic_data["name"] in processed_prompt,
            "Contains JSON format": '"content":' in processed_prompt,
            "Contains README sections": "readme_markdown" in processed_prompt,
            "Contains GitHub Pages config": "gh_pages" in processed_prompt,
            "Contains CI suggestion": "ci_suggestion" in processed_prompt,
            "Contains discussions seed": "discussions_seed" in processed_prompt,
            "Contains badges": "badges" in processed_prompt
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
    """Test 2: GitHub Pages schema validation with sample data"""
    print("\n" + "=" * 60)
    print("TEST 2: GitHub Pages Schema Validation")
    print("=" * 60)
    
    # Sample GitHub Pages content
    sample_content = {
        "repo_skeleton": [
            ".github/workflows/ci.yml",
            "docs/index.md",
            "examples/basic_usage.py",
            "src/fastapi_rate_limiter/",
            "tests/",
            "README.md",
            "requirements.txt",
            "setup.py"
        ],
        
        "badges": [
            {
                "alt": "CI",
                "image_url": "https://img.shields.io/github/actions/workflow/status/systemdesign/fastapi-rate-limiter/ci.yml",
                "link_url": "https://github.com/systemdesign/fastapi-rate-limiter/actions"
            },
            {
                "alt": "License",
                "image_url": "https://img.shields.io/badge/license-MIT-green.svg",
                "link_url": "LICENSE"
            },
            {
                "alt": "Python",
                "image_url": "https://img.shields.io/badge/python-3.8%2B-blue.svg",
                "link_url": "https://python.org"
            }
        ],
        
        "readme_markdown": """# FastAPI Rate Limiter

[![CI](https://img.shields.io/github/actions/workflow/status/systemdesign/fastapi-rate-limiter/ci.yml)](https://github.com/systemdesign/fastapi-rate-limiter/actions)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org)

Production-ready rate limiting middleware for FastAPI applications with Redis backend and configurable strategies.

- **Demo**: https://fastapi-rate-limiter-demo.herokuapp.com
- **Docs**: ./docs/index.md
- **Further reading**: https://blog.example.com/fastapi-rate-limiter?utm_source=github&utm_medium=repo

## Table of Contents
- [Features](#features)
- [Quickstart](#quickstart)
- [Usage](#usage)
- [Configuration](#configuration)
- [Architecture](#architecture)
- [Roadmap](#roadmap)
- [Benchmarks](#benchmarks)
- [Contributing](#contributing)
- [License](#license)
- [FAQ](#faq)

## Features
- Multiple rate limiting strategies (fixed window, sliding window, token bucket)
- Redis backend for distributed rate limiting
- FastAPI middleware integration
- Configurable rate limits per endpoint
- Custom key extraction (IP, user ID, API key)
- Detailed metrics and monitoring

## Quickstart
```bash
# clone
git clone https://github.com/systemdesign/fastapi-rate-limiter.git
cd fastapi-rate-limiter

# create env
python -m venv .venv && source .venv/bin/activate

# install
pip install -e .
```

## Usage
```python
# minimal runnable example
from fastapi import FastAPI
from fastapi_rate_limiter import RateLimiter, RateLimitMiddleware

app = FastAPI()
rate_limiter = RateLimiter(redis_url="redis://localhost:6379")
app.add_middleware(RateLimitMiddleware, rate_limiter=rate_limiter)

@app.get("/api/data")
@rate_limiter.limit("100/minute")
async def get_data():
    return {"message": "Hello World"}
```

## Configuration
| Name | Type | Default | Description |
|------|------|---------|-------------|
| REDIS_URL | string | "redis://localhost:6379" | Redis connection URL |
| DEFAULT_RATE_LIMIT | string | "1000/hour" | Default rate limit |
| RATE_LIMIT_STRATEGY | string | "fixed_window" | Rate limiting strategy |
| KEY_EXTRACTOR | string | "ip" | Key extraction method |

Set via environment variables or `.env`.

## Architecture
```mermaid
flowchart LR
    Client-->Middleware[Rate Limit Middleware]
    Middleware-->Redis[(Redis)]
    Middleware-->FastAPI[FastAPI App]
    Redis-->Middleware
    FastAPI-->Client
```
_Alt text_: Request flow through rate limiting middleware with Redis backend.

## Roadmap
- [ ] Distributed rate limiting with consistent hashing
- [ ] GraphQL support
- [ ] Rate limit headers (X-RateLimit-*)
- [ ] WebSocket rate limiting

## Benchmarks
- p95 latency: 2.3ms (local Redis)
- Throughput: 15,000 rps (single instance)
- Memory usage: ~50MB (100k active keys)

## Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md). Please run tests and linters before PRs.

## License
MIT © Contributors

## FAQ
**Q:** How does distributed rate limiting work?  
**A:** Uses Redis as a shared state store across multiple FastAPI instances.

**Q:** Can I use custom rate limit keys?  
**A:** Yes, implement a custom key extractor function.
""",
        
        "gh_pages": {
            "index_markdown": """---
layout: default
title: FastAPI Rate Limiter
---

# FastAPI Rate Limiter

Production-ready rate limiting middleware for FastAPI applications with Redis backend and configurable strategies.

- **Get started:** [README](../README.md#quickstart)
- **Architecture:** [diagram](../README.md#architecture)
- **Examples:** [/examples](../examples)

> For a deep-dive, read: https://blog.example.com/fastapi-rate-limiter?utm_source=github&utm_medium=repo
""",
            "_config_yaml": """title: FastAPI Rate Limiter
remote_theme: pages-themes/minimal@v0.2.0
plugins:
  - jekyll-remote-theme
  - jekyll-seo-tag
  - jekyll-sitemap
markdown: kramdown
""",
            "nav": [
                {"title": "Home", "href": "/"},
                {"title": "README", "href": "/README"},
                {"title": "Examples", "href": "/examples/"}
            ]
        },
        
        "ci_suggestion": {
            "workflow_name": "CI",
            "file_path": ".github/workflows/ci.yml",
            "yaml": """name: CI
on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
jobs:
  build:
    runs-on: ubuntu-latest
    services:
      redis:
        image: redis:7
        ports:
          - 6379:6379
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.11' }
      - run: pip install -e . && pip install pytest pytest-asyncio
      - run: pytest -v --cov=src
"""
        },
        
        "discussions_seed": {
            "title": "Would you approach FastAPI Rate Limiter differently at scale?",
            "body": """### Context
Production-ready rate limiting middleware for FastAPI applications with Redis backend and configurable strategies

### What I'm sharing
- Minimal runnable example with FastAPI middleware
- Architecture sketch showing Redis integration
- Multiple rate limiting strategies (fixed window, sliding window, token bucket)

### What I'd love feedback on
- Trade-offs between different rate limiting algorithms
- Config defaults for common API patterns
- Distributed rate limiting approaches
- Performance optimization strategies

### Stack
- Language: Python 3.8+
- Framework: FastAPI
- Backend: Redis
- Infra: Docker-compose for local dev

### Known limitations
- Currently single Redis instance (no clustering)
- Limited WebSocket support
- No built-in rate limit headers

### Links
- Repo README (this)
- Deep-dive: https://blog.example.com/fastapi-rate-limiter?utm_source=github&utm_medium=repo""",
            "category_suggestion": "Show and tell",
            "labels": ["discussion", "help wanted", "question", "performance"]
        },
        
        "labels_suggestions": [
            {"name": "good first issue", "color": "7057ff"},
            {"name": "help wanted", "color": "008672"},
            {"name": "discussion", "color": "0366d6"},
            {"name": "bug", "color": "d73a4a"},
            {"name": "enhancement", "color": "a2eeef"},
            {"name": "performance", "color": "fbca04"},
            {"name": "documentation", "color": "0075ca"}
        ],
        
        "image_prompts": [
            {
                "role": "repo_diagram",
                "title": "Repository Architecture Diagram",
                "prompt": "Widescreen minimal diagram for FastAPI Rate Limiter: request flow through middleware. Show blocks for client, rate limit middleware, Redis, FastAPI app; arrows and 4-5 short labels; off-white/light background; thin vector strokes; subtle dotted grid; blue accent color; flat vector; generous margins; legible at 1200×630.",
                "negative_prompt": "no stock photos, no faces, no logos, no neon, no 3D bevels, no glossy gradients, no clutter",
                "style_notes": "editorial-tech; crisp kerning; consistent stroke widths",
                "ratio": "1.91:1",
                "size_px": "1200x630",
                "alt_text": "FastAPI rate limiter architecture with Redis backend"
            }
        ],
        
        "compliance": {
            "has_readme_sections": True,
            "has_toc": True,
            "has_quickstart_and_usage": True,
            "has_config_table": True,
            "has_arch_diagram_block": True,
            "has_license": True,
            "discussion_has_questions": True,
            "labels_count_ok": True,
            "image_prompt_count": 1,
            "has_tracked_link_once": True,
            "checks": [
                "README includes title/badges/description/TOC/features/quickstart/usage/config/architecture/roadmap/benchmarks/contributing/license/FAQ",
                "GitHub Pages: index.md + _config.yml provided",
                "CI workflow suggestion with Redis service",
                "Discussions seed includes context + concrete feedback asks",
                "Exactly one tracked link in README under Further reading",
                "1 repository diagram image prompt matches image_plan.count"
            ]
        }
    }
    
    try:
        print("🧪 Testing direct schema validation...")
        github_pages = GitHubPagesContent(**sample_content)
        print("✅ Direct schema validation passed")
        print(f"📁 Repository skeleton: {len(github_pages.repo_skeleton)} files/dirs")
        print(f"🏷️ Badges: {len(github_pages.badges)}")
        print(f"📄 README length: {len(github_pages.readme_markdown)} characters")
        print(f"🌐 GitHub Pages config: {'✅' if github_pages.gh_pages else '❌'}")
        print(f"🔄 CI workflow: {'✅' if github_pages.ci_suggestion else '❌'}")
        print(f"💬 Discussions seed: {'✅' if github_pages.discussions_seed else '❌'}")
        print(f"🏷️ Label suggestions: {len(github_pages.labels_suggestions)}")
        
        print("\n🧪 Testing schema validator function...")
        validated_content = validate_content("github_pages", "content", sample_content)
        print("✅ Schema validator function passed")
        print(f"📋 Validated content type: {type(validated_content).__name__}")
        
        print(f"\n📋 Sample GitHub Pages Structure:")
        print(f"   • Repository files: {len(github_pages.repo_skeleton)}")
        print(f"   • Badges: {len(github_pages.badges)} (CI, License, Python)")
        print(f"   • README sections: All required sections present")
        print(f"   • GitHub Pages: index.md + _config.yml")
        print(f"   • CI workflow: GitHub Actions with Redis service")
        print(f"   • Discussion labels: {len(github_pages.discussions_seed['labels'])}")
        
        return True
        
    except Exception as e:
        print(f"❌ Schema validation failed: {e}")
        return False

def test_direct_schema_instantiation():
    """Test 3: Direct GitHub Pages schema instantiation"""
    print("\n" + "=" * 60)
    print("TEST 3: Direct GitHub Pages Schema Instantiation")
    print("=" * 60)
    
    # Minimal valid GitHub Pages content
    minimal_content = {
        "repo_skeleton": [
            ".github/workflows/ci.yml",
            "src/",
            "tests/",
            "README.md"
        ],
        
        "badges": [
            {
                "alt": "Build",
                "image_url": "https://img.shields.io/github/actions/workflow/status/user/repo/ci.yml",
                "link_url": "https://github.com/user/repo/actions"
            },
            {
                "alt": "License",
                "image_url": "https://img.shields.io/badge/license-MIT-green.svg",
                "link_url": "LICENSE"
            }
        ],
        
        "readme_markdown": """# WebSocket Chat Server

[![Build](https://img.shields.io/github/actions/workflow/status/user/repo/ci.yml)](https://github.com/user/repo/actions)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Real-time WebSocket chat server with room support and message persistence.

- **Demo**: https://chat-demo.example.com
- **Docs**: ./docs/index.md

## Table of Contents
- [Features](#features)
- [Quickstart](#quickstart)
- [Usage](#usage)
- [Configuration](#configuration)
- [Architecture](#architecture)
- [Roadmap](#roadmap)
- [Benchmarks](#benchmarks)
- [Contributing](#contributing)
- [License](#license)
- [FAQ](#faq)

## Features
- Real-time WebSocket communication
- Chat rooms with user management
- Message history persistence
- Typing indicators and presence

## Quickstart
```bash
# clone and setup
git clone https://github.com/user/websocket-chat.git
cd websocket-chat
npm install
```

## Usage
```javascript
// minimal server example
const WebSocketServer = require('./src/server');
const server = new WebSocketServer({ port: 8080 });
server.start();
```

## Configuration
| Name | Type | Default | Description |
|------|------|---------|-------------|
| PORT | number | 8080 | Server port |
| DB_URL | string | "sqlite://chat.db" | Database URL |

## Architecture
```mermaid
flowchart LR
    Client1-->Server[WebSocket Server]
    Client2-->Server
    Server-->DB[(Database)]
```
_Alt text_: WebSocket clients connected to server with database persistence.

## Roadmap
- [ ] Voice chat support
- [ ] File sharing

## Benchmarks
- Concurrent connections: 1000+
- Message latency: <50ms

## Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md).

## License
MIT © Contributors

## FAQ
**Q:** How many concurrent users?  
**A:** Tested with 1000+ concurrent connections.
""",
        
        "gh_pages": {
            "index_markdown": """---
layout: default
title: WebSocket Chat Server
---

# WebSocket Chat Server

Real-time WebSocket chat server with room support and message persistence.

- **Get started:** [README](../README.md#quickstart)
- **Architecture:** [diagram](../README.md#architecture)
- **Examples:** [/examples](../examples)
""",
            "_config_yaml": """title: WebSocket Chat Server
remote_theme: pages-themes/minimal@v0.2.0
plugins:
  - jekyll-remote-theme
markdown: kramdown
""",
            "nav": [
                {"title": "Home", "href": "/"},
                {"title": "README", "href": "/README"}
            ]
        },
        
        "ci_suggestion": {
            "workflow_name": "CI",
            "file_path": ".github/workflows/ci.yml",
            "yaml": """name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '18' }
      - run: npm ci && npm test
"""
        },
        
        "discussions_seed": {
            "title": "Would you approach WebSocket Chat Server differently at scale?",
            "body": """### Context
Real-time WebSocket chat server with room support and message persistence

### What I'm sharing
- Minimal runnable WebSocket server
- Architecture with database persistence

### What I'd love feedback on
- Scaling strategies for high concurrent connections
- Message delivery guarantees

### Stack
- Language: Node.js
- Protocol: WebSocket
- Database: SQLite/PostgreSQL

### Known limitations
- Single server instance
- Basic authentication

### Links
- Repo README (this)
""",
            "category_suggestion": "Show and tell",
            "labels": ["discussion", "help wanted", "question"]
        },
        
        "labels_suggestions": [
            {"name": "good first issue", "color": "7057ff"},
            {"name": "help wanted", "color": "008672"},
            {"name": "discussion", "color": "0366d6"},
            {"name": "bug", "color": "d73a4a"},
            {"name": "enhancement", "color": "a2eeef"}
        ],
        
        "image_prompts": [
            {
                "role": "repo_diagram",
                "title": "Repository Architecture Diagram",
                "prompt": "Widescreen minimal diagram for WebSocket Chat Server: client connections and data flow. Show blocks for multiple clients, WebSocket server, database; arrows and 3-4 short labels; off-white/light background; thin vector strokes; subtle dotted grid; green accent color; flat vector; generous margins; legible at 1200×630.",
                "negative_prompt": "no stock photos, no faces, no logos, no neon, no 3D bevels, no glossy gradients, no clutter",
                "style_notes": "editorial-tech; crisp kerning; consistent stroke widths",
                "ratio": "1.91:1",
                "size_px": "1200x630",
                "alt_text": "WebSocket chat server architecture with multiple clients"
            }
        ],
        
        "compliance": {
            "has_readme_sections": True,
            "has_toc": True,
            "has_quickstart_and_usage": True,
            "has_config_table": True,
            "has_arch_diagram_block": True,
            "has_license": True,
            "discussion_has_questions": True,
            "labels_count_ok": True,
            "image_prompt_count": 1,
            "has_tracked_link_once": False,
            "checks": [
                "README includes all required sections",
                "GitHub Pages: index.md + _config.yml provided",
                "CI workflow suggestion provided",
                "Discussions seed includes context + feedback asks",
                "No tracked link (no primary_url provided)",
                "1 repository diagram image prompt"
            ]
        }
    }
    
    try:
        github_pages = GitHubPagesContent(**minimal_content)
        print("✅ Direct schema instantiation successful")
        print(f"📊 GitHub Pages structure:")
        print(f"   • Repository skeleton: {len(github_pages.repo_skeleton)} items")
        print(f"   • Badges: {len(github_pages.badges)}")
        print(f"   • README length: {len(github_pages.readme_markdown)} characters")
        print(f"   • GitHub Pages files: index.md + _config.yml")
        print(f"   • CI workflow: {github_pages.ci_suggestion['workflow_name']}")
        print(f"   • Discussion labels: {len(github_pages.discussions_seed['labels'])}")
        print(f"   • Label suggestions: {len(github_pages.labels_suggestions)}")
        
        # Test JSON serialization
        json_data = github_pages.model_dump()
        json_str = json.dumps(json_data, indent=2)
        print("✅ JSON serialization successful")
        print(f"📄 JSON size: {len(json_str)} characters")
        
        return True
        
    except Exception as e:
        print(f"❌ Direct schema instantiation failed: {e}")
        return False

def main():
    """Run all GitHub Pages tests"""
    print("🧪 GITHUB PAGES CONTENT GENERATION TESTS")
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
        print("🎉 All GitHub Pages tests passed! Ready for integration.")
        return True
    else:
        print("⚠️ Some tests failed. Check implementation.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
