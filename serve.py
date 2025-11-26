#!/usr/bin/env python3
"""
Simple HTTP server to serve the Learn French in Foix website locally.
Run: python serve.py
Then open: http://localhost:8000
"""

import http.server
import socketserver
import os
from pathlib import Path

PORT = 8000
HANDLER = http.server.SimpleHTTPRequestHandler

# Change to the script directory
os.chdir(Path(__file__).parent)

with socketserver.TCPServer(("", PORT), HANDLER) as httpd:
    print(f"✅ Server running at http://localhost:{PORT}")
    print(f"📁 Serving files from: {os.getcwd()}")
    print(f"🌐 Open http://localhost:{PORT} in your browser")
    print(f"❌ Press Ctrl+C to stop the server")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n✓ Server stopped")
