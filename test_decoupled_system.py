#!/usr/bin/env python3
"""
Test script to demonstrate the decoupled topic processing system.

This script:
1. Adds topics via the API (which saves them as pending)
2. Shows the processing status
3. Demonstrates how the worker picks up and processes topics
"""
import requests
import time
import json
import sys

BASE_URL = "http://localhost:8000/api/v1"

def print_status(status_data):
    """Pretty print the processing status."""
    print("\n" + "="*50)
    print("PROCESSING STATUS")
    print("="*50)
    print(f"Is Processing: {status_data.get('is_processing', False)}")
    print(f"Pending: {status_data.get('pending_count', 0)}")
    print(f"Processing: {status_data.get('processing_count', 0)}")
    print(f"Completed: {status_data.get('completed_count', 0)}")
    print(f"Failed: {status_data.get('failed_count', 0)}")
    print(f"Total: {status_data.get('total_count', 0)}")
    
    if status_data.get('recent_failures'):
        print("\nRecent Failures:")
        for failure in status_data['recent_failures'][:3]:
            print(f"  - {failure['title']}: {failure['error_message']}")
    print("="*50)

def test_decoupled_system():
    """Test the decoupled topic processing system."""
    print("Testing Decoupled Topic Processing System")
    print("-" * 50)
    
    # Test topics
    test_topics = [
        "How Netflix Handles 220 Million Concurrent Streams",
        "Building a Real-time Analytics System at Scale",
        "Designing Discord's Voice Chat Infrastructure",
        "How Uber Processes Millions of Rides Per Day",
        "Building a Global CDN from Scratch"
    ]
    
    print(f"\n1. Adding {len(test_topics)} topics to the system...")
    
    # Add topics via API
    try:
        response = requests.post(
            f"{BASE_URL}/topics",
            json={
                "topics": test_topics,
                "batch_size": 5
            }
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✓ Topics added successfully!")
            print(f"  - Saved: {result.get('saved_topics', 0)}")
            print(f"  - Skipped: {result.get('skipped_topics', 0)}")
            if result.get('skipped_titles'):
                print(f"  - Skipped titles: {', '.join(result['skipped_titles'])}")
        else:
            print(f"✗ Failed to add topics: {response.status_code}")
            print(f"  Error: {response.text}")
            return
            
    except Exception as e:
        print(f"✗ Error calling API: {e}")
        return
    
    # Check initial status
    print("\n2. Checking initial processing status...")
    try:
        response = requests.get(f"{BASE_URL}/processing-status")
        if response.status_code == 200:
            status = response.json()
            print_status(status)
        else:
            print(f"✗ Failed to get status: {response.status_code}")
    except Exception as e:
        print(f"✗ Error getting status: {e}")
    
    # Check worker status
    print("\n3. Checking worker status...")
    try:
        response = requests.get(f"{BASE_URL}/worker-status")
        if response.status_code == 200:
            worker_status = response.json()
            print(f"Worker Running: {worker_status.get('worker_running', False)}")
            print(f"Message: {worker_status.get('message', '')}")
            
            if not worker_status.get('worker_running'):
                print("\n⚠️  Worker doesn't appear to be running!")
                print("Please run the worker in another terminal:")
                print("  python run_worker.py")
        else:
            print(f"✗ Failed to get worker status: {response.status_code}")
    except Exception as e:
        print(f"✗ Error getting worker status: {e}")
    
    # Monitor processing
    print("\n4. Monitoring processing progress...")
    print("(Press Ctrl+C to stop monitoring)")
    
    try:
        prev_status = None
        no_change_count = 0
        
        while True:
            response = requests.get(f"{BASE_URL}/processing-status")
            if response.status_code == 200:
                status = response.json()
                
                # Only print if status changed
                if prev_status != status:
                    print_status(status)
                    prev_status = status
                    no_change_count = 0
                else:
                    no_change_count += 1
                    if no_change_count % 10 == 0:
                        print(".", end="", flush=True)
                
                # Check if processing is complete
                if not status.get('is_processing') and status.get('pending_count', 0) == 0:
                    print("\n\n✓ All topics have been processed!")
                    break
            
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\n\nMonitoring stopped by user.")
    
    # Final status
    print("\n5. Final processing summary...")
    try:
        response = requests.get(f"{BASE_URL}/processing-status")
        if response.status_code == 200:
            status = response.json()
            print_status(status)
            
            # Get detailed topic summary
            response = requests.get(f"{BASE_URL}/topic-status-summary")
            if response.status_code == 200:
                summary = response.json()
                if summary.get('success'):
                    print("\nDetailed Status Summary:")
                    for status_type, count in summary['summary'].items():
                        if isinstance(count, int):
                            print(f"  {status_type}: {count}")
                            
    except Exception as e:
        print(f"✗ Error getting final status: {e}")
    
    print("\n" + "="*50)
    print("Test completed!")
    print("="*50)


if __name__ == "__main__":
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code != 200:
            print("❌ Server is not running! Please start the FastAPI server first.")
            print("Run: python start_unified_server.py")
            sys.exit(1)
    except:
        print("❌ Cannot connect to server! Please start the FastAPI server first.")
        print("Run: python start_unified_server.py")
        sys.exit(1)
    
    test_decoupled_system()


