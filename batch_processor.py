#!/usr/bin/env python3
"""
Batch processor for generating system design topics using Gemini 2.5 Flash.
Handles reading topics from files, processing in batches, and saving results.
"""

import json
import os
import sys
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
import argparse
import time

from gemini_client import GeminiClient
from database import TopicsDatabase

# Configure logging
logger = logging.getLogger(__name__)


class TopicBatchProcessor:
    """Processes topics in batches using the Gemini client."""
    
    def __init__(self, api_keys: List[str] = None, output_dir: str = "output", db_path: str = None):
        """Initialize the batch processor.
        
        Args:
            api_keys: List of Google AI API keys for rotation
            output_dir: Directory to save generated topic files (optional if using DB)
            db_path: Path to SQLite database (optional)
        """
        self.client = GeminiClient(api_keys)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Initialize database
        self.db = TopicsDatabase(db_path)
        
    def load_topics(self, topics_file: str) -> List[Dict[str, Any]]:
        """Load topics from a JSON file.
        
        Args:
            topics_file: Path to JSON file containing topics
            
        Returns:
            List of topic dictionaries with 'id' and 'title' keys
        """
        try:
            with open(topics_file, 'r') as f:
                topics = json.load(f)
            
            if not isinstance(topics, list):
                raise ValueError("Topics file must contain a JSON array")
            
            # Validate topic structure
            for i, topic in enumerate(topics):
                if not isinstance(topic, dict):
                    raise ValueError(f"Topic {i} must be a dictionary")
                if 'id' not in topic or 'title' not in topic:
                    raise ValueError(f"Topic {i} must have 'id' and 'title' keys")
                if not isinstance(topic['id'], int):
                    raise ValueError(f"Topic {i} 'id' must be an integer")
                if not isinstance(topic['title'], str):
                    raise ValueError(f"Topic {i} 'title' must be a string")
            
            logger.info(f"Loaded {len(topics)} topics from {topics_file}")
            return topics
            
        except FileNotFoundError:
            logger.error(f"Topics file not found: {topics_file}")
            raise FileNotFoundError(f"Topics file not found: {topics_file}")
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in topics file: {e}")
            raise ValueError(f"Invalid JSON in topics file: {e}")
    
    def get_all_topic_ids(self, topics: List[Dict[str, Any]]) -> List[int]:
        """Extract all topic IDs for cross-linking.
        
        Args:
            topics: List of topic dictionaries
            
        Returns:
            List of all topic IDs
        """
        return [topic['id'] for topic in topics]
    
    def process_batch(self, topics_batch: List[Dict[str, Any]], 
                     all_topic_ids: List[int], 
                     created_date: str = None, 
                     updated_date: str = None,
                     delay_seconds: float = 1.0) -> List[Dict[str, Any]]:
        """Process a batch of topics.
        
        Args:
            topics_batch: List of topics to process (max 5)
            all_topic_ids: All available topic IDs for cross-linking
            created_date: ISO date string for creation date
            updated_date: ISO date string for update date
            delay_seconds: Delay between API calls to avoid rate limiting
            
        Returns:
            List of generated topic objects
        """
        if not topics_batch:
            return []
        
        logger.info(f"Processing batch of {len(topics_batch)} topics...")
        
        try:
            result = self.client.generate_topics(
                topics_batch, 
                all_topic_ids, 
                created_date, 
                updated_date
            )
            
            # Handle both single object and array responses
            if isinstance(result, dict):
                return [result]
            elif isinstance(result, list):
                return result
            else:
                raise ValueError(f"Unexpected result type: {type(result)}")
                
        except Exception as e:
            logger.error(f"Error processing batch: {e}", exc_info=True)
            return []
        finally:
            # Add delay to avoid rate limiting
            if delay_seconds > 0:
                time.sleep(delay_seconds)
    
    def save_topic(self, topic: Dict[str, Any], batch_id: str = None, save_to_file: bool = True) -> str:
        """Save a single topic to database and optionally to file.
        
        Args:
            topic: Topic dictionary to save
            batch_id: Optional batch identifier for tracking
            save_to_file: Whether to also save to JSON file
            
        Returns:
            Path to the saved file or database confirmation
        """
        # Save to database
        db_success = self.db.save_topic(topic, batch_id)
        
        if not db_success:
            logger.warning(f"Failed to save topic {topic['id']} to database")
        
        # Optionally save to file
        if save_to_file:
            topic_id = topic['id']
            filename = f"{topic_id}.json"
            filepath = self.output_dir / filename
            
            try:
                with open(filepath, 'w') as f:
                    json.dump(topic, f, indent=2)
                logger.debug(f"Saved topic {topic_id} to file {filepath}")
                return str(filepath)
            except Exception as e:
                logger.warning(f"Failed to save topic {topic_id} to file: {e}")
                return f"Database only (file save failed)"
        else:
            return "Database only"
    
    def process_all_topics(self, topics_file: str, 
                          batch_size: int = 5,
                          created_date: str = None,
                          updated_date: str = None,
                          delay_seconds: float = 1.0,
                          save_to_file: bool = True) -> Dict[str, Any]:
        """Process all topics from a file in batches.
        
        Args:
            topics_file: Path to JSON file containing topics
            batch_size: Number of topics to process per batch (max 5)
            created_date: ISO date string for creation date
            updated_date: ISO date string for update date
            delay_seconds: Delay between API calls
            save_to_file: Whether to save topics to JSON files in addition to database
            
        Returns:
            Summary dictionary with processing results
        """
        # Load topics
        topics = self.load_topics(topics_file)
        all_topic_ids = self.get_all_topic_ids(topics)
        
        logger.info(f"Loaded {len(topics)} topics from {topics_file}")
        logger.info(f"Processing in batches of {min(batch_size, 5)}")
        
        # Set default dates
        today = datetime.now().strftime("%Y-%m-%d")
        created_date = created_date or today
        updated_date = updated_date or today
        
        # Process in batches
        successful_topics = []
        failed_topics = []
        batch_id = f"batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        for i in range(0, len(topics), batch_size):
            batch = topics[i:i + batch_size]
            batch_num = (i // batch_size) + 1
            total_batches = (len(topics) + batch_size - 1) // batch_size
            
            logger.info(f"Processing batch {batch_num}/{total_batches}: {[t['id'] for t in batch]}")
            
            generated_topics = self.process_batch(
                batch, 
                all_topic_ids, 
                created_date, 
                updated_date,
                delay_seconds
            )
            
            # Save successful topics
            for topic in generated_topics:
                try:
                    filepath = self.save_topic(topic, batch_id, save_to_file)
                    successful_topics.append({
                        'id': topic['id'],
                        'title': topic['title'],
                        'file': filepath
                    })
                    logger.info(f"✓ Saved topic {topic['id']}: {topic['title']}")
                except Exception as e:
                    failed_topics.append({
                        'id': topic.get('id', 'unknown'),
                        'title': topic.get('title', 'unknown'),
                        'error': str(e)
                    })
                    logger.error(f"✗ Failed to save topic {topic.get('id', 'unknown')}: {e}")
        
        # Get database stats
        db_stats = self.db.get_topics_stats()
        
        # Return summary
        return {
            'total_topics': len(topics),
            'successful': len(successful_topics),
            'failed': len(failed_topics),
            'successful_topics': successful_topics,
            'failed_topics': failed_topics,
            'output_directory': str(self.output_dir),
            'database_path': self.db.db_path,
            'database_stats': db_stats,
            'batch_id': batch_id
        }


def main():
    """Command-line interface for the batch processor."""
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('batch_processor.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    parser = argparse.ArgumentParser(
        description="Generate system design topics using Gemini 2.5 Flash"
    )
    parser.add_argument(
        "topics_file",
        help="JSON file containing topics to process"
    )
    parser.add_argument(
        "--output-dir",
        default="output",
        help="Directory to save generated topics (default: output)"
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=5,
        help="Number of topics per batch (max 5, default: 5)"
    )
    parser.add_argument(
        "--created-date",
        help="Creation date in YYYY-MM-DD format (default: today)"
    )
    parser.add_argument(
        "--updated-date",
        help="Update date in YYYY-MM-DD format (default: today)"
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=1.0,
        help="Delay between API calls in seconds (default: 1.0)"
    )
    parser.add_argument(
        "--api-keys",
        nargs="+",
        help="Google AI API keys for rotation (or use config.py)"
    )
    parser.add_argument(
        "--db-path",
        help="Path to SQLite database file (default: topics.db)"
    )
    parser.add_argument(
        "--db-only",
        action="store_true",
        help="Save only to database, skip JSON files"
    )
    
    args = parser.parse_args()
    
    # Validate batch size
    if args.batch_size > 5:
        logger.warning("Batch size limited to 5 by Gemini API")
        args.batch_size = 5
    
    try:
        processor = TopicBatchProcessor(
            api_keys=args.api_keys,
            output_dir=args.output_dir,
            db_path=args.db_path
        )
        
        summary = processor.process_all_topics(
            topics_file=args.topics_file,
            batch_size=args.batch_size,
            created_date=args.created_date,
            updated_date=args.updated_date,
            delay_seconds=args.delay,
            save_to_file=not args.db_only
        )
        
        print(f"\n{'='*50}")
        print("PROCESSING SUMMARY")
        print(f"{'='*50}")
        print(f"Total topics: {summary['total_topics']}")
        print(f"Successful: {summary['successful']}")
        print(f"Failed: {summary['failed']}")
        print(f"Output directory: {summary['output_directory']}")
        print(f"Database path: {summary['database_path']}")
        
        # Show database stats
        db_stats = summary.get('database_stats', {})
        if db_stats:
            print(f"\nDatabase Statistics:")
            print(f"  Total topics in DB: {db_stats.get('total_topics', 0)}")
            print(f"  By category: {db_stats.get('by_category', {})}")
            print(f"  By complexity: {db_stats.get('by_complexity', {})}")
            print(f"  Recent processing (24h): {db_stats.get('recent_processing_24h', 0)}")
        
        if summary['failed_topics']:
            print(f"\nFailed topics:")
            for failed in summary['failed_topics']:
                print(f"  - {failed['id']}: {failed['error']}")
        
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
