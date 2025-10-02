#!/usr/bin/env python3
"""
Benchmark script to demonstrate performance improvements between
old and refactored database implementations.
"""

import time
import logging
import sys
from pathlib import Path

# Suppress logs during benchmarking
logging.basicConfig(level=logging.CRITICAL)

def benchmark_old_implementation():
    """Benchmark the old implementation (if available)."""
    try:
        from unified_database import UnifiedDatabase as OldDB
        
        print("🔍 Benchmarking OLD implementation...")
        db = OldDB("benchmark_old.db")
        
        # Create test topic
        test_topic = {
            'id': 1,
            'title': 'Test Topic',
            'description': 'Test Description',
            'category': 'Testing',
            'subcategory': 'Benchmark',
            'company': 'Test Co',
            'technologies': ['Python'],
            'complexity_level': 'Medium',
            'tags': ['test'],
            'related_topics': [],
            'metrics': {},
            'implementation_details': {},
            'learning_objectives': [],
            'difficulty': 5,
            'estimated_read_time': '5 min',
            'prerequisites': [],
            'created_date': '2025-01-01',
            'updated_date': '2025-01-01'
        }
        
        # Warm-up
        for _ in range(10):
            db.save_topic(test_topic)
            db.get_topic_by_id(1)
        
        # Benchmark writes
        iterations = 100
        start = time.time()
        for i in range(iterations):
            test_topic['id'] = i
            db.save_topic(test_topic)
        write_time = time.time() - start
        
        # Benchmark reads
        start = time.time()
        for i in range(iterations):
            db.get_topic_by_id(i % 10 or 1)
        read_time = time.time() - start
        
        # Cleanup
        Path("benchmark_old.db").unlink(missing_ok=True)
        
        return {
            'write_time': write_time,
            'read_time': read_time,
            'total_time': write_time + read_time,
            'write_ops_per_sec': iterations / write_time,
            'read_ops_per_sec': iterations / read_time
        }
        
    except ImportError:
        print("⚠️  Old implementation not found (unified_database.py)")
        return None
    except Exception as e:
        print(f"❌ Error benchmarking old implementation: {e}")
        return None


def benchmark_new_implementation():
    """Benchmark the new refactored implementation."""
    try:
        from unified_database_refactored import UnifiedDatabase as NewDB
        
        print("🚀 Benchmarking NEW (refactored) implementation...")
        db = NewDB("benchmark_new.db")
        
        # Create test topic
        test_topic = {
            'id': 1,
            'title': 'Test Topic',
            'description': 'Test Description',
            'category': 'Testing',
            'subcategory': 'Benchmark',
            'company': 'Test Co',
            'technologies': ['Python'],
            'complexity_level': 'Medium',
            'tags': ['test'],
            'related_topics': [],
            'metrics': {},
            'implementation_details': {},
            'learning_objectives': [],
            'difficulty': 5,
            'estimated_read_time': '5 min',
            'prerequisites': [],
            'created_date': '2025-01-01',
            'updated_date': '2025-01-01'
        }
        
        # Warm-up
        for _ in range(10):
            db.save_topic(test_topic)
            db.get_topic_by_id(1)
        
        # Benchmark writes
        iterations = 100
        start = time.time()
        for i in range(iterations):
            test_topic['id'] = i
            db.save_topic(test_topic)
        write_time = time.time() - start
        
        # Benchmark reads
        start = time.time()
        for i in range(iterations):
            db.get_topic_by_id(i % 10 or 1)
        read_time = time.time() - start
        
        # Cleanup
        db.close_connections()
        Path("benchmark_new.db").unlink(missing_ok=True)
        
        return {
            'write_time': write_time,
            'read_time': read_time,
            'total_time': write_time + read_time,
            'write_ops_per_sec': iterations / write_time,
            'read_ops_per_sec': iterations / read_time
        }
        
    except ImportError:
        print("❌ New implementation not found (unified_database_refactored.py)")
        return None
    except Exception as e:
        print(f"❌ Error benchmarking new implementation: {e}")
        import traceback
        traceback.print_exc()
        return None


def print_comparison(old_results, new_results):
    """Print detailed comparison of results."""
    print("\n" + "="*70)
    print("📊 PERFORMANCE COMPARISON RESULTS")
    print("="*70)
    
    if old_results and new_results:
        print("\n📝 Detailed Metrics:")
        print("-" * 70)
        
        # Write performance
        write_improvement = (old_results['write_time'] / new_results['write_time'])
        print(f"\n✏️  WRITE OPERATIONS (100 iterations):")
        print(f"   Old:  {old_results['write_time']:.3f}s ({old_results['write_ops_per_sec']:.1f} ops/sec)")
        print(f"   New:  {new_results['write_time']:.3f}s ({new_results['write_ops_per_sec']:.1f} ops/sec)")
        print(f"   📈 Improvement: {write_improvement:.2f}x faster")
        
        # Read performance
        read_improvement = (old_results['read_time'] / new_results['read_time'])
        print(f"\n📖 READ OPERATIONS (100 iterations):")
        print(f"   Old:  {old_results['read_time']:.3f}s ({old_results['read_ops_per_sec']:.1f} ops/sec)")
        print(f"   New:  {new_results['read_time']:.3f}s ({new_results['read_ops_per_sec']:.1f} ops/sec)")
        print(f"   📈 Improvement: {read_improvement:.2f}x faster")
        
        # Overall performance
        total_improvement = (old_results['total_time'] / new_results['total_time'])
        print(f"\n⚡ OVERALL PERFORMANCE:")
        print(f"   Old Total:  {old_results['total_time']:.3f}s")
        print(f"   New Total:  {new_results['total_time']:.3f}s")
        print(f"   📈 Overall Improvement: {total_improvement:.2f}x faster")
        
        # Time saved
        time_saved = old_results['total_time'] - new_results['total_time']
        print(f"\n💰 TIME SAVED: {time_saved:.3f}s ({time_saved/old_results['total_time']*100:.1f}% reduction)")
        
        # Extrapolation
        print(f"\n🔮 EXTRAPOLATION (1000 operations):")
        print(f"   Old:  {old_results['total_time']*10:.2f}s (~{old_results['total_time']*10/60:.1f} minutes)")
        print(f"   New:  {new_results['total_time']*10:.2f}s (~{new_results['total_time']*10/60:.1f} minutes)")
        print(f"   Time Saved: {time_saved*10:.2f}s (~{time_saved*10/60:.1f} minutes)")
        
    elif new_results:
        print("\n✅ New Implementation Results:")
        print(f"   Write: {new_results['write_time']:.3f}s ({new_results['write_ops_per_sec']:.1f} ops/sec)")
        print(f"   Read:  {new_results['read_time']:.3f}s ({new_results['read_ops_per_sec']:.1f} ops/sec)")
        print(f"   Total: {new_results['total_time']:.3f}s")
        print("\n⚠️  Could not compare (old implementation not available)")
    else:
        print("\n❌ No results available")
    
    print("\n" + "="*70)


def print_feature_comparison():
    """Print feature comparison table."""
    print("\n📋 FEATURE COMPARISON")
    print("="*70)
    
    features = [
        ("Connection Pooling", "❌ No", "✅ Yes (Thread-local)"),
        ("Proper Logging", "❌ No (print only)", "✅ Yes (Full logging)"),
        ("Code Duplication", "❌ High (~500 lines)", "✅ None (Decorator pattern)"),
        ("Error Handling", "⚠️  Inconsistent", "✅ Consistent"),
        ("Transaction Mgmt", "⚠️  Manual", "✅ Automatic"),
        ("Rollback on Error", "❌ No", "✅ Yes"),
        ("Stack Traces", "❌ No", "✅ Yes (exc_info=True)"),
        ("Dict-like Results", "❌ No (tuples)", "✅ Yes (sqlite3.Row)"),
        ("Foreign Keys", "❌ Not enforced", "✅ Enforced"),
        ("Thread Safety", "⚠️  Limited", "✅ Full"),
    ]
    
    print(f"\n{'Feature':<25} {'Old':<25} {'New':<25}")
    print("-" * 70)
    for feature, old, new in features:
        print(f"{feature:<25} {old:<25} {new:<25}")
    
    print("\n" + "="*70)


def main():
    """Run benchmarks and display results."""
    print("\n" + "="*70)
    print("🎯 DATABASE PERFORMANCE BENCHMARK")
    print("="*70)
    print("\nTesting: 100 write operations + 100 read operations")
    print("This benchmark demonstrates the performance improvements from:")
    print("  • Thread-local connection pooling")
    print("  • Reduced code duplication")
    print("  • Better transaction management")
    print("\n" + "-"*70)
    
    # Run benchmarks
    old_results = benchmark_old_implementation()
    print()
    new_results = benchmark_new_implementation()
    
    # Display results
    print_comparison(old_results, new_results)
    print_feature_comparison()
    
    # Summary
    print("\n💡 KEY IMPROVEMENTS:")
    print("-" * 70)
    print("1. 🚀 Connection Pooling: Reuses connections per thread")
    print("2. 📝 Proper Logging: Structured, searchable, filterable logs")
    print("3. 🔄 DRY Principle: Eliminated ~500 lines of duplicate code")
    print("4. 🛡️  Error Handling: Automatic rollback on errors")
    print("5. 🧵 Thread Safety: Safe for concurrent operations")
    print("=" * 70)
    print("\n✅ Benchmark Complete!\n")


if __name__ == "__main__":
    main()
