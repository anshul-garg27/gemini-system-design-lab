#!/usr/bin/env python3
"""
Quick test to verify worker consistency improvements.
Simulates the worker flow with ID tracking.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from unified_database import unified_db


def test_worker_flow():
    """Test the complete worker flow with ID tracking."""
    
    print("🧪 Testing Improved Worker Consistency")
    print("=" * 60)
    
    # Step 1: Add topics for processing
    print("\n📝 Step 1: Adding topics for processing...")
    
    test_topics = [
        "How Netflix Handles Video Streaming",
        "Instagram Story Feature Architecture",
        "WhatsApp End-to-End Encryption"
    ]
    
    topic_ids = []
    for title in test_topics:
        topic_status_id = unified_db.add_topic_for_processing(title)
        if topic_status_id:
            topic_ids.append((topic_status_id, title))
            print(f"✅ Added: '{title}' → ID: {topic_status_id}")
        else:
            print(f"❌ Failed to add: '{title}'")
    
    # Step 2: Simulate worker polling
    print(f"\n🔍 Step 2: Simulating worker poll...")
    
    pending = unified_db.get_pending_topics_with_ids(limit=10)
    print(f"Found {len(pending)} pending topics:")
    for topic_id, title in pending[-3:]:  # Show last 3
        print(f"   - ID {topic_id}: {title}")
    
    # Step 3: Simulate processing with status updates
    print(f"\n🔄 Step 3: Simulating processing with ID tracking...")
    
    for topic_status_id, title in topic_ids:
        print(f"\n   Processing ID {topic_status_id}: {title}")
        
        # Update to processing
        success = unified_db.update_topic_status_by_id(topic_status_id, 'processing')
        print(f"      → Set to 'processing': {'✅' if success else '❌'}")
        
        # Simulate Gemini modifying the title
        modified_title = f"Comprehensive Guide: {title}"
        print(f"      → Gemini returned modified title: '{modified_title}'")
        
        # Update to completed (still using same ID!)
        success = unified_db.update_topic_status_by_id(topic_status_id, 'completed')
        print(f"      → Set to 'completed': {'✅' if success else '❌'}")
    
    # Step 4: Check for duplicates
    print(f"\n🔍 Step 4: Checking for duplicates...")
    
    conn = unified_db.get_connection()
    cursor = conn.cursor()
    
    # Check if any of our test titles have duplicates
    for _, title in topic_ids:
        cursor.execute("""
            SELECT COUNT(*) 
            FROM topic_status 
            WHERE title LIKE ?
        """, (f"%{title[:20]}%",))
        
        count = cursor.fetchone()[0]
        if count > 1:
            print(f"   ❌ DUPLICATE FOUND: '{title}' appears {count} times")
        else:
            print(f"   ✅ No duplicates: '{title}'")
    
    conn.close()
    
    # Step 5: Verify status updates
    print(f"\n📊 Step 5: Verifying final status...")
    
    for topic_status_id, title in topic_ids:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT status, updated_at 
            FROM topic_status 
            WHERE id = ?
        """, (topic_status_id,))
        
        result = cursor.fetchone()
        if result:
            status, updated_at = result
            print(f"   ID {topic_status_id}: status='{status}', updated={updated_at}")
        else:
            print(f"   ❌ ID {topic_status_id} not found!")
        
        conn.close()
        conn = unified_db.get_connection()
    
    conn.close()
    
    print(f"\n{'='*60}")
    print("✅ Test completed! Check the results above.")
    print("If you see 'No duplicates' for all topics, the system is working correctly!")
    print("="*60)


def check_existing_duplicates():
    """Check for any existing duplicates in the database."""
    
    print("\n🔍 Checking for existing duplicates in database...")
    
    conn = unified_db.get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT title, COUNT(*) as count 
        FROM topic_status 
        GROUP BY title 
        HAVING count > 1
        ORDER BY count DESC
    """)
    
    duplicates = cursor.fetchall()
    
    if duplicates:
        print(f"\n⚠️  Found {len(duplicates)} titles with duplicates:")
        for title, count in duplicates[:10]:  # Show first 10
            print(f"   - '{title}': {count} entries")
        
        if len(duplicates) > 10:
            print(f"   ... and {len(duplicates) - 10} more")
    else:
        print("✅ No existing duplicates found!")
    
    conn.close()


def show_status_summary():
    """Show summary of topic statuses."""
    
    print("\n📊 Current Status Summary:")
    
    conn = unified_db.get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT status, COUNT(*) as count
        FROM topic_status
        GROUP BY status
        ORDER BY count DESC
    """)
    
    results = cursor.fetchall()
    
    total = sum(count for _, count in results)
    
    for status, count in results:
        percentage = (count / total * 100) if total > 0 else 0
        print(f"   {status:12s}: {count:4d} ({percentage:5.1f}%)")
    
    print(f"   {'Total':12s}: {total:4d}")
    
    conn.close()


def main():
    """Run all tests."""
    
    print("\n" + "="*60)
    print("🚀 WORKER CONSISTENCY TEST SUITE")
    print("="*60)
    
    # Show current state
    show_status_summary()
    check_existing_duplicates()
    
    # Ask user if they want to run the test
    print("\n" + "="*60)
    response = input("Run new test flow? (y/n): ").strip().lower()
    
    if response == 'y':
        test_worker_flow()
    else:
        print("Test skipped.")
    
    print("\n✅ Done!")


if __name__ == "__main__":
    main()
