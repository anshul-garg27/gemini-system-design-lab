"""
Worker service for processing pending topics in the background.
Uses a worker pool with capacity tracking to only process topics when workers are available.
"""
import asyncio
import logging
import os
import signal
import sys
import time
from datetime import datetime
from typing import List, Dict, Any
from concurrent.futures import ThreadPoolExecutor
import threading

# Add parent directory to path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unified_database import UnifiedDatabase
from gemini_client import GeminiClient
from batch_processor import TopicBatchProcessor
from app.routes_topics import process_topics_background, processing_status, status_lock

logger = logging.getLogger(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


class WorkerPool:
    """Worker pool with capacity tracking for efficient resource management."""
    
    def __init__(self, max_workers: int = 10):
        """
        Initialize the worker pool.
        
        Args:
            max_workers: Maximum number of concurrent workers
        """
        self.max_workers = max_workers
        self.active_workers = 0
        self.available_workers = max_workers
        self.lock = threading.Lock()
        
        logger.info(f"WorkerPool initialized with max_workers={max_workers}")
    
    def can_accept_work(self, work_size: int = 1) -> bool:
        """
        Check if we can accept new work.
        
        Args:
            work_size: Number of workers needed for the work
            
        Returns:
            True if we can accept the work, False otherwise
        """
        with self.lock:
            return self.available_workers >= work_size
    
    def acquire_workers(self, count: int = 1) -> bool:
        """
        Acquire workers for processing.
        
        Args:
            count: Number of workers to acquire
            
        Returns:
            True if workers were acquired successfully, False otherwise
        """
        with self.lock:
            if self.available_workers >= count:
                self.available_workers -= count
                self.active_workers += count
                logger.debug(f"Acquired {count} workers. Available: {self.available_workers}, Active: {self.active_workers}")
                return True
            logger.debug(f"Could not acquire {count} workers. Available: {self.available_workers}")
            return False
    
    def release_workers(self, count: int = 1):
        """
        Release workers after processing.
        
        Args:
            count: Number of workers to release
        """
        with self.lock:
            self.active_workers -= count
            self.available_workers += count
            logger.debug(f"Released {count} workers. Available: {self.available_workers}, Active: {self.active_workers}")
    
    def get_status(self) -> Dict[str, int]:
        """
        Get current worker pool status.
        
        Returns:
            Dictionary with worker pool statistics
        """
        with self.lock:
            return {
                'max_workers': self.max_workers,
                'active_workers': self.active_workers,
                'available_workers': self.available_workers,
                'utilization': (self.active_workers / self.max_workers) * 100 if self.max_workers > 0 else 0
            }


class TopicWorker:
    """Worker class for processing pending topics with capacity-aware processing."""
    
    def __init__(self, max_workers: int = 10, batch_size: int = 5, poll_interval: int = 10):
        """
        Initialize the topic worker.
        
        Args:
            max_workers: Maximum number of concurrent workers
            batch_size: Number of topics to process in a single Gemini API call
            poll_interval: Seconds to wait between database polls
        """
        self.worker_pool = WorkerPool(max_workers)
        self.batch_size = batch_size
        self.poll_interval = poll_interval
        self.db = UnifiedDatabase()  # Create instance, not just reference to class
        self.is_running = False
        
        logger.info(f"TopicWorker initialized with max_workers={max_workers}, batch_size={batch_size}, poll_interval={poll_interval}s")
    
    def get_pending_topics(self, limit: int = None) -> List[str]:
        """
        Get pending topic titles from the database.
        Now includes topic_status_id tracking for consistency.
        
        Args:
            limit: Maximum number of topics to fetch
            
        Returns:
            List of pending topic titles
            Note: Topics now have topic_status_id embedded, which will be
            carried through the process_topics_background workflow
        """
        try:
            # Get all topics with pending status (now includes topic_status_id)
            topics = self.db.get_topics_by_status('pending', limit=limit)
            
            # Log the topic_status_ids being processed
            if topics:
                logger.info(f"Fetched {len(topics)} pending topics with IDs: {[t.get('topic_status_id') for t in topics]}")
            
            # Extract just the titles for process_topics_background
            # Note: The process_topics_background will re-fetch topic_status_id
            # using get_topic_status_by_title, so ID tracking is maintained
            return [topic['title'] for topic in topics]
        except Exception as e:
            logger.exception(f"Error fetching pending topics: {e}")
            return []
    
    def process_pending_topics(self):
        """
        Process pending topics using capacity-aware worker pool.
        Only processes topics when workers are available.
        """
        # Check if we have available workers
        if not self.worker_pool.can_accept_work():
            logger.debug("No available workers, skipping this cycle")
            return
        
        # Calculate how many topics we can process based on available workers
        available_workers = self.worker_pool.available_workers
        max_topics = available_workers * self.batch_size
        
        # Get limited pending topic titles based on available capacity
        pending_titles = self.get_pending_topics(limit=max_topics)
        
        if not pending_titles:
            logger.debug("No pending topics found")
            return
        
        # Calculate required workers for this batch
        required_workers = (len(pending_titles) + self.batch_size - 1) // self.batch_size
        
        # Try to acquire workers for this batch
        if not self.worker_pool.acquire_workers(required_workers):
            logger.warning(f"Could not acquire {required_workers} workers, skipping this cycle")
            return
        
        logger.info(f"Acquired {required_workers} workers for {len(pending_titles)} topics, starting processing...")
        
        # Process with acquired workers
        try:
            # Use the existing process_topics_background function
            # This will handle all the parallel processing, status updates, etc.
            process_topics_background(pending_titles, self.batch_size)
            
            # Wait for processing to complete
            while True:
                with status_lock:
                    if not processing_status['is_processing']:
                        logger.info("Processing completed")
                        break
                time.sleep(2)
                
        except Exception as e:
            logger.exception(f"Error during processing: {e}")
        finally:
            # Always release workers
            self.worker_pool.release_workers(required_workers)
            logger.info(f"Released {required_workers} workers")
    
    async def run(self):
        """
        Main worker loop that polls the database and processes pending topics.
        """
        logger.info("Starting TopicWorker...")
        
        self.is_running = True
        
        while self.is_running:
            try:
                # Process pending topics
                self.process_pending_topics()
                
                # Log worker pool status
                status = self.worker_pool.get_status()
                logger.debug(f"Worker pool status: {status['available_workers']}/{status['max_workers']} available, {status['utilization']:.1f}% utilization")
                
                # Wait before next poll
                logger.debug(f"Waiting {self.poll_interval} seconds before next poll...")
                await asyncio.sleep(self.poll_interval)
                
            except Exception as e:
                logger.exception(f"Error in worker loop: {e}")
                await asyncio.sleep(self.poll_interval)
    
    def stop(self):
        """Stop the worker gracefully."""
        logger.info("Stopping TopicWorker...")
        self.is_running = False
        logger.info("TopicWorker stopped")


def signal_handler(signum, frame):
    """Handle shutdown signals."""
    logger.info(f"Received signal {signum}, shutting down...")
    if worker:
        worker.stop()
    sys.exit(0)


# Global worker instance
worker = None


async def main():
    """Main entry point for the worker service."""
    global worker
    
    # Get configuration from environment variables
    max_workers = int(os.getenv('WORKER_MAX_WORKERS', '80'))
    batch_size = int(os.getenv('WORKER_BATCH_SIZE', '5'))
    poll_interval = int(os.getenv('WORKER_POLL_INTERVAL', '10'))
    
    # Create and run worker
    worker = TopicWorker(
        max_workers=max_workers,
        batch_size=batch_size,
        poll_interval=poll_interval
    )
    
    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Run worker
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
