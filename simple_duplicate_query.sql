-- Simple query to find duplicate titles
-- Run this in your SQLite database

-- Find duplicates with count
SELECT 
    title,
    COUNT(*) as count
FROM 
    topic_status
GROUP BY 
    title
HAVING 
    COUNT(*) > 1
ORDER BY 
    count DESC;


