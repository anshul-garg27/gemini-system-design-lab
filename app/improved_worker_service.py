"""
Improved Worker service with proper ID tracking and consistency.
Polls database for pending topics and maintains ID throughout processing.
"""
import asyncio
import logging
import os
import signal
import sys
import time
from datetime import datetime
from typing import List, Dict, Any, Tuple
from concurrent.futures import ThreadPoolExecutor
import threading

# Add parent directory to path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unified_database import unified_db
from gemini_client import GeminiClient

logger = logging.getLogger(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


class WorkerPool:
    """Worker pool with capacity tracking for efficient resource management."""
    
    def __init__(self, max_workers: int = 10):
        """Initialize the worker pool."""
        self.max_workers = max_workers
        self.active_workers = 0
        self.available_workers = max_workers
        self.lock = threading.Lock()
        
        logger.info(f"WorkerPool initialized with max_workers={max_workers}")
    
    def can_accept_work(self, work_size: int = 1) -> bool:
        """Check if we can accept new work."""
        with self.lock:
            return self.available_workers >= work_size
    
    def acquire_workers(self, count: int = 1) -> bool:
        """Acquire workers for processing."""
        with self.lock:
            if self.available_workers >= count:
                self.available_workers -= count
                self.active_workers += count
                logger.debug(f"Acquired {count} workers. Available: {self.available_workers}")
                return True
            logger.debug(f"Could not acquire {count} workers. Available: {self.available_workers}")
            return False
    
    def release_workers(self, count: int = 1):
        """Release workers after processing."""
        with self.lock:
            self.active_workers -= count
            self.available_workers += count
            logger.debug(f"Released {count} workers. Available: {self.available_workers}")
    
    def get_status(self) -> Dict[str, int]:
        """Get current worker pool status."""
        with self.lock:
            return {
                'max_workers': self.max_workers,
                'active_workers': self.active_workers,
                'available_workers': self.available_workers,
                'utilization': (self.active_workers / self.max_workers) * 100 if self.max_workers > 0 else 0
            }


class ImprovedTopicWorker:
    """
    Improved worker class with proper ID tracking.
    Polls database and maintains consistency throughout processing.
    """
    
    def __init__(self, max_workers: int = 10, batch_size: int = 5, poll_interval: int = 10):
        """
        Initialize the improved topic worker.
        
        Args:
            max_workers: Maximum number of concurrent workers
            batch_size: Number of topics to process in a single Gemini API call
            poll_interval: Seconds to wait between database polls
        """
        self.worker_pool = WorkerPool(max_workers)
        self.batch_size = batch_size
        self.poll_interval = poll_interval
        self.db = unified_db
        self.gemini_client = GeminiClient()
        self.is_running = False
        
        logger.info(f"ImprovedTopicWorker initialized: max_workers={max_workers}, "
                   f"batch_size={batch_size}, poll_interval={poll_interval}s")
    
    def get_pending_topics_with_ids(self, limit: int = None) -> List[Tuple[int, str]]:
        """
        Get pending topics with their IDs from database.
        
        Returns:
            List of (topic_status_id, title) tuples
        """
        try:
            return self.db.get_pending_topics_with_ids(limit=limit)
        except Exception as e:
            logger.exception(f"Error fetching pending topics: {e}")
            return []
    
    def process_single_topic_with_id(self, topic_status_id: int, title: str) -> Dict[str, Any]:
        """
        Process a single topic while maintaining its ID.
        
        Args:
            topic_status_id: The topic_status table ID
            title: The topic title
            
        Returns:
            Processing result dictionary
        """
        logger.info(f"🔄 Processing topic {topic_status_id}: {title}")
        
        # Update status to 'processing'
        self.db.update_topic_status_by_id(topic_status_id, 'processing')
        
        try:
            # Get next available topic ID for the topics table
            topic_id = self.db.get_next_available_id()
            
            # Generate using Gemini
            topics = self.gemini_client.generate_topics([{
                'id': topic_id,
                'title': title
            }])
            
            if topics and len(topics) > 0:
                generated_topic = topics[0]
                
                # Ensure correct ID
                generated_topic['id'] = topic_id
                
                # Save to topics table
                saved = self.db.save_topic(generated_topic, source='worker_batch')
                
                if saved:
                    # Update status to 'completed'
                    self.db.update_topic_status_by_id(topic_status_id, 'completed')
                    logger.info(f"✅ Successfully processed topic {topic_status_id}: {title}")
                    
                    return {
                        'success': True,
                        'topic_status_id': topic_status_id,
                        'topic_id': topic_id,
                        'title': title,
                        'generated_title': generated_topic.get('title', title)
                    }
                else:
                    raise Exception("Failed to save topic to database")
            else:
                raise Exception("No topics generated by Gemini API")
                
        except Exception as e:
            error_msg = str(e)
            logger.error(f"❌ Failed to process topic {topic_status_id}: {error_msg}")
            
            # Update status to 'failed'
            self.db.update_topic_status_by_id(
                topic_status_id=topic_status_id,
                status='failed',
                error_message=error_msg
            )
            
            return {
                'success': False,
                'topic_status_id': topic_status_id,
                'title': title,
                'error': error_msg
            }
    
    def process_batch_with_ids(self, topics_batch: List[Tuple[int, str]]) -> Dict[str, Any]:
        """
        Process a batch of topics while maintaining their IDs.
        
        Args:
            topics_batch: List of (topic_status_id, title) tuples
            
        Returns:
            Batch processing statistics
        """
        stats = {
            'total': len(topics_batch),
            'processed': 0,
            'failed': 0
        }
        
        logger.info(f"📦 Processing batch of {len(topics_batch)} topics")
        
        # Process each topic in the batch
        for topic_status_id, title in topics_batch:
            result = self.process_single_topic_with_id(topic_status_id, title)
            
            if result['success']:
                stats['processed'] += 1
            else:
                stats['failed'] += 1
            
            # Small delay between topics to avoid rate limiting
            time.sleep(0.5)
        
        logger.info(f"📊 Batch complete: {stats['processed']} processed, {stats['failed']} failed")
        return stats
    
    def process_pending_topics(self):
        """
        Process pending topics using capacity-aware worker pool.
        Maintains ID consistency throughout processing.
        """
        # Check if we have available workers
        if not self.worker_pool.can_accept_work():
            logger.debug("No available workers, skipping this cycle")
            return
        
        # Calculate how many topics we can process
        available_workers = self.worker_pool.available_workers
        max_topics = available_workers * self.batch_size
        
        # Get pending topics WITH IDs
        pending_topics_with_ids = self.get_pending_topics_with_ids(limit=max_topics)
        
        if not pending_topics_with_ids:
            logger.debug("No pending topics found")
            return
        
        logger.info(f"📋 Found {len(pending_topics_with_ids)} pending topics")
        
        # Calculate required workers
        required_workers = (len(pending_topics_with_ids) + self.batch_size - 1) // self.batch_size
        
        # Try to acquire workers
        if not self.worker_pool.acquire_workers(required_workers):
            logger.warning(f"Could not acquire {required_workers} workers, skipping this cycle")
            return
        
        logger.info(f"🔧 Acquired {required_workers} workers for {len(pending_topics_with_ids)} topics")
        
        try:
            # Split into batches
            batches = []
            for i in range(0, len(pending_topics_with_ids), self.batch_size):
                batch = pending_topics_with_ids[i:i + self.batch_size]
                batches.append(batch)
            
            # Process all batches
            total_stats = {'total': 0, 'processed': 0, 'failed': 0}
            
            for batch_idx, batch in enumerate(batches):
                logger.info(f"🔄 Processing batch {batch_idx + 1}/{len(batches)}")
                batch_stats = self.process_batch_with_ids(batch)
                
                total_stats['total'] += batch_stats['total']
                total_stats['processed'] += batch_stats['processed']
                total_stats['failed'] += batch_stats['failed']
            
            logger.info(f"✅ All batches processed: {total_stats['processed']}/{total_stats['total']} successful")
            
        except Exception as e:
            logger.exception(f"Error during batch processing: {e}")
        finally:
            # Always release workers
            self.worker_pool.release_workers(required_workers)
            logger.info(f"🔓 Released {required_workers} workers")
    
    async def run(self):
        """Main worker loop that polls database and processes pending topics."""
        logger.info("🚀 Starting ImprovedTopicWorker...")
        
        self.is_running = True
        
        while self.is_running:
            try:
                # Process pending topics
                self.process_pending_topics()
                
                # Log worker pool status
                status = self.worker_pool.get_status()
                logger.debug(f"📊 Worker pool: {status['available_workers']}/{status['max_workers']} available, "
                           f"{status['utilization']:.1f}% utilization")
                
                # Wait before next poll
                logger.debug(f"⏳ Waiting {self.poll_interval} seconds before next poll...")
                await asyncio.sleep(self.poll_interval)
                
            except Exception as e:
                logger.exception(f"❌ Error in worker loop: {e}")
                await asyncio.sleep(self.poll_interval)
    
    def stop(self):
        """Stop the worker gracefully."""
        logger.info("🛑 Stopping ImprovedTopicWorker...")
        self.is_running = False
        logger.info("✅ ImprovedTopicWorker stopped")


def signal_handler(signum, frame):
    """Handle shutdown signals."""
    logger.info(f"📡 Received signal {signum}, shutting down...")
    if worker:
        worker.stop()
    sys.exit(0)


# Global worker instance
worker = None


async def main():
    """Main entry point for the improved worker service."""
    global worker
    
    # Get configuration from environment variables
    max_workers = int(os.getenv('WORKER_MAX_WORKERS', '10'))
    batch_size = int(os.getenv('WORKER_BATCH_SIZE', '5'))
    poll_interval = int(os.getenv('WORKER_POLL_INTERVAL', '10'))
    
    logger.info("=" * 60)
    logger.info("🚀 IMPROVED WORKER SERVICE - Starting with ID Tracking")
    logger.info(f"⚙️  Configuration:")
    logger.info(f"   - Max Workers: {max_workers}")
    logger.info(f"   - Batch Size: {batch_size}")
    logger.info(f"   - Poll Interval: {poll_interval}s")
    logger.info("=" * 60)
    
    # Create and run improved worker
    worker = ImprovedTopicWorker(
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
