# Content Generation Service - Local Setup

A simple, local-only FastAPI service that generates multi-platform content using Gemini 2.5 Flash.

## Features

- **Multi-Platform Content**: Generate content for 20+ social media platforms
- **Parallel Processing**: Up to 6 concurrent API calls for faster generation
- **Strict JSON Validation**: All responses validated against platform-specific schemas
- **Caching**: Intelligent caching to avoid duplicate API calls
- **Image Prompts**: Generate Nano Banana-ready image prompts
- **Local Only**: No external dependencies, runs entirely locally

## Quick Start

### 1. Install Dependencies

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install fastapi uvicorn httpx pydantic python-dotenv
```

### 2. Environment Setup

```bash
# Copy environment template
cp env.example .env

# Edit .env and add your Gemini API key
GEMINI_API_KEY=your_actual_api_key_here
```

### 3. Run the Service

```bash
# Start the development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The service will be available at:
- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/docs
- **Health**: http://localhost:8000/api/health

## API Usage

### Generate Content for Multiple Platforms

```bash
curl -X POST "http://localhost:8000/api/content/generate-all" \
  -H "Content-Type: application/json" \
  -d '{
    "topicId": "t-001",
    "topicName": "How WhatsApp group calls scale",
    "topicDescription": "Signaling, SFU/MCU trade-offs, backpressure...",
    "audience": "intermediate",
    "tone": "clear, confident, non-cringe",
    "locale": "en",
    "primaryUrl": "https://example.com/whatsapp-scale",
    "brand": {
      "siteUrl": "https://example.com",
      "handles": {
        "instagram": "@anshul",
        "x": "@anshul",
        "linkedin": "anshul",
        "youtube": "anshul",
        "github": "anshul"
      },
      "utmBase": "utm_source={platform}&utm_medium=social&utm_campaign=whatsapp-calls"
    },
    "targetPlatforms": [
      "instagram:carousel",
      "x_twitter:thread",
      "youtube:long_form"
    ],
    "options": {
      "include_images": true,
      "max_length_levels": "standard",
      "force": false
    }
  }'
```

### Generate Content for Single Platform

```bash
curl -X POST "http://localhost:8000/api/content/instagram/carousel" \
  -H "Content-Type: application/json" \
  -d '{
    "topicId": "t-001",
    "topicName": "How WhatsApp group calls scale",
    "topicDescription": "Signaling, SFU/MCU trade-offs, backpressure...",
    "audience": "intermediate",
    "tone": "clear, confident, non-cringe",
    "locale": "en",
    "primaryUrl": "https://example.com/whatsapp-scale",
    "brand": {
      "siteUrl": "https://example.com",
      "handles": {
        "instagram": "@anshul",
        "x": "@anshul",
        "linkedin": "anshul",
        "youtube": "anshul",
        "github": "anshul"
      },
      "utmBase": "utm_source={platform}&utm_medium=social&utm_campaign=whatsapp-calls"
    },
    "options": {
      "include_images": true,
      "max_length_levels": "standard",
      "force": false
    }
  }'
```

## Supported Platforms

### Instagram
- `instagram:reel` - Short-form video content
- `instagram:carousel` - Multi-slide posts
- `instagram:story` - Story format content
- `instagram:post` - Single image posts

### LinkedIn
- `linkedin:post` - Professional posts
- `linkedin:carousel` - Multi-slide professional content

### X/Twitter
- `x_twitter:thread` - Thread format content

### YouTube
- `youtube:short` - Short-form video content
- `youtube:long_form` - Long-form video scripts

### Other Platforms
- `threads:post` - Meta's Threads platform
- `facebook:post` - Facebook posts
- `medium:article` - Medium articles
- `substack:newsletter` - Substack newsletters
- `reddit:post` - Reddit posts
- `hacker_news:item` - Hacker News submissions
- `devto:article` - Dev.to articles
- `hashnode:article` - Hashnode articles
- `github_pages:content` - GitHub Pages content
- `notion:page` - Notion pages
- `personal_blog:post` - Personal blog posts
- `ghost:post` - Ghost CMS posts
- `telegram:post` - Telegram channel posts

## Project Structure

```
app/
├── main.py                 # FastAPI application entry point
├── routes_orchestrator.py # Orchestrator endpoints
├── routes_platform.py     # Platform-specific endpoints
├── service_tasks.py       # Task management and execution
├── gemini_client.py       # Gemini API client
├── schemas.py            # Pydantic models and validation
├── store.py              # Database and cache management
└── prompts/
    ├── header.txt        # Global prompt header
    └── bodies/           # Platform-specific prompt templates
        ├── ig-carousel.txt
        ├── x-thread.txt
        └── yt-long.txt

data/
├── app.db               # SQLite database
└── cache/               # Cached results
    └── {hash}.json      # Cached content files
```

## Configuration

### Environment Variables

- `GEMINI_API_KEY` - Your Gemini API key (required)
- `IMAGE_TOOL_NAME` - Image generation tool name (default: "nano-banana")
- `MAX_CONCURRENT_TASKS` - Maximum parallel tasks (default: 6)
- `GEMINI_TIMEOUT` - API timeout in seconds (default: 30)
- `GEMINI_MAX_RETRIES` - Maximum retry attempts (default: 1)

### Database

The service uses SQLite for local storage:
- **Jobs**: Track generation jobs and their status
- **Tasks**: Individual platform generation tasks
- **Results**: Generated content and metadata
- **Prompts**: Prompt templates and versions

### Caching

Content is cached using SHA256 fingerprints:
- **Key**: `SHA256(topicTitle|platform|format|promptVersion)`
- **Location**: `./data/cache/{hash}.json`
- **Reuse**: Cached content is reused unless `force=true`

## Development

### Adding New Platforms

1. **Add Platform Schema**: Update `schemas.py` with new content model
2. **Create Prompt Template**: Add `{platform}-{format}.txt` in `prompts/bodies/`
3. **Update Validation**: Add platform to validation switch
4. **Add Route**: Add endpoint in `routes_platform.py`

### Testing

```bash
# Test health endpoint
curl http://localhost:8000/api/health

# Test single platform
curl -X POST "http://localhost:8000/api/content/instagram/carousel" \
  -H "Content-Type: application/json" \
  -d @examples/sample_request.json
```

## Troubleshooting

### Common Issues

1. **Missing API Key**: Ensure `GEMINI_API_KEY` is set in `.env`
2. **Database Errors**: Delete `./data/app.db` to reset database
3. **Cache Issues**: Clear `./data/cache/` directory
4. **Port Conflicts**: Change port with `--port 8001`

### Logs

The service logs to console with timestamps. Check for:
- API call failures
- Validation errors
- Database connection issues
- Cache read/write problems

## Performance

- **Concurrency**: Up to 6 parallel API calls
- **Caching**: Reduces API calls for repeated content
- **Validation**: Fast JSON schema validation
- **Database**: Lightweight SQLite for local storage

## Security

- **Input Validation**: All inputs validated against schemas
- **Prompt Guards**: Basic PII/secrets filtering
- **Rate Limiting**: Built into Gemini client
- **Local Only**: No external network dependencies
