#!/usr/bin/env python3
"""
Test script to verify the refactored database works correctly.
Run this BEFORE integrating to ensure everything works.
"""

import logging
import sys
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def test_import():
    """Test that we can import the refactored database."""
    print("\n" + "="*70)
    print("Test 1: Import Refactored Database")
    print("="*70)
    
    try:
        from unified_database_refactored import UnifiedDatabase
        print("✅ Successfully imported UnifiedDatabase from refactored module")
        return True
    except ImportError as e:
        print(f"❌ Failed to import: {e}")
        return False


def test_initialization():
    """Test database initialization."""
    print("\n" + "="*70)
    print("Test 2: Initialize Database")
    print("="*70)
    
    try:
        from unified_database_refactored import UnifiedDatabase
        db = UnifiedDatabase("test_refactored.db")
        print("✅ Database initialized successfully")
        return db
    except Exception as e:
        print(f"❌ Initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return None


def test_save_topic(db):
    """Test saving a topic."""
    print("\n" + "="*70)
    print("Test 3: Save Topic")
    print("="*70)
    
    test_topic = {
        'id': 9999,
        'title': 'Test Topic - Refactored DB',
        'description': 'Testing the refactored database implementation',
        'category': 'Testing',
        'subcategory': 'Integration Tests',
        'company': 'Test Company',
        'technologies': ['Python', 'SQLite'],
        'complexity_level': 'Medium',
        'tags': ['test', 'integration'],
        'related_topics': [],
        'metrics': {'test_metric': 100},
        'implementation_details': {'test': 'details'},
        'learning_objectives': ['Test objective 1', 'Test objective 2'],
        'difficulty': 5,
        'estimated_read_time': '5 min',
        'prerequisites': ['Python basics'],
        'created_date': datetime.now().strftime("%Y-%m-%d"),
        'updated_date': datetime.now().strftime("%Y-%m-%d")
    }
    
    try:
        result = db.save_topic(test_topic)
        if result:
            print("✅ Topic saved successfully")
            return True
        else:
            print("❌ Failed to save topic (returned False)")
            return False
    except Exception as e:
        print(f"❌ Error saving topic: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_retrieve_topic(db):
    """Test retrieving a topic."""
    print("\n" + "="*70)
    print("Test 4: Retrieve Topic")
    print("="*70)
    
    try:
        topic = db.get_topic_by_id(9999)
        if topic:
            print(f"✅ Retrieved topic: {topic['title']}")
            print(f"   Category: {topic['category']}")
            print(f"   Technologies: {topic['technologies']}")
            return True
        else:
            print("❌ Topic not found")
            return False
    except Exception as e:
        print(f"❌ Error retrieving topic: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_connection_pooling(db):
    """Test connection pooling performance."""
    print("\n" + "="*70)
    print("Test 5: Connection Pooling Performance")
    print("="*70)
    
    import time
    
    try:
        # Perform 100 operations
        iterations = 100
        start = time.time()
        
        for i in range(iterations):
            db.get_topic_by_id(9999)
        
        elapsed = time.time() - start
        ops_per_sec = iterations / elapsed
        
        print(f"✅ Completed {iterations} operations in {elapsed:.3f}s")
        print(f"   Performance: {ops_per_sec:.1f} operations/second")
        
        if elapsed < 0.5:  # Should be very fast with pooling
            print("✅ Connection pooling working efficiently!")
            return True
        else:
            print("⚠️  Performance slower than expected (might not be using pooling)")
            return False
            
    except Exception as e:
        print(f"❌ Error during performance test: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_transaction_management(db):
    """Test transaction context manager."""
    print("\n" + "="*70)
    print("Test 6: Transaction Management")
    print("="*70)
    
    try:
        # Test successful transaction
        with db.transaction() as cursor:
            cursor.execute("SELECT COUNT(*) FROM topics")
            count = cursor.fetchone()[0]
        print(f"✅ Transaction committed successfully (found {count} topics)")
        
        # Test rollback on error
        try:
            with db.transaction() as cursor:
                cursor.execute("SELECT * FROM topics")
                raise Exception("Intentional error to test rollback")
        except Exception as e:
            if "Intentional error" in str(e):
                print("✅ Transaction rolled back on error (as expected)")
            else:
                raise
        
        return True
        
    except Exception as e:
        print(f"❌ Transaction management error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_logging():
    """Test logging functionality."""
    print("\n" + "="*70)
    print("Test 7: Logging")
    print("="*70)
    
    try:
        logger.debug("Debug message test")
        logger.info("Info message test")
        logger.warning("Warning message test")
        
        print("✅ Logging configured correctly")
        print("   Check above for log messages with timestamps")
        return True
        
    except Exception as e:
        print(f"❌ Logging error: {e}")
        return False


def test_statistics(db):
    """Test statistics methods."""
    print("\n" + "="*70)
    print("Test 8: Statistics")
    print("="*70)
    
    try:
        stats = db.get_stats()
        print(f"✅ Retrieved database statistics:")
        print(f"   Total topics: {stats['total_topics']}")
        print(f"   Completed: {stats['completed_topics']}")
        print(f"   Success rate: {stats['success_rate']}%")
        return True
        
    except Exception as e:
        print(f"❌ Statistics error: {e}")
        import traceback
        traceback.print_exc()
        return False


def cleanup(db):
    """Clean up test data and close connections."""
    print("\n" + "="*70)
    print("Cleanup")
    print("="*70)
    
    try:
        # Close connections
        db.close_connections()
        print("✅ Connections closed")
        
        # Remove test database
        import os
        if os.path.exists("test_refactored.db"):
            os.remove("test_refactored.db")
            print("✅ Test database removed")
        
        return True
        
    except Exception as e:
        print(f"⚠️  Cleanup warning: {e}")
        return False


def main():
    """Run all tests."""
    print("\n" + "="*70)
    print("🧪 REFACTORED DATABASE INTEGRATION TESTS")
    print("="*70)
    print("\nThis script tests the refactored database before integration.")
    print("All tests should pass before proceeding with integration.\n")
    
    results = {
        'import': False,
        'initialization': False,
        'save_topic': False,
        'retrieve_topic': False,
        'connection_pooling': False,
        'transaction_management': False,
        'logging': False,
        'statistics': False
    }
    
    # Test 1: Import
    results['import'] = test_import()
    if not results['import']:
        print("\n❌ CRITICAL: Cannot import refactored database. Aborting tests.")
        return 1
    
    # Test 2: Initialization
    db = test_initialization()
    if not db:
        print("\n❌ CRITICAL: Cannot initialize database. Aborting tests.")
        return 1
    results['initialization'] = True
    
    # Test 3-8: Functional tests
    results['save_topic'] = test_save_topic(db)
    results['retrieve_topic'] = test_retrieve_topic(db)
    results['connection_pooling'] = test_connection_pooling(db)
    results['transaction_management'] = test_transaction_management(db)
    results['logging'] = test_logging()
    results['statistics'] = test_statistics(db)
    
    # Cleanup
    cleanup(db)
    
    # Print summary
    print("\n" + "="*70)
    print("📊 TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name.replace('_', ' ').title()}")
    
    print(f"\n{'='*70}")
    print(f"Results: {passed}/{total} tests passed")
    print(f"{'='*70}")
    
    if passed == total:
        print("\n✅ All tests passed! Ready to integrate.")
        print("\nNext steps:")
        print("  1. Run: python integrate_refactored_db.py")
        print("  2. Or manually: cp unified_database_refactored.py unified_database.py")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please review errors before integrating.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
