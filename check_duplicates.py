#!/usr/bin/env python3
"""
Script to check for duplicate titles in the database and optionally clean them up.
"""
import sqlite3
from datetime import datetime

try:
    from tabulate import tabulate
except ImportError:
    # Simple fallback if tabulate is not installed
    def tabulate(data, headers=None, tablefmt=None):
        if headers:
            print("\t".join(headers))
            print("-" * 80)
        for row in data:
            print("\t".join(str(x) for x in row))

def check_duplicates():
    """Check for duplicate titles in the database (schema-aware)."""
    conn = sqlite3.connect('unified.db')
    cursor = conn.cursor()
    
    print("=" * 80)
    print("CHECKING FOR DUPLICATE TITLES")
    print("=" * 80)
    
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
    
    # 1. Check duplicates in topic_status table
    print("\n1. Duplicate titles in topic_status table:")
    print("-" * 50)
    
    cursor.execute(f"""
        SELECT 
            {title_column},
            COUNT(*) as duplicate_count,
            GROUP_CONCAT(status) as statuses,
            GROUP_CONCAT(created_at) as created_dates
        FROM 
            topic_status
        GROUP BY 
            {title_column}
        HAVING 
            COUNT(*) > 1
        ORDER BY 
            duplicate_count DESC,
            {title_column} ASC
        LIMIT 20
    """)
    
    duplicates = cursor.fetchall()
    
    if duplicates:
        headers = ["Title", "Count", "Statuses", "Created Dates"]
        # Truncate long titles for display
        display_data = []
        for row in duplicates:
            title = row[0][:50] + "..." if len(row[0]) > 50 else row[0]
            display_data.append([title, row[1], row[2], row[3]])
        
        print(tabulate(display_data, headers=headers, tablefmt="grid"))
        print(f"\nTotal duplicate titles found: {len(duplicates)}")
    else:
        print("No duplicates found in topic_status table!")
    
    # 2. Show detailed info for top duplicates
    if duplicates and len(duplicates) > 0:
        print("\n2. Detailed view of most duplicated title:")
        print("-" * 50)
        
        most_duplicated_title = duplicates[0][0]
        
        if has_original_title:
            cursor.execute("""
                SELECT 
                    original_title,
                    current_title,
                    status,
                    error_message,
                    created_at
                FROM 
                    topic_status
                WHERE 
                    original_title = ?
                ORDER BY 
                    created_at DESC
            """, (most_duplicated_title,))
            
            details = cursor.fetchall()
            headers = ["Original Title", "Current Title", "Status", "Error", "Created At"]
            display_data = []
            for row in details:
                orig = row[0][:30] + "..." if len(row[0]) > 30 else row[0]
                curr = (row[1][:30] + "...") if row[1] and len(row[1]) > 30 else (row[1] or "NULL")
                error = (row[3][:20] + "...") if row[3] and len(row[3]) > 20 else row[3]
                display_data.append([orig, curr, row[2], error, row[4]])
        else:
            cursor.execute("""
                SELECT 
                    title,
                    status,
                    error_message,
                    created_at
                FROM 
                    topic_status
                WHERE 
                    title = ?
                ORDER BY 
                    created_at DESC
            """, (most_duplicated_title,))
            
            details = cursor.fetchall()
            headers = ["Title", "Status", "Error", "Created At"]
            display_data = []
            for row in details:
                title = row[0][:30] + "..." if len(row[0]) > 30 else row[0]
                error = (row[2][:30] + "...") if row[2] and len(row[2]) > 30 else row[2]
                display_data.append([title, row[1], error, row[3]])
        
        print(tabulate(display_data, headers=headers, tablefmt="grid"))
    
    # 3. Summary by status
    print("\n3. Duplicate summary by status:")
    print("-" * 50)
    
    cursor.execute(f"""
        SELECT 
            status,
            COUNT(*) as total_duplicates
        FROM (
            SELECT {title_column}, status
            FROM topic_status
            WHERE {title_column} IN (
                SELECT {title_column}
                FROM topic_status
                GROUP BY {title_column}
                HAVING COUNT(*) > 1
            )
        )
        GROUP BY status
    """)
    
    status_summary = cursor.fetchall()
    if status_summary:
        headers = ["Status", "Total Duplicate Entries"]
        print(tabulate(status_summary, headers=headers, tablefmt="grid"))
    
    # 4. Check for duplicates in topics table
    print("\n4. Duplicate titles in topics table:")
    print("-" * 50)
    
    cursor.execute("""
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
            duplicate_count DESC
        LIMIT 10
    """)
    
    topic_duplicates = cursor.fetchall()
    
    if topic_duplicates:
        headers = ["Title", "Count"]
        display_data = []
        for row in topic_duplicates:
            title = row[0][:50] + "..." if len(row[0]) > 50 else row[0]
            display_data.append([title, row[1]])
        
        print(tabulate(display_data, headers=headers, tablefmt="grid"))
    else:
        print("No duplicates found in topics table!")
    
    conn.close()

def cleanup_duplicates(dry_run=True):
    """Clean up duplicate entries, keeping only the most recent one (schema-aware)."""
    conn = sqlite3.connect('unified.db')
    cursor = conn.cursor()
    
    # Detect schema
    cursor.execute("PRAGMA table_info(topic_status)")
    columns = {row[1] for row in cursor.fetchall()}
    has_original_title = 'original_title' in columns
    title_column = 'original_title' if has_original_title else 'title'
    
    if dry_run:
        print("\n" + "=" * 80)
        print("DRY RUN - CLEANUP SIMULATION (no data will be deleted)")
        print("=" * 80)
    else:
        print("\n" + "=" * 80)
        print("CLEANING UP DUPLICATES")
        print("=" * 80)
    
    # 1. Clean up topic_status duplicates
    print("\n1. Cleaning up topic_status table duplicates:")
    print("-" * 50)
    
    # Find duplicates that would be deleted from topic_status
    cursor.execute(f"""
        SELECT 
            t1.{title_column},
            t1.status,
            t1.created_at
        FROM 
            topic_status t1
        WHERE 
            EXISTS (
                SELECT 1
                FROM topic_status t2
                WHERE t1.{title_column} = t2.{title_column}
                AND t1.rowid < t2.rowid
            )
        ORDER BY 
            t1.{title_column}, t1.created_at
    """)
    
    status_to_delete = cursor.fetchall()
    
    if status_to_delete:
        print(f"\nWould delete {len(status_to_delete)} duplicate entries from topic_status:")
        headers = ["Title", "Status", "Created At"]
        display_data = []
        for row in status_to_delete[:10]:  # Show first 10
            title = row[0][:50] + "..." if len(row[0]) > 50 else row[0]
            display_data.append([title, row[1], row[2]])
        
        print(tabulate(display_data, headers=headers, tablefmt="grid"))
        
        if len(status_to_delete) > 10:
            print(f"\n... and {len(status_to_delete) - 10} more entries")
        
        if not dry_run:
            print("\nDeleting topic_status duplicates...")
            cursor.execute(f"""
                DELETE FROM topic_status 
                WHERE rowid NOT IN (
                    SELECT MAX(rowid)
                    FROM topic_status
                    GROUP BY {title_column}
                )
            """)
            conn.commit()
            print(f"Deleted {cursor.rowcount} duplicate entries from topic_status!")
    else:
        print("\nNo duplicates to clean up in topic_status!")
    
    # 2. Clean up topics table duplicates
    print("\n2. Cleaning up topics table duplicates:")
    print("-" * 50)
    
    # Find duplicates in topics table
    cursor.execute("""
        SELECT 
            t1.id,
            t1.title,
            t1.created_date,
            t1.source
        FROM 
            topics t1
        WHERE 
            EXISTS (
                SELECT 1
                FROM topics t2
                WHERE t1.title = t2.title
                AND t1.id < t2.id
            )
        ORDER BY 
            t1.title, t1.id
    """)
    
    topics_to_delete = cursor.fetchall()
    
    if topics_to_delete:
        print(f"\nWould delete {len(topics_to_delete)} duplicate entries from topics:")
        headers = ["ID", "Title", "Created Date", "Source"]
        display_data = []
        for row in topics_to_delete[:10]:  # Show first 10
            title = row[1][:40] + "..." if len(row[1]) > 40 else row[1]
            display_data.append([row[0], title, row[2], row[3]])
        
        print(tabulate(display_data, headers=headers, tablefmt="grid"))
        
        if len(topics_to_delete) > 10:
            print(f"\n... and {len(topics_to_delete) - 10} more entries")
        
        if not dry_run:
            # Collect IDs to delete
            ids_to_delete = [row[0] for row in topics_to_delete]
            
            print("\nDeleting topics duplicates...")
            # Delete in batches to avoid issues with large IN clauses
            batch_size = 100
            total_deleted = 0
            
            for i in range(0, len(ids_to_delete), batch_size):
                batch_ids = ids_to_delete[i:i + batch_size]
                placeholders = ','.join(['?' for _ in batch_ids])
                cursor.execute(f"""
                    DELETE FROM topics 
                    WHERE id IN ({placeholders})
                """, batch_ids)
                total_deleted += cursor.rowcount
            
            conn.commit()
            print(f"Deleted {total_deleted} duplicate entries from topics!")
    else:
        print("\nNo duplicates to clean up in topics!")
    
    # 3. Summary
    print("\n" + "=" * 80)
    print("CLEANUP SUMMARY")
    print("=" * 80)
    
    if dry_run:
        total_would_delete = len(status_to_delete) + len(topics_to_delete)
        print(f"\nDRY RUN - Would delete {total_would_delete} total duplicate entries:")
        print(f"  - topic_status: {len(status_to_delete)} entries")
        print(f"  - topics: {len(topics_to_delete)} entries")
        print("\nRun with --cleanup to actually delete these duplicates.")
    else:
        print("\nCleanup completed successfully!")
    
    conn.close()

if __name__ == "__main__":
    import sys
    
    # Check for duplicates
    check_duplicates()
    
    # Ask if user wants to clean up
    if len(sys.argv) > 1 and sys.argv[1] == "--cleanup":
        response = input("\nDo you want to clean up duplicates? (y/N): ")
        if response.lower() == 'y':
            cleanup_duplicates(dry_run=False)
        else:
            print("\nShowing cleanup simulation...")
            cleanup_duplicates(dry_run=True)
    else:
        print("\nTo clean up duplicates, run: python check_duplicates.py --cleanup")
