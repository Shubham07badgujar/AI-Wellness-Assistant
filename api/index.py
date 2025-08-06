"""
Vercel serverless function for AI Wellness Assistant
"""

import sys
import os
from pathlib import Path

# Add the parent directory to the path so we can import our modules
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.insert(0, str(parent_dir))

# Import the Flask app
from web_server import app

# For Vercel, we need to export the app as the default export
# Vercel will handle the WSGI interface
def handler(environ, start_response):
    return app(environ, start_response)

# Also make the app available directly
application = app

if __name__ == "__main__":
    app.run(debug=False)
