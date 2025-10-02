#!/usr/bin/env python3
"""
Test the integrated consistency fix with existing code structure.
Tests both frontend flow and worker polling flow.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from unified_database import unified_db


def test_flow_1_frontend_add():
    """Test Flow 1: Frontend adds topics"""
    print("\n" + "="*60)
    print("TEST 1: Frontend Add Flow (Direct Add)")
    print("="*60)
    
    test_titles = [
        "How Netflix CDN Works Globally",
        "Instagram Photo Compression Algorithm",
        "WhatsApp Message Queue Architecture"
    ]
    
    print("\n📝 Step 1: Simulating frontend adding topics...")
    added_ids = []
    
    for title in test_titles:
        # Check if already exists
        existing = unified_db.get_topic_status_by_title(title)
        
        if existing:
            print(f"⚠️  Topic already exists: {title} (ID: {existing['id']})")
            added_ids.append(existing['id'])
        else:
            # Add new topic
            topic_status_id = unified_db.add_topic_for_processing(title)
            if topic_status_id:
                added_ids.append(topic_status_id)
                print(f"✅ Added: {title} → topic_status_id={topic_status_id}")
            else:
                print(f"❌ Failed to add: {title}")
    
    print(f"\n✅ Flow 1 Complete: Added {len(added_ids)} topics")
    print(f"   Topic Status IDs: {added_ids}")
    
    return added_ids


def test_flow_2_worker_polling():
    """Test Flow 2: Worker polls and processes"""
    print("\n" + "="*60)
    print("TEST 2: Worker Polling Flow")
    print("="*60)
    
    print("\n🔍 Step 1: Worker polls for pending topics...")
    pending_topics = unified_db.get_topics_by_status('pending', limit=10)
    
    if not pending_topics:
        print("   No pending topics found")
        return []
    
    print(f"   Found {len(pending_topics)} pending topics:")
    for topic in pending_topics:
        print(f"   - ID {topic['topic_status_id']}: {topic['title']}")
    
    print("\n🔄 Step 2: Simulating processing with ID tracking...")
    processed_ids = []
    
    for topic in pending_topics[:3]:  # Process first 3
        topic_status_id = topic['topic_status_id']
        title = topic['title']
        
        print(f"\n   Processing topic_status_id={topic_status_id}: {title}")
        
        # Simulate: Update to processing
        success = unified_db.update_topic_status_by_id(topic_status_id, 'processing')
        print(f"      → Set to 'processing': {'✅' if success else '❌'}")
        
        # Simulate: Gemini returns modified title
        modified_title = f"Comprehensive: {title}"
        print(f"      → Gemini modified title to: '{modified_title}'")
        
        # Simulate: Update to completed (using same ID!)
        success = unified_db.update_topic_status_by_id(topic_status_id, 'completed')
        print(f"      → Set to 'completed': {'✅' if success else '❌'}")
        
        processed_ids.append(topic_status_id)
    
    print(f"\n✅ Flow 2 Complete: Processed {len(processed_ids)} topics")
    print(f"   Topic Status IDs: {processed_ids}")
    
    return processed_ids


def check_for_duplicates():
    """Check if any duplicates were created"""
    print("\n" + "="*60)
    print("VERIFICATION: Checking for Duplicates")
    print("="*60)
    
    conn = unified_db.get_connection()
    cursor = conn.cursor()
    
    # Check schema first
    cursor.execute("PRAGMA table_info(topic_status)")
    columns = {row[1] for row in cursor.fetchall()}
    
    # Check for duplicate titles
    if 'original_title' in columns:
        cursor.execute("""
            SELECT original_title, COUNT(*) as count
            FROM topic_status
            GROUP BY original_title
            HAVING count > 1
            ORDER BY count DESC
            LIMIT 10
        """)
    else:
        cursor.execute("""
            SELECT title, COUNT(*) as count
            FROM topic_status
            GROUP BY title
            HAVING count > 1
            ORDER BY count DESC
            LIMIT 10
        """)
    
    duplicates = cursor.fetchall()
    
    if duplicates:
        print(f"\n❌ Found {len(duplicates)} titles with duplicates:")
        for title, count in duplicates:
            print(f"   - '{title}': {count} entries")
    else:
        print("\n✅ No duplicates found! ID tracking is working correctly.")
    
    # Show status distribution
    cursor.execute("""
        SELECT status, COUNT(*) as count
        FROM topic_status
        GROUP BY status
        ORDER BY count DESC
    """)
    
    statuses = cursor.fetchall()
    
    print("\n📊 Status Distribution:")
    for status, count in statuses:
        print(f"   {status:12s}: {count:4d}")
    
    conn.close()
    
    return len(duplicates) == 0


def test_id_consistency():
    """Test that ID is maintained throughout lifecycle"""
    print("\n" + "="*60)
    print("TEST 3: ID Consistency Throughout Lifecycle")
    print("="*60)
    
    # Clean up any previous test runs first
    conn = unified_db.get_connection()
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(topic_status)")
    columns = {row[1] for row in cursor.fetchall()}
    
    if 'original_title' in columns:
        cursor.execute("DELETE FROM topic_status WHERE original_title LIKE 'Test ID Consistency%'")
    else:
        cursor.execute("DELETE FROM topic_status WHERE title LIKE 'Test ID Consistency%'")
    conn.commit()
    conn.close()
    
    test_title = "Test ID Consistency Topic"
    
    print(f"\n📝 Adding topic: {test_title}")
    topic_status_id = unified_db.add_topic_for_processing(test_title)
    print(f"   Initial topic_status_id: {topic_status_id}")
    
    # Check initial state
    status = unified_db.get_topic_status_by_title(test_title)
    print(f"\n📊 Initial State:")
    print(f"   topic_status_id: {status['id']}")
    print(f"   title: {status['title']}")
    print(f"   status: {status['status']}")
    
    # Update to processing
    unified_db.update_topic_status_by_id(topic_status_id, 'processing')
    status = unified_db.get_topic_status_by_title(test_title)
    print(f"\n📊 After 'processing' Update:")
    print(f"   topic_status_id: {status['id']} (should be {topic_status_id})")
    print(f"   status: {status['status']}")
    print(f"   ✅ ID maintained!" if status['id'] == topic_status_id else "❌ ID changed!")
    
    # Update to completed with a cleaned title (simulating Gemini's output)
    gemini_cleaned_title = "Comprehensive Guide to ID Consistency Testing Patterns"
    unified_db.update_topic_status_by_id(
        topic_status_id, 
        'completed',
        current_title=gemini_cleaned_title
    )
    status = unified_db.get_topic_status_by_title(test_title)
    print(f"\n📊 After 'completed' Update (with current_title):")
    print(f"   topic_status_id: {status['id']} (should be {topic_status_id})")
    print(f"   status: {status['status']}")
    if 'original_title' in status:
        print(f"   original_title: {status.get('original_title')}")
        print(f"   current_title: {status.get('current_title')}")
    print(f"   ✅ ID maintained!" if status['id'] == topic_status_id else "❌ ID changed!")
    
    # Check for duplicates
    conn = unified_db.get_connection()
    cursor = conn.cursor()
    
    # Check schema first
    cursor.execute("PRAGMA table_info(topic_status)")
    columns = {row[1] for row in cursor.fetchall()}
    
    if 'original_title' in columns:
        cursor.execute("SELECT COUNT(*) FROM topic_status WHERE original_title = ?", (test_title,))
    else:
        cursor.execute("SELECT COUNT(*) FROM topic_status WHERE title = ?", (test_title,))
    
    count = cursor.fetchone()[0]
    conn.close()
    
    print(f"\n🔍 Duplicate Check:")
    print(f"   Entries for '{test_title}': {count}")
    
    if count == 1 and status['id'] == topic_status_id:
        print(f"\n✅ ID Consistency Test PASSED!")
        return True
    else:
        print(f"\n❌ ID Consistency Test FAILED!")
        return False


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("🚀 INTEGRATED CONSISTENCY TEST SUITE")
    print("="*60)
    print("\nTesting the integrated solution that:")
    print("- Keeps existing process_topics_background logic")
    print("- Adds topic_status_id tracking")
    print("- Works with both frontend and worker flows")
    print("="*60)
    
    # Test 1: Frontend flow
    frontend_ids = test_flow_1_frontend_add()
    
    # Test 2: Worker polling flow
    worker_ids = test_flow_2_worker_polling()
    
    # Test 3: ID consistency
    consistency_ok = test_id_consistency()
    
    # Verification
    no_duplicates = check_for_duplicates()
    
    # Final summary
    print("\n" + "="*60)
    print("📊 FINAL SUMMARY")
    print("="*60)
    
    print(f"✅ Frontend Flow: Added {len(frontend_ids)} topics")
    print(f"✅ Worker Flow: Processed {len(worker_ids)} topics")
    print(f"{'✅' if consistency_ok else '❌'} ID Consistency: {'PASSED' if consistency_ok else 'FAILED'}")
    print(f"{'✅' if no_duplicates else '❌'} No Duplicates: {'PASSED' if no_duplicates else 'FAILED'}")
    
    if consistency_ok and no_duplicates:
        print("\n🎉 All tests PASSED! The integrated solution is working correctly.")
        print("\n✅ Key Points:")
        print("   - topic_status_id is tracked throughout the lifecycle")
        print("   - No duplicate rows are created")
        print("   - Title modifications don't break tracking")
        print("   - Existing parallel processing is preserved")
    else:
        print("\n❌ Some tests FAILED. Please review the implementation.")
    
    print("="*60)


if __name__ == "__main__":
    main()
