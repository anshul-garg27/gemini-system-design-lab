# Decoupled Topic Processing Worker System

## Overview

The topic processing system has been decoupled from the API endpoints to provide better scalability, reliability, and visibility into processing status. Instead of processing topics synchronously during API calls, topics are now:

1. **Saved to database** with "pending" status when submitted
2. **Processed by workers** that poll the database for pending topics
3. **Updated with status** (processing, completed, or failed) as they progress

## Architecture

```
Frontend → API → Database (pending) → Worker Service → Gemini API
                     ↓                      ↓
                Topic Status           Update Status
                  Table               (processing/completed/failed)
```

### Status Flow
```
pending → processing → completed
                   ↘ failed
```

1. **Pending**: Topic submitted, waiting to be processed
2. **Processing**: Worker picked up topic, currently generating content
3. **Completed**: Successfully processed and saved
4. **Failed**: Processing failed with error

## Key Components

### 1. API Endpoints

- **POST /api/v1/topics** - Saves topics with "pending" status
- **GET /api/v1/processing-status** - Returns current processing status
- **GET /api/v1/worker-status** - Checks if worker is running
- **GET /api/v1/topic-status-summary** - Detailed status breakdown

### 2. Worker Service (`app/worker_service.py`)

- Polls database every 10 seconds (configurable)
- Fetches limited number of pending topics (max 30 at a time)
- Calls `process_topics_background` function from routes_topics.py
- Topics are updated to 'processing' status when picked up
- Reuses all existing processing logic including parallel batch processing
- Waits for processing to complete before next poll

### 3. Database Tables

- **topics** - Stores generated topic data
- **topic_status** - Tracks processing status of each topic
  - `pending` - Waiting to be processed
  - `processing` - Currently being processed
  - `completed` - Successfully processed
  - `failed` - Processing failed (with error message)

## How to Use

### 1. Start the FastAPI Server

```bash
python start_unified_server.py
```

### 2. Start the Worker Service

In a separate terminal:

```bash
python run_worker.py
```

#### Worker Configuration

Configure via environment variables:

```bash
# Number of topics per Gemini API call (default: 5, max: 5)
export WORKER_BATCH_SIZE=5

# Seconds between database polls (default: 10)
export WORKER_POLL_INTERVAL=10

python run_worker.py
```

Note: The worker uses `process_topics_background` which handles its own parallel processing internally.

### 3. Submit Topics

Topics can be submitted via:

1. **API Call**:
```bash
curl -X POST http://localhost:8000/api/v1/topics \
  -H "Content-Type: application/json" \
  -d '{
    "topics": [
      "How Netflix Handles Video Streaming",
      "Building a Real-time Chat System"
    ],
    "batch_size": 5
  }'
```

2. **Frontend**: Use the existing web interface

### 4. Monitor Progress

1. **Check Processing Status**:
```bash
curl http://localhost:8000/api/v1/processing-status
```

Returns:
```json
{
  "is_processing": true,
  "pending_count": 5,
  "processing_count": 2,
  "completed_count": 10,
  "failed_count": 1,
  "total_count": 18,
  "recent_failures": [...],
  "show_status": true
}
```

2. **Check Worker Status**:
```bash
curl http://localhost:8000/api/v1/worker-status
```

3. **Use Test Script**:
```bash
python test_decoupled_system.py
```

## Benefits

1. **Scalability**: Can run multiple workers to process topics faster
2. **Reliability**: Failed topics are tracked and can be retried
3. **Visibility**: Real-time status of all topics in the system
4. **Decoupling**: API responds immediately without waiting for processing
5. **Fault Tolerance**: If worker crashes, topics remain pending and can be reprocessed

## Frontend Integration

The frontend can show processing status by:

1. Polling `/api/v1/processing-status` endpoint
2. Displaying status bar when `show_status` is true
3. Showing counts of pending/processing/completed/failed topics
4. Listing recent failures for transparency

Example frontend logic:
```javascript
// Poll for status every 5 seconds
setInterval(async () => {
  const response = await fetch('/api/v1/processing-status');
  const status = await response.json();
  
  if (status.show_status) {
    // Show status bar with counts
    updateStatusBar(status);
  } else {
    // Hide status bar
    hideStatusBar();
  }
}, 5000);
```

## Handling Failures

Failed topics are tracked with error messages in the database:

1. **View Failed Topics**:
```bash
curl http://localhost:8000/api/v1/processing-status
```

2. **Retry Failed Topic**:
```bash
curl -X POST http://localhost:8000/api/v1/topics/123/retry
```

3. **Clean Up Failed Topics**:
```bash
curl -X POST http://localhost:8000/api/v1/cleanup-failed
```

## Best Practices

1. **Monitor Worker Health**: Check worker logs for errors
2. **Set Appropriate Batch Size**: 5 topics per batch works well with Gemini
3. **Handle Rate Limits**: Worker includes delays between batches (handled by process_topics_background)
4. **Clean Up Periodically**: Remove old failed topics to keep DB clean
5. **Single Worker Instance**: Run only one worker instance since process_topics_background handles parallel processing internally
6. **Efficient Fetching**: Worker only fetches as many topics as it can process concurrently (max 30)

## Troubleshooting

### Worker Not Processing Topics

1. Check if worker is running: `ps aux | grep worker_service`
2. Check worker logs for errors
3. Verify database connectivity
4. Check Gemini API keys are valid

### Topics Stuck in "Processing"

This can happen if worker crashes during processing:

1. Restart the worker
2. Topics will timeout and can be reprocessed
3. Or manually update status in database

### High Failure Rate

1. Check worker logs for specific errors
2. Verify Gemini API quotas
3. Check network connectivity
4. Review failed topic error messages in database

## Migration Notes

The system maintains backward compatibility:
- Existing completed topics are preserved
- Failed topics can be retried
- Frontend continues to work with minimal changes
- Same topic generation logic and prompts
