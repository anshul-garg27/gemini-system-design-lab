# Topic Status Foreign Key Fix

## 🐛 Problem

**Error**: `sqlite3.IntegrityError: FOREIGN KEY constraint failed`

The `topic_status` table had an incorrect foreign key constraint:
```sql
FOREIGN KEY (id) REFERENCES topics(id) ON DELETE CASCADE
```

This caused failures because:
1. **Workflow**: Topics are created in `topic_status` with status='pending' BEFORE being processed
2. **FK Constraint**: The `id` in `topic_status` must exist in `topics.id`
3. **Issue**: At creation time, the topic doesn't exist in `topics` yet (it's added after Gemini generates it)

## ✅ Solution

**Date**: 2025-10-01

Removed the foreign key constraint from `topic_status` table since:
- `topic_status` is a queue/tracking table for topics to be processed
- Topics are inserted BEFORE they exist in the `topics` table
- The `original_title` field serves as the logical link (not a database FK)

### Changes Made

1. **Removed FK constraint** from `topic_status.id -> topics.id`
2. **Added UNIQUE constraint** on `original_title` to prevent duplicates
3. **Updated schema** in `unified_database.py`

### New Schema

```sql
CREATE TABLE topic_status (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    original_title TEXT NOT NULL UNIQUE,  -- Added UNIQUE
    current_title TEXT,
    status TEXT NOT NULL,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    -- No foreign key constraint
)
```

## 🔄 Workflow Clarification

### 1. Topic Creation (Before Processing)
```python
# User submits topic titles
# POST /api/topics
db.save_topic_status(original_title, 'pending', None)
# ✅ Inserts into topic_status with status='pending'
# ❌ OLD: Would fail because topic not in topics table yet
```

### 2. Topic Processing (Worker Service)
```python
# Worker picks up pending topics
# Calls Gemini API to generate content
generated_data = gemini_client.generate_topic(original_title)

# Saves to topics table
db.save_topic(generated_data)  # Insert into topics

# Updates status
db.update_topic_status(original_title, 'completed')
```

### 3. Relationship

```
topic_status.original_title  →  Logical Link  →  topics.title
                                (Not a DB FK)
```

## 📊 Migration

### Backup & Restore
- ✅ Backed up 11,664 existing records
- ✅ Dropped old table with FK
- ✅ Created new table without FK
- ✅ Restored all 11,664 records

### Files Modified

1. **unified_database.py**
   - Updated schema definition (line 197)
   - Added UNIQUE constraint on original_title

2. **fix_topic_status_fk.py** (Migration script)
   - One-time script to fix existing database
   - Can be deleted after verification

## 🧪 Testing

### Verify Fix
```bash
# Check new schema
sqlite3 unified.db "SELECT sql FROM sqlite_master WHERE name='topic_status';"

# Test topic creation
curl -X POST http://localhost:8000/api/topics \
  -H "Content-Type: application/json" \
  -d '{"titles": "How Redis Works\nHow Kafka Works"}'

# Should succeed without FK error ✅
```

### Expected Behavior
- ✅ Topics can be created before processing
- ✅ No foreign key errors
- ✅ Duplicate detection still works (UNIQUE constraint)
- ✅ Worker service processes normally

## 🔍 Root Cause

The FK constraint was likely added manually or by a migration script that didn't account for the workflow:
- `topic_status` is a **pre-processing queue**
- `topics` is the **final processed data**
- The relationship is **logical, not physical**

## 📝 Best Practices

### DO ✅
- Use `topic_status` for tracking pending/processing/completed states
- Let `original_title` be the logical link between tables
- Use UNIQUE constraints to prevent duplicates

### DON'T ❌
- Don't add FK constraints between queue tables and result tables
- Don't assume all entries in `topic_status` exist in `topics`
- Don't use `topic_status.id` as a reference (it's auto-generated)

## 🚀 Future Improvements

1. **Add index** on `original_title` for faster lookups
2. **Clean up completed** entries older than 30 days
3. **Add status transitions** validation (pending → processing → completed)
4. **Monitor** for orphaned entries

---

**Status**: ✅ Fixed  
**Impact**: High (blocked topic creation)  
**Downtime**: None (hot fix applied)  
**Data Loss**: None (all records preserved)
