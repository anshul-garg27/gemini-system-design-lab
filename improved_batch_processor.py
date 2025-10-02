#!/usr/bin/env python3
"""
Improved Batch Processor with proper ID tracking and consistency.
Fixes the issue of creating new rows instead of updating existing ones.
"""

import json
import os
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import argparse
import time

from gemini_client import GeminiClient
from improved_unified_database import improved_unified_db


class ImprovedTopicBatchProcessor:
    """Improved processor that maintains ID consistency throughout the workflow."""
    
    def __init__(self, api_keys: List[str] = None, output_dir: str = "output"):
        """Initialize the improved batch processor."""
        self.client = GeminiClient(api_keys)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.db = improved_unified_db
        
    def process_topics_with_consistency(self, topics_input: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Process topics while maintaining ID consistency.
        
        Args:
            topics_input: List of topics with 'title' and optionally 'id'
            
        Returns:
            Processing statistics and results
        """
        stats = {
            'total': len(topics_input),
            'processed': 0,
            'failed': 0,
            'skipped': 0,
            'results': []
        }
        
        # Step 1: Add all topics to topic_status as 'pending'
        topic_status_mappings = []
        for topic_input in topics_input:
            original_title = topic_input.get('title', '')
            if not original_title:
                print(f"Skipping empty title")
                stats['skipped'] += 1
                continue
                
            # Add to topic_status table
            topic_status_id = self.db.add_topic_for_processing(original_title)
            if topic_status_id:
                topic_status_mappings.append({
                    'topic_status_id': topic_status_id,
                    'original_title': original_title,
                    'suggested_id': topic_input.get('id')  # User's suggested ID
                })
                print(f"✅ Added '{original_title}' with status ID: {topic_status_id}")
            else:
                print(f"❌ Failed to add '{original_title}' to processing queue")
                stats['failed'] += 1
        
        # Step 2: Process each topic while carrying the topic_status_id
        for mapping in topic_status_mappings:
            topic_status_id = mapping['topic_status_id']
            original_title = mapping['original_title']
            suggested_id = mapping['suggested_id']
            
            print(f"\n🔄 Processing: {original_title} (Status ID: {topic_status_id})")
            
            # Update status to 'processing'
            self.db.update_topic_status_by_id(topic_status_id, 'processing')
            
            try:
                # Generate content using Gemini
                result = self._generate_single_topic_with_id(
                    original_title=original_title,
                    suggested_id=suggested_id,
                    topic_status_id=topic_status_id
                )
                
                if result['success']:
                    # Update status to 'completed' and save the modified title
                    generated_topic = result['topic']
                    final_title = generated_topic.get('title', original_title)
                    
                    self.db.update_topic_status_by_id(
                        topic_status_id=topic_status_id,
                        status='completed',
                        current_title=final_title
                    )
                    
                    # Save to topics table with foreign key reference
                    saved = self.db.save_generated_topic_with_status_id(
                        topic_data=generated_topic,
                        topic_status_id=topic_status_id
                    )
                    
                    if saved:
                        print(f"✅ Successfully processed and saved: {final_title}")
                        stats['processed'] += 1
                        stats['results'].append({
                            'topic_status_id': topic_status_id,
                            'original_title': original_title,
                            'final_title': final_title,
                            'status': 'completed'
                        })
                    else:
                        raise Exception("Failed to save generated topic")
                        
                else:
                    raise Exception(result.get('error', 'Unknown generation error'))
                    
            except Exception as e:
                error_msg = str(e)
                print(f"❌ Failed to process '{original_title}': {error_msg}")
                
                # Update status to 'failed' with error message
                self.db.update_topic_status_by_id(
                    topic_status_id=topic_status_id,
                    status='failed',
                    error_message=error_msg
                )
                
                stats['failed'] += 1
                stats['results'].append({
                    'topic_status_id': topic_status_id,
                    'original_title': original_title,
                    'status': 'failed',
                    'error': error_msg
                })
        
        return stats
    
    def _generate_single_topic_with_id(self, original_title: str, suggested_id: Optional[int], 
                                     topic_status_id: int) -> Dict[str, Any]:
        """Generate a single topic while maintaining ID references."""
        try:
            # Create topic with suggested ID or auto-generate
            topic_id = suggested_id if suggested_id else self._get_next_available_id()
            
            # Generate using Gemini client
            topics = self.client.generate_topics([{
                'id': topic_id,
                'title': original_title
            }])
            
            if topics and len(topics) > 0:
                generated_topic = topics[0]
                # Ensure the topic has the correct ID
                generated_topic['id'] = topic_id
                
                return {
                    'success': True,
                    'topic': generated_topic,
                    'topic_status_id': topic_status_id
                }
            else:
                return {
                    'success': False,
                    'error': 'No topics generated by Gemini',
                    'topic_status_id': topic_status_id
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'topic_status_id': topic_status_id
            }
    
    def _get_next_available_id(self) -> int:
        """Get next available ID from topics table."""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT MAX(id) FROM topics")
            result = cursor.fetchone()
            max_id = result[0] if result[0] is not None else 0
            return max_id + 1
        finally:
            conn.close()
    
    def process_from_file(self, topics_file: str) -> Dict[str, Any]:
        """Process topics from a JSON file."""
        try:
            with open(topics_file, 'r') as f:
                topics_input = json.load(f)
                
            if not isinstance(topics_input, list):
                raise ValueError("Topics file must contain a JSON array")
                
            return self.process_topics_with_consistency(topics_input)
            
        except Exception as e:
            print(f"Error processing topics file: {e}")
            return {
                'total': 0,
                'processed': 0,
                'failed': 1,
                'skipped': 0,
                'error': str(e),
                'results': []
            }
    
    def get_processing_status(self) -> Dict[str, Any]:
        """Get current processing status from database."""
        return self.db.get_processing_statistics()
    
    def retry_failed_topics(self) -> Dict[str, Any]:
        """Retry all failed topics."""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        try:
            # Get all failed topics
            cursor.execute("""
                SELECT id, original_title 
                FROM topic_status 
                WHERE status = 'failed'
            """)
            failed_topics = cursor.fetchall()
            
            if not failed_topics:
                return {'message': 'No failed topics to retry', 'retried': 0}
            
            # Reset failed topics to pending
            for topic_status_id, original_title in failed_topics:
                self.db.update_topic_status_by_id(
                    topic_status_id=topic_status_id,
                    status='pending',
                    error_message=None
                )
            
            print(f"Reset {len(failed_topics)} failed topics to pending status")
            
            # Process the reset topics
            topics_input = [{'title': title} for _, title in failed_topics]
            return self.process_topics_with_consistency(topics_input)
            
        finally:
            conn.close()


def main():
    """Main CLI interface."""
    parser = argparse.ArgumentParser(description='Improved Topic Batch Processor')
    parser.add_argument('topics_file', help='JSON file containing topics to process')
    parser.add_argument('--output-dir', default='output', help='Output directory for generated files')
    parser.add_argument('--retry-failed', action='store_true', help='Retry failed topics')
    parser.add_argument('--status', action='store_true', help='Show processing status')
    
    args = parser.parse_args()
    
    # Initialize processor
    try:
        from config import API_KEYS
        processor = ImprovedTopicBatchProcessor(api_keys=API_KEYS, output_dir=args.output_dir)
    except ImportError:
        print("Warning: Could not import API_KEYS from config.py")
        processor = ImprovedTopicBatchProcessor(output_dir=args.output_dir)
    
    if args.status:
        # Show processing status
        stats = processor.get_processing_status()
        print("\n📊 Processing Statistics:")
        print(f"Total Topics: {stats['total_topics']}")
        print(f"Completed: {stats['completed']}")
        print(f"Failed: {stats['failed']}")
        print(f"Processing: {stats['processing']}")
        print(f"Pending: {stats['pending']}")
        print(f"Completion Rate: {stats['completion_rate']}%")
        return
    
    if args.retry_failed:
        # Retry failed topics
        print("🔄 Retrying failed topics...")
        result = processor.retry_failed_topics()
        print(f"Retried: {result.get('retried', 0)} topics")
        return
    
    # Process topics from file
    print(f"🚀 Processing topics from: {args.topics_file}")
    result = processor.process_from_file(args.topics_file)
    
    print(f"\n📊 Processing Complete!")
    print(f"Total: {result['total']}")
    print(f"Processed: {result['processed']}")
    print(f"Failed: {result['failed']}")
    print(f"Skipped: {result['skipped']}")


if __name__ == "__main__":
    main()
