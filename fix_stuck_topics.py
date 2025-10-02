#!/usr/bin/env python3
"""
Fix topics stuck in 'processing' or 'in_progress' status.
These are topics that were being processed when the worker crashed.
"""
import sqlite3
from datetime import datetime, timedelta

def fix_stuck_topics():
    """Reset stuck topics back to 'pending' status."""
    conn = sqlite3.connect('unified.db')
    cursor = conn.cursor()
    
    print("=" * 80)
    print("FIXING STUCK TOPICS")
    print("=" * 80)
    
    # Find topics stuck in processing states
    cursor.execute("""
        SELECT status, COUNT(*) as count
        FROM topic_status
        WHERE status IN ('processing', 'in_progress')
        GROUP BY status
    """)
    
    stuck_counts = cursor.fetchall()
    
    if not stuck_counts:
        print("\nNo stuck topics found!")
        return
    
    print("\nStuck topics found:")
    for status, count in stuck_counts:
        print(f"  - {status}: {count} topics")
    
    # Show some examples
    print("\nExamples of stuck topics:")
    cursor.execute("""
        SELECT title, status, created_at
        FROM topic_status
        WHERE status IN ('processing', 'in_progress')
        LIMIT 5
    """)
    
    examples = cursor.fetchall()
    for title, status, created_at in examples:
        print(f"  - [{status}] {title[:60]}... (created: {created_at})")
    
    # Ask for confirmation
    total_stuck = sum(count for _, count in stuck_counts)
    response = input(f"\nReset {total_stuck} stuck topics back to 'pending'? (y/N): ")
    
    if response.lower() == 'y':
        # Reset stuck topics to pending
        cursor.execute("""
            UPDATE topic_status
            SET status = 'pending'
            WHERE status IN ('processing', 'in_progress')
        """)
        
        updated = cursor.rowcount
        conn.commit()
        
        print(f"\n✓ Reset {updated} topics to 'pending' status")
        print("These topics will be picked up by the worker on the next run.")
        
        # Show new status counts
        cursor.execute("""
            SELECT status, COUNT(*) as count
            FROM topic_status
            GROUP BY status
            ORDER BY status
        """)
        
        print("\nNew status distribution:")
        for status, count in cursor.fetchall():
            print(f"  - {status}: {count}")
    else:
        print("\nCancelled. No changes made.")
    
    conn.close()

if __name__ == "__main__":
    fix_stuck_topics()


