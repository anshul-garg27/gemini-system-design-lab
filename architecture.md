# Content Generation Service Architecture

## Overview
A simple, local-only FastAPI service that generates multi-platform content using Gemini 2.5 Flash. The service orchestrates parallel content generation across multiple social media platforms and formats.

## Core Flow

### 1. Content Generation Request
```
POST /api/content/generate-all
├── Validates input schema
├── Creates job record in SQLite
├── Spawns parallel subtasks (max 6 concurrent)
└── Returns job ID immediately
```

### 2. Parallel Task Execution
```
For each (platform, format) combination:
├── Generate cache fingerprint: SHA256(topicTitle|platform|format|promptVersion)
├── Check cache (if force=false)
├── If not cached:
│   ├── Build prompt = GLOBAL_HEADER + PLATFORM_BODY
│   ├── Call Gemini 2.5 Flash with strict JSON instruction
│   ├── Validate response against platform schema
│   ├── Cache normalized JSON
│   └── Update task status
└── Return validated envelope
```

### 3. Result Aggregation
```
GET /api/results/{jobId}
├── Collect all completed tasks
├── Merge results into unified response
├── Include any errors
└── Return final JSON
```

## Data Model

### SQLite Tables
- **jobs**: `(id, created_at, status, topic_id, topic_name)`
- **tasks**: `(id, job_id, platform, format, status, cached, started_at, finished_at, error)`
- **results**: `(task_id, raw_response, normalized_json)`
- **prompts**: `(task_id, platform, format, prompt_version, body)`

### Cache Strategy
- **Location**: `./data/cache/{fingerprint}.json`
- **Fingerprint**: `SHA256(topicTitle|platform|format|promptVersion)`
- **Reuse**: Unless `force=true`, cached results are returned immediately

## Concurrency Model
- **Max Parallel Tasks**: 6 (configurable)
- **Implementation**: `asyncio.gather()` with semaphore
- **Error Handling**: Individual task failures don't stop others
- **Retry Logic**: 1 retry with "return valid JSON only" correction

## Validation Pipeline
1. **Request Validation**: Pydantic models for input
2. **Response Validation**: Platform-specific schemas
3. **Envelope Validation**: Common meta + platform content
4. **Error Recovery**: Re-prompt with JSON-only instruction

## Platform Support
- **Instagram**: reel, carousel, story, post
- **LinkedIn**: post, carousel  
- **X/Twitter**: thread
- **YouTube**: short, long_form
- **Threads**: post
- **Facebook**: post
- **Medium**: article
- **Substack**: newsletter
- **Reddit**: post
- **Hacker News**: item
- **Dev.to**: article
- **Hashnode**: article
- **GitHub Pages**: content
- **Notion**: page
- **Personal Blog**: post
- **Ghost**: post
- **Telegram**: post

## API Endpoints

### Orchestrator Routes
- `POST /api/content/generate-all` - Generate content for multiple platforms
- `GET /api/jobs/{jobId}` - Check job status
- `GET /api/results/{jobId}` - Get final results
- `POST /api/content/regenerate` - Re-run specific platforms

### Per-Platform Routes
- `POST /api/content/{platform}/{format}` - Generate for specific platform
- `POST /api/content/{platform}-{format}` - Alias format

### Utility Routes
- `GET /api/health` - Health check

## Security & Safety
- **Prompt Guards**: Strip PII/secrets, max length limits
- **Input Validation**: All inputs validated against schemas
- **Rate Limiting**: Built into Gemini client (30s timeout, 1 retry)
- **Error Isolation**: Failed tasks don't affect others

## Deployment
- **Local Only**: No Docker, Redis, or external services
- **Start Command**: `uvicorn app.main:app --reload`
- **Dependencies**: FastAPI, httpx, pydantic, sqlite3
- **Data Directory**: `./data/` (auto-created)
