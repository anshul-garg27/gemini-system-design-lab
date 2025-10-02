-- Find duplicate titles in topic_status table
-- This shows titles that appear more than once

SELECT 
    title,
    COUNT(*) as duplicate_count,
    GROUP_CONCAT(status) as statuses,
    GROUP_CONCAT(created_at) as created_dates
FROM 
    topic_status
GROUP BY 
    title
HAVING 
    COUNT(*) > 1
ORDER BY 
    duplicate_count DESC,
    title ASC;

-- Alternative: Show all records for duplicate titles
-- This gives more detail about each duplicate entry

SELECT 
    ts1.*
FROM 
    topic_status ts1
INNER JOIN (
    SELECT title
    FROM topic_status
    GROUP BY title
    HAVING COUNT(*) > 1
) ts2 ON ts1.title = ts2.title
ORDER BY 
    ts1.title, 
    ts1.created_at;

-- Find duplicates in topics table (if they exist there)
SELECT 
    title,
    COUNT(*) as duplicate_count
FROM 
    topics
GROUP BY 
    title
HAVING 
    COUNT(*) > 1
ORDER BY 
    duplicate_count DESC;

-- Find titles that exist in both topic_status and topics multiple times
SELECT 
    t.title,
    COUNT(DISTINCT t.id) as topic_count,
    COUNT(DISTINCT ts.created_at) as status_count
FROM 
    topics t
INNER JOIN 
    topic_status ts ON t.title = ts.title
GROUP BY 
    t.title
HAVING 
    topic_count > 1 OR status_count > 1;

-- Clean up duplicates (BE CAREFUL - this deletes data!)
-- This keeps the most recent entry and deletes older duplicates
/*
DELETE FROM topic_status 
WHERE rowid NOT IN (
    SELECT MAX(rowid)
    FROM topic_status
    GROUP BY title
);
*/


