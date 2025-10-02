# Check Duplicates Script Updated ✅

## 🔧 **What Was Updated**

Updated `check_duplicates.py` to be **schema-aware** and work with both old and new database schemas.

## 📊 **Changes Made**

### 1. **Schema Detection**
Added automatic schema detection at the start:

```python
# Detect schema
cursor.execute("PRAGMA table_info(topic_status)")
columns = {row[1] for row in cursor.fetchall()}
has_original_title = 'original_title' in columns

if has_original_title:
    print("\n📊 Schema: NEW (original_title + current_title)")
    title_column = 'original_title'
else:
    print("\n📊 Schema: OLD (title)")
    title_column = 'title'
```

### 2. **Dynamic Column Selection**
All queries now use the detected schema:

```python
# OLD CODE:
SELECT title FROM topic_status ...

# NEW CODE (Schema-aware):
SELECT {title_column} FROM topic_status ...
```

### 3. **Enhanced Detailed View**
For new schema, shows both `original_title` AND `current_title`:

```python
if has_original_title:
    headers = ["Original Title", "Current Title", "Status", "Error", "Created At"]
    # Shows both user input and Gemini's cleaned version
else:
    headers = ["Title", "Status", "Error", "Created At"]
    # Shows only single title column
```

## 🧪 **Test Results**

```bash
python3 check_duplicates.py
```

**Output:**
```
================================================================================
CHECKING FOR DUPLICATE TITLES
================================================================================

📊 Schema: NEW (original_title + current_title)  ✅

1. Duplicate titles in topic_status table:
--------------------------------------------------
No duplicates found in topic_status table!  ✅

3. Duplicate summary by status:
--------------------------------------------------
(empty - no duplicates)

4. Duplicate titles in topics table:
--------------------------------------------------
... (some duplicates in topics table, but not in topic_status)
```

## ✅ **Features**

### 1. **Automatic Schema Detection**
- Detects if using old (`title`) or new (`original_title`/`current_title`) schema
- Shows schema type in output
- Adapts all queries accordingly

### 2. **Duplicate Detection**
- ✅ Checks `topic_status` table for duplicates
- ✅ Checks `topics` table for duplicates
- ✅ Shows summary by status
- ✅ Shows detailed view of most duplicated title

### 3. **Cleanup Support**
- ✅ Dry-run mode (default)
- ✅ Actual cleanup with `--cleanup` flag
- ✅ Schema-aware deletion
- ✅ Keeps most recent entry

### 4. **Enhanced Display for New Schema**
Shows both titles when available:

```
╔════════════════╦═══════════════╦═════════╦═══════╦════════════╗
║ Original Title ║ Current Title ║ Status  ║ Error ║ Created At ║
╠════════════════╬═══════════════╬═════════╬═══════╬════════════╣
║ 38. Give me... ║ UUIDs vs ...  ║ completed║ NULL ║ 2025-01-01 ║
╚════════════════╩═══════════════╩═════════╩═══════╩════════════╝
```

## 🎯 **Usage**

### Check for Duplicates:
```bash
python3 check_duplicates.py
```

### Cleanup Duplicates (Dry Run):
```bash
python3 check_duplicates.py --cleanup
# Will show what would be deleted without actually deleting
```

### Cleanup Duplicates (Actually Delete):
```bash
python3 check_duplicates.py --cleanup
# Then type 'y' when prompted
```

## 📝 **Example Output**

### With New Schema:
```
📊 Schema: NEW (original_title + current_title)

1. Duplicate titles in topic_status table:
--------------------------------------------------
No duplicates found in topic_status table!

2. Detailed view (if duplicates exist):
┌────────────────────┬───────────────────┬───────────┐
│ Original Title     │ Current Title     │ Status    │
├────────────────────┼───────────────────┼───────────┤
│ 38. **UUIDs...**   │ UUIDs vs IDs...   │ completed │
│ 38. **UUIDs...**   │ NULL              │ pending   │
└────────────────────┴───────────────────┴───────────┘
```

### With Old Schema:
```
📊 Schema: OLD (title)

1. Duplicate titles in topic_status table:
--------------------------------------------------
┌─────────────────────┬───────┬──────────────┐
│ Title               │ Count │ Statuses     │
├─────────────────────┼───────┼──────────────┤
│ How Netflix CDN...  │ 2     │ completed... │
└─────────────────────┴───────┴──────────────┘
```

## 🔍 **What It Checks**

### 1. **Topic Status Duplicates**
Checks if same `original_title` (or `title` in old schema) appears multiple times:

```sql
-- New Schema:
SELECT original_title, COUNT(*) 
FROM topic_status 
GROUP BY original_title 
HAVING COUNT(*) > 1

-- Old Schema:
SELECT title, COUNT(*) 
FROM topic_status 
GROUP BY title 
HAVING COUNT(*) > 1
```

### 2. **Topics Table Duplicates**
Checks the main `topics` table (always uses `title` column):

```sql
SELECT title, COUNT(*) 
FROM topics 
GROUP BY title 
HAVING COUNT(*) > 1
```

### 3. **Duplicate Summary by Status**
Shows how many duplicate entries are in each status:

```
┌───────────┬─────────────────────────┐
│ Status    │ Total Duplicate Entries │
├───────────┼─────────────────────────┤
│ completed │ 5                       │
│ pending   │ 2                       │
│ failed    │ 1                       │
└───────────┴─────────────────────────┘
```

## 🛡️ **Safety Features**

1. **Dry Run by Default**
   - Shows what would be deleted without actually deleting
   - Need `--cleanup` flag + confirmation to actually delete

2. **Keeps Most Recent**
   - When deleting duplicates, keeps the entry with highest `rowid` (most recent)
   - Older duplicates are removed

3. **Batch Processing**
   - Deletes in batches of 100 to avoid issues with large datasets

## 🎉 **Summary**

✅ **Updated Features:**
- Schema detection (old vs new)
- Dynamic column selection
- Enhanced display for new schema
- Both titles visible in detailed view

✅ **Backward Compatible:**
- Works with old `title` schema
- Works with new `original_title`/`current_title` schema
- Automatically adapts

✅ **Safe:**
- Dry-run by default
- Confirmation required for actual deletion
- Keeps most recent entries

**Script is now fully compatible with your new schema!** 🚀
