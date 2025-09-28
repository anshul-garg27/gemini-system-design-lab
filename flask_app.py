#!/usr/bin/env python3
"""
Flask web application for the System Design Topic Generator.
Provides a beautiful UI for bulk topic entry, progress tracking, and analytics.
"""

import os
import json
import threading
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import sqlite3
from unified_database import unified_db
from gemini_client import GeminiClient
from batch_processor import TopicBatchProcessor


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Global variables for processing
processing_status = {
    'is_processing': False,
    'current_batch': 0,
    'total_batches': 0,
    'processed_topics': 0,
    'failed_topics': 0,
    'skipped_topics': 0,
    'skipped_titles': [],
    'current_topic': None,
    'errors': []
}

# Initialize database and processor
db = unified_db
processor = None


def init_processor():
    """Initialize the batch processor."""
    global processor
    try:
        processor = TopicBatchProcessor()
        return True
    except Exception as e:
        print(f"Error initializing processor: {e}")
        return False


def update_processing_status(status_update):
    """Update processing status and emit to clients."""
    global processing_status
    processing_status.update(status_update)
    socketio.emit('status_update', processing_status)


def process_single_batch(batch, batch_num, all_topic_ids):
    """Process a single batch of topics."""
    try:
        # Generate topics using Gemini
        generated_topics = processor.client.generate_topics(
            batch, 
            all_topic_ids=all_topic_ids,
            created_date=datetime.now().strftime("%Y-%m-%d"),
            updated_date=datetime.now().strftime("%Y-%m-%d")
        )
        
        # Small delay to respect rate limits
        time.sleep(1.0)
        
        # Handle response (single topic or list)
        if isinstance(generated_topics, dict):
            generated_topics = [generated_topics]
        
        return {
            'batch_num': batch_num,
            'success': True,
            'topics': generated_topics,
            'error': None
        }
    except Exception as e:
        return {
            'batch_num': batch_num,
            'success': False,
            'topics': [],
            'error': str(e)
        }


def process_topics_background(topic_titles, batch_size=5):
    """Process topics in background thread."""
    global processing_status
    
    try:
        # Initialize processor
        if not init_processor():
            update_processing_status({
                'is_processing': False,
                'errors': ['Failed to initialize processor']
            })
            return
        
        # Filter out topics that already exist and are completed
        topics_to_process = []
        skipped_topics = []
        retry_topics = []
        
        # Get the next available ID to avoid conflicts
        next_id = db.get_next_available_id()
        
        for i, title in enumerate(topic_titles):
            title = title.strip()
            
            # Check if topic already exists
            existing_topic = db.get_topic_by_title(title)
            
            if existing_topic:
                if existing_topic.get('status') == 'completed':
                    skipped_topics.append(title)
                    print(f"Skipping existing completed topic: {title}")
                    continue
                elif existing_topic.get('status') in ['failed', 'pending']:
                    retry_topics.append({
                        'id': existing_topic['id'],
                        'title': title,
                        'status': 'pending',
                        'created_at': datetime.now().isoformat()
                    })
                    print(f"Retrying existing topic with status '{existing_topic.get('status')}': {title}")
                    continue
            
            # Use sequential IDs starting from next available ID
            topic_id = next_id + i
            topics_to_process.append({
                'id': topic_id,
                'title': title,
                'status': 'pending',
                'created_at': datetime.now().isoformat()
            })
        
        # Combine new topics and retry topics
        all_topics_to_process = topics_to_process + retry_topics
        
        # If no topics to process, return early
        if not all_topics_to_process:
            update_processing_status({
                'is_processing': False,
                'processed_topics': len(skipped_topics),
                'skipped_topics': len(skipped_topics),
                'current_topic': f'All {len(skipped_topics)} topics already exist and are completed!'
            })
            return
        
        # Save topics to process with pending status
        for topic in all_topics_to_process:
            db.save_topic_status(topic['title'], 'pending', None)
        
        # Update status with skipped topics info
        if skipped_topics:
            update_processing_status({
                'skipped_topics': len(skipped_topics),
                'skipped_titles': skipped_topics[:5]  # Show first 5 skipped topics
            })
        
        # Calculate batches
        total_batches = (len(all_topics_to_process) + batch_size - 1) // batch_size
        
        update_processing_status({
            'is_processing': True,
            'current_batch': 0,
            'total_batches': total_batches,
            'processed_topics': len(skipped_topics),  # Count skipped as processed
            'failed_topics': 0,
            'current_topic': None,
            'errors': []
        })
        
        # Process in parallel batches
        all_topic_ids = [t['id'] for t in all_topics_to_process]
        
        # Calculate parallel processing parameters
        parallel_batches = min(10, total_batches)  # Max 10 parallel batches
        batch_groups = []
        
        # Group batches for parallel processing
        for i in range(0, total_batches, parallel_batches):
            group_batches = []
            for batch_num in range(i, min(i + parallel_batches, total_batches)):
                start_idx = batch_num * batch_size
                end_idx = min(start_idx + batch_size, len(all_topics_to_process))
                batch = all_topics_to_process[start_idx:end_idx]
                group_batches.append((batch_num, batch))
            batch_groups.append(group_batches)
        
        # Process each group of batches in parallel
        for group_idx, batch_group in enumerate(batch_groups):
            update_processing_status({
                'current_batch': group_idx + 1,
                'total_batches': len(batch_groups),
                'current_topic': f"Processing parallel group {group_idx + 1}/{len(batch_groups)} ({len(batch_group)} batches)"
            })
            
            # Process batches in parallel using ThreadPoolExecutor
            with ThreadPoolExecutor(max_workers=parallel_batches) as executor:
                # Submit all batches in this group for parallel processing
                future_to_batch = {}
                for batch_num, batch in batch_group:
                    future = executor.submit(process_single_batch, batch, batch_num, all_topic_ids)
                    future_to_batch[future] = (batch_num, batch)
                
                # Collect results as they complete
                batch_results = []
                for future in as_completed(future_to_batch):
                    batch_num, batch = future_to_batch[future]
                    try:
                        result = future.result()
                        batch_results.append(result)
                        print(f"Batch {batch_num + 1} completed successfully")
                    except Exception as e:
                        print(f"Batch {batch_num + 1} failed: {e}")
                        batch_results.append({
                            'batch_num': batch_num,
                            'success': False,
                            'error': str(e),
                            'topics': []
                        })
                
                # Process all results from this parallel group
                for result in batch_results:
                    if result['success']:
                        generated_topics = result['topics']
                        
                        # Save successful topics
                        for topic in generated_topics:
                            try:
                                db.save_topic(topic, f"web_batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
                                db.save_topic_status(topic['title'], 'completed', None)
                                
                                processing_status['processed_topics'] += 1
                                update_processing_status({
                                    'processed_topics': processing_status['processed_topics']
                                })
                            except Exception as e:
                                db.save_topic_status(topic['title'], 'failed', str(e))
                                processing_status['failed_topics'] += 1
                                update_processing_status({
                                    'failed_topics': processing_status['failed_topics']
                                })
                    else:
                        # Handle failed batch
                        for topic in batch_group[result['batch_num']][1]:  # Get the batch topics
                            db.save_topic_status(topic['title'], 'failed', result['error'])
                            processing_status['failed_topics'] += 1
                        
                        update_processing_status({
                            'failed_topics': processing_status['failed_topics'],
                            'errors': processing_status['errors'] + [f"Batch {result['batch_num'] + 1} failed: {result['error']}"]
                        })
        
        # Processing complete
        update_processing_status({
            'is_processing': False,
            'current_topic': 'Processing complete!'
        })
        
    except Exception as e:
        update_processing_status({
            'is_processing': False,
            'errors': [f"Processing failed: {str(e)}"]
        })


@app.route('/')
def index():
    """Main dashboard page."""
    stats = db.get_topics_stats()
    return render_template('index.html', stats=stats)


@app.route('/topics')
def topics():
    """Topics management page."""
    page = request.args.get('page', 1, type=int)
    per_page = 20
    offset = (page - 1) * per_page
    
    topics_data = db.get_topics_paginated(offset, per_page)
    total_topics = db.get_total_topics_count()
    
    return render_template('topics.html', 
                         topics=topics_data, 
                         page=page, 
                         per_page=per_page,
                         total_topics=total_topics)


@app.route('/analytics')
def analytics():
    """Analytics dashboard page."""
    stats = db.get_detailed_stats()
    # Ensure we have all required fields with defaults
    if not stats:
        stats = {
            'total_topics': 0,
            'status_breakdown': {'completed': 0, 'pending': 0, 'failed': 0},
            'category_breakdown': {},
            'complexity_breakdown': {},
            'daily_stats': [],
            'company_breakdown': {}
        }
    return render_template('analytics.html', stats=stats)


@app.route('/api/topics', methods=['POST'])
def create_topics():
    """API endpoint to create topics from bulk input."""
    data = request.get_json()
    topic_titles = data.get('topics', [])
    batch_size = data.get('batch_size', 5)
    
    # Validate batch size (per API call)
    if not isinstance(batch_size, int) or batch_size < 1 or batch_size > 5:
        return jsonify({'error': 'Batch size must be between 1 and 5 topics per API call'}), 400
    
    if not topic_titles:
        return jsonify({'error': 'No topics provided'}), 400
    
    if processing_status['is_processing']:
        return jsonify({'error': 'Already processing topics'}), 400
    
    # Start background processing
    thread = threading.Thread(
        target=process_topics_background, 
        args=(topic_titles, batch_size)
    )
    thread.daemon = True
    thread.start()
    
    return jsonify({'message': 'Processing started', 'total_topics': len(topic_titles)})


@app.route('/api/topics', methods=['GET'])
def get_topics():
    """API endpoint to get topics with pagination, search, and filtering."""
    limit = request.args.get('limit', 5, type=int)
    offset = request.args.get('offset', 0, type=int)
    
    # Search and filter parameters
    search = request.args.get('search', '').strip()
    category = request.args.get('category', '').strip()
    status = request.args.get('status', '').strip()
    complexity = request.args.get('complexity', '').strip()
    company = request.args.get('company', '').strip()
    sort_by = request.args.get('sort_by', 'created_date').strip()
    sort_order = request.args.get('sort_order', 'desc').strip()
    
    # Get topics with search and filters
    topics = db.get_topics_paginated(
        offset=offset, 
        limit=limit,
        search=search,
        category=category,
        status=status,
        complexity=complexity,
        company=company,
        sort_by=sort_by,
        sort_order=sort_order
    )
    
    # Get total count for pagination (with same filters)
    total_count = db.get_topics_count(
        search=search,
        category=category,
        status=status,
        complexity=complexity,
        company=company
    )
    
    return jsonify({
        'topics': topics,
        'total_count': total_count,
        'limit': limit,
        'offset': offset
    })


@app.route('/api/status')
def get_status():
    """API endpoint to get current processing status."""
    return jsonify(processing_status)


@app.route('/api/topics/<int:topic_id>')
def get_topic(topic_id):
    """API endpoint to get a specific topic."""
    topic = db.get_topic(topic_id)
    if not topic:
        return jsonify({'error': 'Topic not found'}), 404
    return jsonify(topic)


@app.route('/api/topics/<int:topic_id>', methods=['DELETE'])
def delete_topic(topic_id):
    """API endpoint to delete a topic."""
    try:
        # Delete from database
        success = db.delete_topic(topic_id)
        if success:
            return jsonify({'message': 'Topic deleted successfully'})
        else:
            return jsonify({'error': 'Topic not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/topics/<int:topic_id>/retry', methods=['POST'])
def retry_topic(topic_id):
    """API endpoint to retry processing a failed topic."""
    topic_status = db.get_topic_status(topic_id)
    if not topic_status:
        return jsonify({'error': 'Topic not found'}), 404
    
    if topic_status['status'] != 'failed':
        return jsonify({'error': 'Topic is not in failed status'}), 400
    
    # Retry processing
    try:
        if not processor:
            init_processor()
        
        topic_data = [{'id': topic_id, 'title': topic_status['title']}]
        all_ids = [topic_id]
        
        result = processor.client.generate_topics(topic_data, all_ids)
        
        if isinstance(result, dict):
            result = [result]
        
        for topic in result:
            db.save_topic(topic, f"retry_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
            db.save_topic_status(topic_status['title'], 'completed', None)
        
        return jsonify({'message': 'Topic processed successfully'})
        
    except Exception as e:
        db.save_topic_status(topic_status['title'], 'failed', str(e))
        return jsonify({'error': str(e)}), 500


@app.route('/api/stats')
def get_stats():
    """API endpoint to get database statistics."""
    return jsonify(db.get_topics_stats())


@socketio.on('connect')
def handle_connect():
    """Handle client connection."""
    emit('status_update', processing_status)


# Template helper functions
@app.route('/api/cleanup-failed', methods=['POST'])
def cleanup_failed_topics():
    """Clean up failed topics from the database."""
    try:
        cleaned_count = db.cleanup_failed_topics()
        return jsonify({
            'success': True,
            'message': f'Cleaned up {cleaned_count} failed topics',
            'cleaned_count': cleaned_count
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/topic-status-summary')
def get_topic_status_summary():
    """Get a summary of topic statuses."""
    try:
        summary = db.get_topic_status_summary()
        return jsonify({
            'success': True,
            'summary': summary
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.template_filter('get_complexity_badge_class')
def get_complexity_badge_class(complexity):
    classes = {
        'beginner': 'bg-success',
        'intermediate': 'bg-warning', 
        'advanced': 'bg-danger',
        'expert': 'bg-dark'
    }
    return classes.get(complexity, 'bg-secondary')


@app.template_filter('get_status_badge_class')
def get_status_badge_class(status):
    classes = {
        'completed': 'bg-success',
        'pending': 'bg-warning',
        'failed': 'bg-danger'
    }
    return classes.get(status, 'bg-secondary')


@app.template_filter('get_status_icon')
def get_status_icon(status):
    icons = {
        'completed': 'check-circle',
        'pending': 'clock',
        'failed': 'exclamation-triangle'
    }
    return icons.get(status, 'question-circle')


@app.template_filter('get_status_color')
def get_status_color(status):
    colors = {
        'completed': 'success',
        'pending': 'warning',
        'failed': 'danger'
    }
    return colors.get(status, 'secondary')


if __name__ == '__main__':
    # Initialize processor
    init_processor()
    
    # Run the application
    socketio.run(app, debug=True, host='0.0.0.0', port=5001)
