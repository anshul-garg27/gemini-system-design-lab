-- SQL queries to clean up duplicates in both tables
-- BE CAREFUL: These queries DELETE data!

-- 1. Check duplicates before cleanup
-- ===================================

-- Check topic_status duplicates
SELECT 
    title,
    COUNT(*) as count,
    GROUP_CONCAT(status) as statuses
FROM 
    topic_status
GROUP BY 
    title
HAVING 
    COUNT(*) > 1
ORDER BY 
    count DESC
LIMIT 10;

-- Check topics duplicates
SELECT 
    title,
    COUNT(*) as count,
    GROUP_CONCAT(id) as ids
FROM 
    topics
GROUP BY 
    title
HAVING 
    COUNT(*) > 1
ORDER BY 
    count DESC
LIMIT 10;

-- 2. Cleanup queries (DANGEROUS - Make backups first!)
-- =====================================================

-- Backup commands first
-- .backup unified_backup.db

-- Delete older duplicates from topic_status (keeps the newest)
DELETE FROM topic_status 
WHERE rowid NOT IN (
    SELECT MAX(rowid)
    FROM topic_status
    GROUP BY title
);

-- Delete older duplicates from topics (keeps the one with highest ID)
DELETE FROM topics 
WHERE id NOT IN (
    SELECT MAX(id)
    FROM topics
    GROUP BY title
);

-- Alternative: Delete specific duplicates from topics while keeping the best one
-- This keeps the topic with the most complete data (most fields filled)
/*
DELETE FROM topics 
WHERE id IN (
    SELECT t1.id
    FROM topics t1
    INNER JOIN topics t2 ON t1.title = t2.title
    WHERE t1.id < t2.id
    AND (
        -- Keep the one with more data
        LENGTH(t1.description) < LENGTH(t2.description)
        OR t1.technologies IS NULL AND t2.technologies IS NOT NULL
        OR t1.implementation_details IS NULL AND t2.implementation_details IS NOT NULL
    )
);
*/

-- 3. Verify cleanup
-- =================

-- Check remaining counts
SELECT 'topic_status' as table_name, COUNT(DISTINCT title) as unique_titles, COUNT(*) as total_rows FROM topic_status
UNION ALL
SELECT 'topics' as table_name, COUNT(DISTINCT title) as unique_titles, COUNT(*) as total_rows FROM topics;

-- 4. Add UNIQUE constraint to prevent future duplicates (optional)
-- ================================================================

-- This will prevent duplicates from being created in the future
-- Only run this AFTER cleaning up existing duplicates!

/*
-- Create new tables with UNIQUE constraint
CREATE TABLE topic_status_new (
    title TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Copy data from old table
INSERT INTO topic_status_new SELECT * FROM topic_status;

-- Rename tables
DROP TABLE topic_status;
ALTER TABLE topic_status_new RENAME TO topic_status;
*/


