#!/usr/bin/env python3
"""Minimal Flask test - just responds to health check"""
from flask import Flask

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    return {'status': 'OK', 'message': 'Flask is running'}

if __name__ == '__main__':
    print("Starting minimal Flask server on port 5005...")
    app.run(host='localhost', port=5005, debug=False)
