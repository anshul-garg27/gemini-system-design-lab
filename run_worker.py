#!/usr/bin/env python3
"""
Script to run the topic processing worker service with capacity-aware worker pool.

Usage:
    python run_worker.py
    
Environment variables:
    WORKER_MAX_WORKERS: Maximum concurrent workers (default: 10)
    WORKER_BATCH_SIZE: Number of topics per API call (default: 5)
    WORKER_POLL_INTERVAL: Seconds between DB polls (default: 10)
"""
import asyncio
import sys
import os

# Add app directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.worker_service import main

if __name__ == "__main__":
    print("Starting Topic Processing Worker Service with Worker Pool...")
    print(f"Max Workers: {os.getenv('WORKER_MAX_WORKERS', '10')}")
    print(f"Batch Size: {os.getenv('WORKER_BATCH_SIZE', '5')}")
    print(f"Poll Interval: {os.getenv('WORKER_POLL_INTERVAL', '10')}s")
    print("-" * 50)
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nWorker service stopped by user.")
    except Exception as e:
        print(f"\nWorker service error: {e}")
        sys.exit(1)
