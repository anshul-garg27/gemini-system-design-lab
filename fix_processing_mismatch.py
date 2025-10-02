#!/usr/bin/env python3
"""
Fix the title mismatch issue where topics are stuck in processing
because the title format doesn't match between processing and completed.
"""
import sqlite3
import re

def clean_title(title):
    """Clean a title to its core content."""
    # Remove numbering like "167. "
    title = re.sub(r'^\d+\.\s*', '', title)
    
    # Remove "Give me 10 seconds..." prefix
    title = re.sub(r'^Give me \d+ seconds?,.*?how\s*\*\*', '', title, flags=re.IGNORECASE)
    title = re.sub(r'^Give me \d+ seconds?,.*?reveal how\s*\*\*', '', title, flags=re.IGNORECASE)
    title = re.sub(r'^Give me \d+ seconds?,.*?show how\s*\*\*', '', title, flags=re.IGNORECASE)
    title = re.sub(r'^Give me \d+ seconds?,.*?explain how\s*\*\*', '', title, flags=re.IGNORECASE)
    title = re.sub(r'^Give me \d+ seconds?,.*?tell you how\s*\*\*', '', title, flags=re.IGNORECASE)
    
    # Remove ** markdown
    title = title.replace('**', '')
    
    # Remove trailing punctuation and whitespace
    title = re.sub(r'\s*\.\s*$', '', title)
    title = title.strip()
    
    return title

def fix_processing_titles():
    """Fix titles stuck in processing by matching with completed ones."""
    conn = sqlite3.connect('unified.db')
    cursor = conn.cursor()
    
    print("=" * 80)
    print("FIXING PROCESSING TITLE MISMATCHES")
    print("=" * 80)
    
    # Get all processing topics
    cursor.execute("""
        SELECT title, created_at 
        FROM topic_status 
        WHERE status = 'processing'
        ORDER BY created_at DESC
        LIMIT 1000
    """)
    
    processing_topics = cursor.fetchall()
    print(f"\nFound {len(processing_topics)} topics in 'processing' status")
    
    if not processing_topics:
        print("No processing topics to fix!")
        return
    
    # Show examples
    print("\nExamples of processing topics:")
    for title, created_at in processing_topics[:3]:
        clean = clean_title(title)
        print(f"\nOriginal: {title[:80]}...")
        print(f"Cleaned:  {clean}")
    
    # Check for matches
    fixed_count = 0
    no_match_count = 0
    
    print("\n" + "-" * 80)
    print("Checking for completed versions of processing topics...")
    
    for title, created_at in processing_topics:
        clean = clean_title(title)
        
        # Check if a completed version exists
        cursor.execute("""
            SELECT COUNT(*) 
            FROM topic_status 
            WHERE status = 'completed' 
            AND (
                title = ? 
                OR title LIKE ?
                OR title LIKE ?
            )
        """, (clean, f"%{clean}%", clean))
        
        match_count = cursor.fetchone()[0]
        
        if match_count > 0:
            # Update the processing one to completed
            cursor.execute("""
                UPDATE topic_status 
                SET status = 'completed' 
                WHERE title = ? AND status = 'processing'
            """, (title,))
            
            if cursor.rowcount > 0:
                fixed_count += 1
                if fixed_count <= 5:
                    print(f"✓ Fixed: {title[:60]}...")
        else:
            no_match_count += 1
    
    conn.commit()
    
    print(f"\n" + "-" * 80)
    print(f"RESULTS:")
    print(f"  - Fixed: {fixed_count} topics (marked as completed)")
    print(f"  - No match found: {no_match_count} topics (left as processing)")
    
    # For remaining processing topics, offer to reset to pending
    if no_match_count > 0:
        response = input(f"\nReset remaining {no_match_count} processing topics to 'pending'? (y/N): ")
        if response.lower() == 'y':
            cursor.execute("""
                UPDATE topic_status 
                SET status = 'pending' 
                WHERE status = 'processing'
            """)
            reset_count = cursor.rowcount
            conn.commit()
            print(f"✓ Reset {reset_count} topics to 'pending' status")
    
    # Show final status
    cursor.execute("""
        SELECT status, COUNT(*) as cnt 
        FROM topic_status 
        GROUP BY status 
        ORDER BY cnt DESC
    """)
    
    print("\nFinal status distribution:")
    for status, count in cursor.fetchall():
        print(f"  - {status}: {count}")
    
    conn.close()

def fix_future_processing():
    """Add a trigger to clean titles when saving."""
    print("\n" + "=" * 80)
    print("PREVENTING FUTURE ISSUES")
    print("=" * 80)
    
    print("\nTo prevent this issue in the future, modify the code to:")
    print("1. Clean titles before saving to topic_status")
    print("2. Or use a separate 'original_title' column for the raw input")
    print("\nExample fix in routes_topics.py:")
    print("""
# In process_single_batch, clean the title:
for topic in batch:
    clean_title = topic['title'].split('**')[-1].replace('**', '').strip(' .')
    db.save_topic_status(clean_title, 'processing', None)
    """)

if __name__ == "__main__":
    fix_processing_titles()
    fix_future_processing()


