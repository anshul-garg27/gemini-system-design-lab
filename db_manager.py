#!/usr/bin/env python3
"""
Database management utilities for the system design topics database.
"""

import argparse
import json
import sys
from pathlib import Path
from database import TopicsDatabase


def show_stats(db_path: str = None):
    """Show database statistics."""
    db = TopicsDatabase(db_path)
    stats = db.get_topics_stats()
    
    print("Database Statistics")
    print("=" * 50)
    print(f"Total topics: {stats.get('total_topics', 0)}")
    
    if stats.get('by_category'):
        print(f"\nBy Category:")
        for category, count in stats['by_category'].items():
            print(f"  {category}: {count}")
    
    if stats.get('by_complexity'):
        print(f"\nBy Complexity:")
        for complexity, count in stats['by_complexity'].items():
            print(f"  {complexity}: {count}")
    
    print(f"\nRecent processing (24h): {stats.get('recent_processing_24h', 0)}")


def list_topics(db_path: str = None, category: str = None, limit: int = 10):
    """List topics in the database."""
    db = TopicsDatabase(db_path)
    
    if category:
        topics = db.get_topics_by_category(category)
        print(f"Topics in category '{category}':")
    else:
        topics = db.get_all_topics(limit)
        print(f"Recent topics (limit {limit}):")
    
    print("=" * 50)
    
    for topic in topics:
        print(f"ID: {topic['id']}")
        print(f"Title: {topic['title']}")
        print(f"Category: {topic['category']}")
        print(f"Company: {topic['company']}")
        print(f"Complexity: {topic['complexity_level']} (Difficulty: {topic['difficulty']}/10)")
        print(f"Technologies: {', '.join(topic['technologies'])}")
        print(f"Read time: {topic['estimated_read_time']}")
        print("-" * 30)


def show_topic(db_path: str = None, topic_id: int = None):
    """Show detailed information about a specific topic."""
    if not topic_id:
        print("Error: Topic ID required")
        return
    
    db = TopicsDatabase(db_path)
    topic = db.get_topic(topic_id)
    
    if not topic:
        print(f"Topic {topic_id} not found")
        return
    
    print(f"Topic {topic_id}: {topic['title']}")
    print("=" * 50)
    print(f"Description: {topic['description']}")
    print(f"Category: {topic['category']}")
    print(f"Subcategory: {topic['subcategory']}")
    print(f"Company: {topic['company']}")
    print(f"Technologies: {', '.join(topic['technologies'])}")
    print(f"Complexity: {topic['complexity_level']} (Difficulty: {topic['difficulty']}/10)")
    print(f"Tags: {', '.join(topic['tags'])}")
    print(f"Related topics: {topic['related_topics']}")
    print(f"Read time: {topic['estimated_read_time']}")
    print(f"Prerequisites: {', '.join(topic['prerequisites'])}")
    
    print(f"\nMetrics:")
    metrics = topic['metrics']
    print(f"  Scale: {metrics['scale']}")
    print(f"  Performance: {metrics['performance']}")
    print(f"  Reliability: {metrics['reliability']}")
    print(f"  Latency: {metrics['latency']}")
    
    print(f"\nImplementation Details:")
    impl = topic['implementation_details']
    print(f"  Architecture: {impl['architecture']}")
    print(f"  Scaling: {impl['scaling']}")
    print(f"  Storage: {impl['storage']}")
    print(f"  Caching: {impl['caching']}")
    print(f"  Monitoring: {impl['monitoring']}")
    
    print(f"\nLearning Objectives:")
    for i, objective in enumerate(topic['learning_objectives'], 1):
        print(f"  {i}. {objective}")
    
    print(f"\nCreated: {topic['created_date']}")
    print(f"Updated: {topic['updated_date']}")
    print(f"Generated at: {topic['generated_at']}")


def export_topics(db_path: str = None, output_file: str = None):
    """Export all topics to a JSON file."""
    db = TopicsDatabase(db_path)
    export_file = db.export_to_json(output_file)
    print(f"Exported topics to: {export_file}")


def search_topics(db_path: str = None, query: str = None):
    """Search topics by title or description."""
    if not query:
        print("Error: Search query required")
        return
    
    db = TopicsDatabase(db_path)
    topics = db.get_all_topics()
    
    # Simple text search
    matching_topics = []
    query_lower = query.lower()
    
    for topic in topics:
        if (query_lower in topic['title'].lower() or 
            query_lower in topic['description'].lower() or
            query_lower in topic['company'].lower() or
            any(query_lower in tech.lower() for tech in topic['technologies'])):
            matching_topics.append(topic)
    
    print(f"Search results for '{query}':")
    print("=" * 50)
    
    if not matching_topics:
        print("No topics found")
        return
    
    for topic in matching_topics:
        print(f"ID: {topic['id']}")
        print(f"Title: {topic['title']}")
        print(f"Company: {topic['company']}")
        print(f"Category: {topic['category']}")
        print("-" * 30)


def main():
    """Command-line interface for database management."""
    parser = argparse.ArgumentParser(
        description="Manage the system design topics database"
    )
    
    parser.add_argument(
        "--db-path",
        help="Path to SQLite database file (default: topics.db)"
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Stats command
    stats_parser = subparsers.add_parser('stats', help='Show database statistics')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List topics')
    list_parser.add_argument('--category', help='Filter by category')
    list_parser.add_argument('--limit', type=int, default=10, help='Limit number of results')
    
    # Show command
    show_parser = subparsers.add_parser('show', help='Show detailed topic information')
    show_parser.add_argument('topic_id', type=int, help='Topic ID to show')
    
    # Export command
    export_parser = subparsers.add_parser('export', help='Export topics to JSON')
    export_parser.add_argument('--output', help='Output file path')
    
    # Search command
    search_parser = subparsers.add_parser('search', help='Search topics')
    search_parser.add_argument('query', help='Search query')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        if args.command == 'stats':
            show_stats(args.db_path)
        elif args.command == 'list':
            list_topics(args.db_path, args.category, args.limit)
        elif args.command == 'show':
            show_topic(args.db_path, args.topic_id)
        elif args.command == 'export':
            export_topics(args.db_path, args.output)
        elif args.command == 'search':
            search_topics(args.db_path, args.query)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
