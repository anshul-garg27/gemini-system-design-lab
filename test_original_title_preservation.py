#!/usr/bin/env python3
"""
Test to verify that original_title is preserved exactly as user input.
No cleaning should happen before saving to database.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from unified_database import unified_db


def test_original_title_preservation():
    """Test that original_title is saved without any cleaning."""
    
    print("\n" + "="*70)
    print("🧪 TEST: Original Title Preservation")
    print("="*70)
    
    # Test cases with various formatting
    test_cases = [
        {
            'input': "38. Give me 10 seconds, I'll show how **UUIDs vs auto-incrementing IDs involve tradeoffs** .",
            'expected_original': "38. Give me 10 seconds, I'll show how **UUIDs vs auto-incrementing IDs involve tradeoffs** .",
            'description': "Numbered + Verbose + Markdown"
        },
        {
            'input': "24. **Why memory generations optimize GC for different object lifetime patterns**",
            'expected_original': "24. **Why memory generations optimize GC for different object lifetime patterns**",
            'description': "Numbered + Markdown"
        },
        {
            'input': "🚀 How Kubernetes Auto-Scaling Works",
            'expected_original': "🚀 How Kubernetes Auto-Scaling Works",
            'description': "Emoji + Simple"
        },
        {
            'input': "167. How Netflix CDN Works",
            'expected_original': "167. How Netflix CDN Works",
            'description': "Numbered + Simple"
        }
    ]
    
    results = []
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{'─'*70}")
        print(f"Test Case {i}: {test['description']}")
        print(f"{'─'*70}")
        print(f"📝 Input: {test['input']}")
        
        # Add topic for processing
        topic_status_id = unified_db.add_topic_for_processing(test['input'])
        
        if not topic_status_id:
            print(f"❌ Failed to add topic")
            results.append(False)
            continue
        
        # Retrieve and check
        status = unified_db.get_topic_status_by_title(test['input'])
        
        if not status:
            print(f"❌ Failed to retrieve topic")
            results.append(False)
            continue
        
        saved_title = status.get('original_title') or status.get('title')
        
        print(f"💾 Saved as: {saved_title}")
        print(f"✅ Expected: {test['expected_original']}")
        
        # Check if they match EXACTLY
        if saved_title == test['expected_original']:
            print(f"✅ PASS: Original title preserved perfectly!")
            results.append(True)
        else:
            print(f"❌ FAIL: Original title was modified!")
            print(f"   Difference:")
            print(f"   - Input:  '{test['input']}'")
            print(f"   - Saved:  '{saved_title}'")
            results.append(False)
        
        # Cleanup
        conn = unified_db.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM topic_status WHERE id = ?", (topic_status_id,))
        conn.commit()
        conn.close()
    
    # Summary
    print(f"\n{'='*70}")
    print("📊 SUMMARY")
    print(f"{'='*70}")
    
    passed = sum(results)
    total = len(results)
    
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print(f"✅ All tests PASSED! Original titles are preserved correctly.")
        return True
    else:
        print(f"❌ {total - passed} test(s) FAILED! Original titles are being modified.")
        return False


def test_full_workflow():
    """Test complete workflow: add → process → verify both titles."""
    
    print("\n" + "="*70)
    print("🔄 TEST: Complete Workflow (Original → Current Title)")
    print("="*70)
    
    user_input = "38. Give me 10 seconds, **UUIDs vs auto-incrementing IDs** ."
    gemini_cleaned = "UUIDs vs Auto-incrementing IDs: Distribution and Storage Tradeoffs"
    
    print(f"\n📝 User Input: {user_input}")
    
    # Step 1: Add topic
    topic_status_id = unified_db.add_topic_for_processing(user_input)
    print(f"✅ Added with topic_status_id: {topic_status_id}")
    
    # Step 2: Check original_title
    status = unified_db.get_topic_status_by_title(user_input)
    saved_original = status.get('original_title') or status.get('title')
    
    print(f"\n📊 After Adding:")
    print(f"   original_title: {saved_original}")
    print(f"   current_title: {status.get('current_title')}")
    print(f"   status: {status['status']}")
    
    # Verify original is unchanged
    if saved_original == user_input:
        print(f"   ✅ Original title preserved!")
    else:
        print(f"   ❌ Original title was modified!")
    
    # Step 3: Simulate Gemini processing
    unified_db.update_topic_status_by_id(topic_status_id, 'processing')
    
    # Step 4: Update with cleaned title (simulating Gemini)
    unified_db.update_topic_status_by_id(
        topic_status_id, 
        'completed',
        current_title=gemini_cleaned
    )
    
    # Step 5: Verify both titles
    final_status = unified_db.get_topic_status_by_title(user_input)
    
    print(f"\n📊 After Processing:")
    print(f"   original_title: {final_status.get('original_title')}")
    print(f"   current_title: {final_status.get('current_title')}")
    print(f"   status: {final_status['status']}")
    
    # Verify
    original_preserved = final_status.get('original_title') == user_input
    current_updated = final_status.get('current_title') == gemini_cleaned
    
    print(f"\n🔍 Verification:")
    print(f"   Original preserved: {'✅' if original_preserved else '❌'}")
    print(f"   Current updated: {'✅' if current_updated else '❌'}")
    
    # Cleanup
    conn = unified_db.get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM topic_status WHERE id = ?", (topic_status_id,))
    conn.commit()
    conn.close()
    
    success = original_preserved and current_updated
    
    if success:
        print(f"\n✅ Complete workflow PASSED!")
    else:
        print(f"\n❌ Complete workflow FAILED!")
    
    return success


def main():
    """Run all tests."""
    print("\n" + "="*70)
    print("🚀 ORIGINAL TITLE PRESERVATION TEST SUITE")
    print("="*70)
    print("\nThis test verifies that:")
    print("1. User input is saved EXACTLY as-is in original_title")
    print("2. No cleaning happens before saving to database")
    print("3. Gemini's cleaned version goes to current_title")
    print("="*70)
    
    # Run tests
    test1_passed = test_original_title_preservation()
    test2_passed = test_full_workflow()
    
    # Final summary
    print("\n" + "="*70)
    print("🎯 FINAL RESULTS")
    print("="*70)
    
    if test1_passed and test2_passed:
        print("✅ ALL TESTS PASSED!")
        print("\nOriginal title preservation is working correctly:")
        print("  ✅ User input preserved exactly")
        print("  ✅ Gemini cleaned version in current_title")
        print("  ✅ Both titles tracked independently")
        return 0
    else:
        print("❌ SOME TESTS FAILED!")
        if not test1_passed:
            print("  ❌ Original title preservation failed")
        if not test2_passed:
            print("  ❌ Complete workflow failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
