# Fixing Stuck Topics Issue

## Problem
Topics can get stuck in 'processing' status if:
- Worker crashes during processing
- Process is killed (Ctrl+C)
- Server restarts
- Network issues during Gemini API calls

## Immediate Fix

Run the fix script to reset stuck topics:

```bash
python3 fix_stuck_topics.py
```

This will:
1. Show all stuck topics
2. Ask for confirmation
3. Reset them to 'pending' status
4. They'll be processed again on next worker run

## Prevention: Add Timeout Mechanism

### Option 1: Add processing timeout check in worker

In `worker_service.py`, add a method to check for stale processing topics:

```python
def reset_stale_processing_topics(self, timeout_minutes=30):
    """Reset topics stuck in processing for too long."""
    timeout_time = datetime.now() - timedelta(minutes=timeout_minutes)
    
    conn = self.db.get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        UPDATE topic_status
        SET status = 'pending'
        WHERE status = 'processing'
        AND created_at < ?
    """, (timeout_time.isoformat(),))
    
    if cursor.rowcount > 0:
        logger.info(f"Reset {cursor.rowcount} stale processing topics to pending")
    
    conn.commit()
    conn.close()
```

Call this before processing:
```python
# In process_pending_topics method
self.reset_stale_processing_topics()
```

### Option 2: Add last_updated timestamp

Modify the topic_status table to track when status was last updated:

```sql
ALTER TABLE topic_status ADD COLUMN last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

-- Update trigger for SQLite
CREATE TRIGGER update_topic_status_timestamp 
AFTER UPDATE ON topic_status
BEGIN
    UPDATE topic_status SET last_updated = CURRENT_TIMESTAMP 
    WHERE rowid = NEW.rowid;
END;
```

### Option 3: Graceful shutdown handler

In `worker_service.py`, reset processing topics on shutdown:

```python
def stop(self):
    """Stop the worker gracefully."""
    logger.info("Stopping TopicWorker...")
    self.is_running = False
    
    # Reset any topics this worker was processing
    conn = self.db.get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE topic_status
        SET status = 'pending'
        WHERE status = 'processing'
    """)
    if cursor.rowcount > 0:
        logger.info(f"Reset {cursor.rowcount} processing topics to pending on shutdown")
    conn.commit()
    conn.close()
    
    logger.info("TopicWorker stopped")
```

## Best Practices

1. **Always use try/finally blocks** when updating status:
```python
try:
    db.save_topic_status(title, 'processing', None)
    # Process topic
    db.save_topic_status(title, 'completed', None)
except Exception as e:
    db.save_topic_status(title, 'failed', str(e))
finally:
    # Ensure status is never left as 'processing'
    pass
```

2. **Monitor stuck topics** regularly:
```bash
# Check for stuck topics
sqlite3 unified.db "SELECT status, COUNT(*) FROM topic_status WHERE status IN ('processing', 'in_progress') GROUP BY status;"
```

3. **Add health checks** to worker to detect and fix stuck topics automatically

## Status Flow Summary

```
pending → processing → completed ✅
    ↓         ↓          ↓
  (waiting) (active)  (success)
              ↓
           failed ❌
          (on error)
              ↓
         [timeout?]
              ↓
         pending ♻️
        (retry)
```


