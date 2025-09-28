#!/usr/bin/env python3
"""
Simple test Flask server to debug the issue
"""

from flask import Flask, jsonify
from unified_database import unified_db

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({'status': 'ok', 'message': 'Flask server is running'})

@app.route('/api/stats')
def stats():
    try:
        stats_data = unified_db.get_stats()
        return jsonify(stats_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/topics')
def topics():
    try:
        topics_data = unified_db.get_topics_paginated(limit=5, offset=0)
        return jsonify(topics_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Starting test Flask server on port 5002...")
    app.run(host='0.0.0.0', port=5002, debug=True)
