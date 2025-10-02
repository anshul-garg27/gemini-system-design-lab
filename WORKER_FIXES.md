# Worker System Fixes

## Issues Fixed

### 1. Pending Count Not Decreasing

**Problem**: When topics moved from pending to completed, the pending count wasn't decreasing.

**Root Cause**: Topics were never being updated to 'processing' status. They jumped directly from 'pending' to 'completed' or 'failed'.

**Fix**: Added status update to 'processing' in `process_single_batch` function:
```python
# Update status to processing for all topics in this batch
for topic in batch:
    db.save_topic_status(topic['title'], 'processing', None)
```

Now the flow is:
1. Topic added → Status: `pending` 
2. Worker picks it up → Status: `processing` (pending count decreases)
3. Processing completes → Status: `completed` or `failed`

### 2. Fetching Too Many Topics at Once

**Problem**: Worker was fetching ALL pending topics from the database, even if there were thousands.

**Root Cause**: No limit was being applied when fetching pending topics.

**Fix**: 
- Added limit to fetch only as many topics as can be processed concurrently
- Conservative limit of 30 topics max per fetch (can process 6 batches of 5 topics each)

```python
# Calculate how many topics to fetch
max_concurrent_topics = min(30, 10 * self.batch_size)  # Max 30 topics at once

# Get limited pending topic titles  
pending_titles = self.get_pending_topics(limit=max_concurrent_topics)
```

## Benefits

1. **Better Memory Usage**: Only loads topics that can be actively processed
2. **Accurate Status Counts**: Frontend now shows correct pending/processing/completed counts
3. **Better Performance**: Database queries are limited and more efficient
4. **Fair Processing**: If multiple workers run, they won't all grab the same topics

## Status Flow

```
pending (1814) → processing (5) → completed (2719)
                              ↘ failed (15)
```

When worker picks up topics:
- Pending: 1814 → 1809 (5 moved to processing)
- Processing: 0 → 5
- Completed: stays same until processing finishes

## Configuration

You can adjust the concurrent processing limit:

```python
# In worker_service.py
max_concurrent_topics = min(30, 10 * self.batch_size)  # Change 30 to your preferred max
```

Lower values = less memory usage, more database polls
Higher values = more memory usage, fewer database polls


