# System Design Topic Generator

A Python client for generating comprehensive system design topics using Google's Gemini 2.5 Flash API with structured JSON output and SQLite database storage.

## Features

- **Structured Output**: Uses Gemini's `response_schema` feature to guarantee JSON format
- **Parallel Processing**: Process multiple topics simultaneously using parallel API calls (5 topics per call, up to 10 concurrent calls)
- **SQLite Storage**: Automatic database storage with comprehensive schema
- **API Key Rotation**: Supports multiple API keys with automatic rotation
- **Schema Validation**: Validates responses against a comprehensive JSON schema
- **Cross-linking**: Automatically links related topics using topic IDs
- **Rate Limiting**: Built-in delays to avoid API rate limits
- **Error Handling**: Robust error handling with detailed error messages
- **Database Management**: CLI tools for database operations and statistics

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up API Keys

Configure your Google AI API keys in `config.py`:

```python
API_KEYS = [
    "AIzaSyCO67rfGWXzxeQSqoupwezNw2RiaMxU5nI",
    "AIzaSyAbP9xIxVVGOQSqp1AxwF0ocCT1c9iRGnU",
    "AIzaSyBTE1iv1_jTMvUNbe-hSSwVA-oqqbiTcHc",
    "AIzaSyBNxuGnXwjcGZOerUMbXuHBJ4lppFk3vos",
    "AIzaSyBFLtr-pr_F1Tl0m013ZkZF14i7ruZ4Emo",
    "AIzaSyCqqid5Vci-ScNNNSKowk55tREJQrvPjN8",
    "AIzaSyCAi57XAKoI376KJEc9iwZZ4w-5e8m46xo"
]
```

Or set a single key as an environment variable:

```bash
export GOOGLE_AI_API_KEY="your-api-key-here"
```

### 3. Run the Generator

```bash
# Process all topics from topics.json (saves to database + JSON files)
python batch_processor.py topics.json

# Save only to database (skip JSON files)
python batch_processor.py topics.json --db-only

# Custom database path
python batch_processor.py topics.json --db-path my_topics.db

# Custom output directory and batch size
python batch_processor.py topics.json --output-dir my_topics --batch-size 3

# With custom dates
python batch_processor.py topics.json --created-date "2024-01-15" --updated-date "2024-01-15"
```

## Usage

### Command Line Interface

```bash
python batch_processor.py topics.json [OPTIONS]

Options:
  --output-dir DIR      Directory to save generated topics (default: output)
  --batch-size N        Number of topics per API call, max 5 (default: 5)
  --created-date DATE   Creation date in YYYY-MM-DD format
  --updated-date DATE   Update date in YYYY-MM-DD format
  --delay SECONDS       Delay between API calls (default: 1.0)
  --api-keys KEY...     Google AI API keys for rotation (or use config.py)
  --db-path PATH        Path to SQLite database file (default: topics.db)
  --db-only             Save only to database, skip JSON files
```

### Web Interface

The system includes a beautiful, modern web interface for easy topic management:

### Features

- **Bulk Topic Entry**: Enter multiple topics at once with real-time processing
- **Progress Tracking**: Live updates on processing status with visual progress bars
- **Topic Management**: View, filter, search, and manage all generated topics
- **Analytics Dashboard**: Comprehensive insights with interactive charts
- **Real-time Updates**: WebSocket-powered live status updates
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile

### Starting the Web Interface

```bash
# Install additional web dependencies
pip install -r requirements.txt

# Start the web application
python app.py
```

Then open your browser to `http://localhost:5000`

### Web Interface Pages

1. **Dashboard** (`/`) - Main page with bulk topic entry and overview
2. **Topics** (`/topics`) - Browse and manage all topics with filtering
3. **Analytics** (`/analytics`) - Detailed analytics with interactive charts

### Web API Endpoints

- `POST /api/topics` - Create topics from bulk input
- `GET /api/status` - Get current processing status
- `GET /api/topics/<id>` - Get specific topic details
- `POST /api/topics/<id>/retry` - Retry failed topic processing
- `GET /api/stats` - Get database statistics

### Database Management (CLI)

```bash
# Show database statistics
python db_manager.py stats

# List recent topics
python db_manager.py list --limit 20

# List topics by category
python db_manager.py list --category system_design

# Show detailed topic information
python db_manager.py show 101

# Search topics
python db_manager.py search "WhatsApp"

# Export all topics to JSON
python db_manager.py export --output all_topics.json
```

## Input Format

Your `topics.json` file should contain an array of topic objects:

```json
[
  {
    "id": 101,
    "title": "How WhatsApp Group Calls Scale to Dozens"
  },
  {
    "id": 102,
    "title": "How Redis Internally Works"
  }
]
```

## Output Format

Each generated topic follows this comprehensive schema:

```json
{
  "id": 101,
  "title": "How WhatsApp Group Calls Scale to Dozens",
  "description": "Detailed explanation of WhatsApp's group call architecture...",
  "category": "system_design",
  "subcategory": "real_time_communication",
  "company": "whatsapp",
  "technologies": ["WebRTC", "SFU", "Kubernetes", "Redis"],
  "complexity_level": "advanced",
  "tags": ["webrtc", "scaling", "real-time", "group-calls"],
  "related_topics": [102, 103],
  "metrics": {
    "scale": "Millions of concurrent group calls",
    "performance": "Sub-200ms latency",
    "reliability": "99.9% uptime",
    "latency": "150ms average"
  },
  "implementation_details": {
    "architecture": "SFU-based WebRTC architecture",
    "scaling": "Horizontal scaling with load balancers",
    "storage": "Redis for session management",
    "caching": "CDN for media content",
    "monitoring": "Real-time metrics and alerting"
  },
  "learning_objectives": [
    "Understand WebRTC architecture",
    "Learn SFU scaling patterns",
    "Master real-time communication design"
  ],
  "difficulty": 7,
  "estimated_read_time": "15 minutes",
  "prerequisites": ["WebRTC basics", "Distributed systems"],
  "created_date": "2024-01-15",
  "updated_date": "2024-01-15"
}
```

## Database Schema

The SQLite database includes two main tables:

### `topics` Table
- **id**: Primary key (topic ID)
- **title**: Topic title
- **description**: Detailed description
- **category**: System design category
- **subcategory**: Specific subcategory
- **company**: Company name (snake_case)
- **technologies**: JSON array of technologies
- **complexity_level**: beginner/intermediate/advanced/expert
- **tags**: JSON array of tags
- **related_topics**: JSON array of related topic IDs
- **metrics**: JSON object with scale/performance/reliability/latency
- **implementation_details**: JSON object with architecture details
- **learning_objectives**: JSON array of learning goals
- **difficulty**: Integer 1-10
- **estimated_read_time**: Reading time estimate
- **prerequisites**: JSON array of prerequisites
- **created_date**: Creation date (ISO format)
- **updated_date**: Update date (ISO format)
- **generated_at**: Timestamp when topic was generated

### `processing_log` Table
- **id**: Auto-increment primary key
- **batch_id**: Batch identifier for tracking
- **topic_id**: Foreign key to topics table
- **status**: success/failed/skipped
- **error_message**: Error details if failed
- **processed_at**: Processing timestamp

## Categories

The system supports these predefined categories:
- `big_tech_companies` - FAANG company system designs
- `databases` - Database design and optimization
- `system_design` - General system architecture
- `cloud_infrastructure` - Cloud-native solutions
- `security` - Security-focused designs
- `ai_ml` - AI/ML system architectures
- `networking` - Network protocols and design
- `algorithms` - Algorithmic system components
- `messaging_streaming` - Real-time messaging and streaming

## Complexity Levels

- `beginner` - Basic concepts, suitable for new developers
- `intermediate` - Moderate complexity, requires some experience
- `advanced` - Complex systems, requires strong technical background
- `expert` - Highly complex, requires deep domain expertise

## Error Handling

The system includes comprehensive error handling:

- **API Errors**: Network failures, rate limiting, invalid responses
- **Validation Errors**: Schema validation failures
- **File Errors**: Missing files, invalid JSON format
- **Configuration Errors**: Missing API keys, invalid parameters
- **Database Errors**: Connection issues, constraint violations

## Rate Limiting

The system includes built-in rate limiting with configurable delays between API calls to avoid hitting Google's rate limits. With multiple API keys configured, the system automatically rotates keys when rate limits are encountered.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Support

For issues and questions:
1. Check the error messages for specific guidance
2. Verify your API key is correctly set
3. Ensure your topics.json format is valid
4. Check Google AI API status and quotas
