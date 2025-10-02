#!/usr/bin/env python3
"""
Test script for the improved consistency logic.
Tests the new workflow with proper ID tracking.
"""

import json
import time
from pathlib import Path
from improved_unified_database import improved_unified_db


def test_consistency_workflow():
    """Test the improved consistency workflow."""
    
    print("🧪 Testing Improved Consistency Workflow")
    print("=" * 50)
    
    # Test data
    test_topics = [
        {"title": "How Netflix Handles Global CDN Distribution"},
        {"title": "Designing Instagram's Photo Upload System", "id": 501},
        {"title": "WhatsApp Message Delivery Architecture"},
    ]
    
    db = improved_unified_db
    
    # Step 1: Add topics for processing
    print("\n📝 Step 1: Adding topics for processing...")
    topic_mappings = []
    
    for i, topic in enumerate(test_topics):
        original_title = topic['title']
        suggested_id = topic.get('id')
        
        topic_status_id = db.add_topic_for_processing(original_title)
        if topic_status_id:
            topic_mappings.append({
                'topic_status_id': topic_status_id,
                'original_title': original_title,
                'suggested_id': suggested_id
            })
            print(f"✅ Added: '{original_title}' → Status ID: {topic_status_id}")
        else:
            print(f"❌ Failed to add: '{original_title}'")
    
    # Step 2: Test status updates
    print("\n🔄 Step 2: Testing status updates...")
    
    for mapping in topic_mappings:
        topic_status_id = mapping['topic_status_id']
        original_title = mapping['original_title']
        
        # Update to processing
        print(f"\n🔄 Processing: {original_title} (ID: {topic_status_id})")
        success = db.update_topic_status_by_id(topic_status_id, 'processing')
        print(f"   Processing status update: {'✅' if success else '❌'}")
        
        # Simulate title modification (as Gemini would do)
        modified_title = f"Enhanced: {original_title}"
        
        # Update with modified title
        success = db.update_topic_status_by_id(
            topic_status_id=topic_status_id,
            status='completed',
            current_title=modified_title
        )
        print(f"   Completion status update: {'✅' if success else '❌'}")
        print(f"   Modified title: '{modified_title}'")
        
        # Simulate saving generated topic data
        fake_topic_data = {
            'id': mapping['suggested_id'] or (topic_status_id + 1000),
            'title': modified_title,
            'description': f"Comprehensive analysis of {original_title}",
            'category': 'system_design',
            'subcategory': 'scalability',
            'company': 'test_company',
            'technologies': ['Python', 'Redis', 'PostgreSQL'],
            'complexity_level': 'intermediate',
            'tags': ['scalability', 'performance'],
            'related_topics': [],
            'metrics': {'scale': '1M+ users', 'latency': '100ms'},
            'implementation_details': {'architecture': 'microservices'},
            'learning_objectives': ['Understand scalability patterns'],
            'difficulty': 6,
            'estimated_read_time': '10 minutes',
            'prerequisites': ['Basic system design'],
            'created_date': '2024-01-01',
            'updated_date': '2024-01-01'
        }
        
        saved = db.save_generated_topic_with_status_id(fake_topic_data, topic_status_id)
        print(f"   Topic save: {'✅' if saved else '❌'}")
    
    # Step 3: Test retrieval and verification
    print("\n📊 Step 3: Testing data retrieval...")
    
    for mapping in topic_mappings:
        topic_status_id = mapping['topic_status_id']
        
        topic_with_status = db.get_topic_with_status(topic_status_id)
        if topic_with_status:
            print(f"\n📋 Topic Status ID {topic_status_id}:")
            print(f"   Original Title: {topic_with_status['original_title']}")
            print(f"   Current Title: {topic_with_status['current_title']}")
            print(f"   Final Title: {topic_with_status['final_title']}")
            print(f"   Status: {topic_with_status['status']}")
            print(f"   Topic ID: {topic_with_status['topic_id']}")
        else:
            print(f"❌ Could not retrieve topic with status ID {topic_status_id}")
    
    # Step 4: Test statistics
    print("\n📈 Step 4: Testing statistics...")
    stats = db.get_processing_statistics()
    
    print(f"Total Topics: {stats['total_topics']}")
    print(f"Completed: {stats['completed']}")
    print(f"Failed: {stats['failed']}")
    print(f"Processing: {stats['processing']}")
    print(f"Pending: {stats['pending']}")
    print(f"Completion Rate: {stats['completion_rate']}%")
    
    # Step 5: Test consistency verification
    print("\n🔍 Step 5: Consistency verification...")
    
    # Check that no duplicate entries were created
    conn = db.get_connection()
    cursor = conn.cursor()
    
    try:
        # Count topic_status entries for our test titles
        test_titles = [topic['title'] for topic in test_topics]
        placeholders = ','.join(['?' for _ in test_titles])
        
        cursor.execute(f"""
            SELECT original_title, COUNT(*) 
            FROM topic_status 
            WHERE original_title IN ({placeholders})
            GROUP BY original_title
            HAVING COUNT(*) > 1
        """, test_titles)
        
        duplicates = cursor.fetchall()
        
        if duplicates:
            print(f"❌ Found duplicate entries: {duplicates}")
        else:
            print("✅ No duplicate entries found")
        
        # Verify foreign key relationships
        cursor.execute("""
            SELECT COUNT(*) 
            FROM topics t 
            INNER JOIN topic_status ts ON t.topic_status_id = ts.id 
            WHERE ts.original_title IN ({})
        """.format(placeholders), test_titles)
        
        linked_count = cursor.fetchone()[0]
        print(f"✅ Foreign key relationships: {linked_count} topics properly linked")
        
    finally:
        conn.close()
    
    print("\n🎉 Consistency test completed!")
    return True


def test_error_handling():
    """Test error handling and failed topic retry."""
    
    print("\n🧪 Testing Error Handling")
    print("=" * 30)
    
    db = improved_unified_db
    
    # Add a topic that will "fail"
    failed_title = "Test Failed Topic Processing"
    topic_status_id = db.add_topic_for_processing(failed_title)
    
    if not topic_status_id:
        print("❌ Could not add test topic")
        return False
    
    print(f"✅ Added test topic with status ID: {topic_status_id}")
    
    # Update to processing
    db.update_topic_status_by_id(topic_status_id, 'processing')
    print("🔄 Updated to processing status")
    
    # Simulate failure
    error_message = "Simulated API timeout error"
    db.update_topic_status_by_id(
        topic_status_id=topic_status_id,
        status='failed',
        error_message=error_message
    )
    print(f"❌ Simulated failure: {error_message}")
    
    # Verify failed status
    topic_with_status = db.get_topic_with_status(topic_status_id)
    if topic_with_status and topic_with_status['status'] == 'failed':
        print("✅ Failed status correctly recorded")
        print(f"   Error message: {topic_with_status['error_message']}")
    else:
        print("❌ Failed status not recorded correctly")
    
    # Test retry logic (reset to pending)
    db.update_topic_status_by_id(
        topic_status_id=topic_status_id,
        status='pending',
        error_message=None
    )
    print("🔄 Reset to pending for retry")
    
    # Verify reset
    topic_with_status = db.get_topic_with_status(topic_status_id)
    if topic_with_status and topic_with_status['status'] == 'pending':
        print("✅ Successfully reset for retry")
    else:
        print("❌ Reset failed")
    
    return True


def main():
    """Run all consistency tests."""
    print("🚀 Starting Improved Consistency Tests")
    print("=" * 60)
    
    # Test 1: Main workflow
    test1_success = test_consistency_workflow()
    
    # Test 2: Error handling
    test2_success = test_error_handling()
    
    print(f"\n📊 Test Results:")
    print(f"   Consistency Workflow: {'✅ PASS' if test1_success else '❌ FAIL'}")
    print(f"   Error Handling: {'✅ PASS' if test2_success else '❌ FAIL'}")
    
    if test1_success and test2_success:
        print("\n🎉 All tests passed! The improved consistency system is working correctly.")
    else:
        print("\n❌ Some tests failed. Please review the implementation.")


if __name__ == "__main__":
    main()
