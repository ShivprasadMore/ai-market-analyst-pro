#!/usr/bin/env python
"""
Entry point for running the Flask application.
"""
from app import create_app

app = create_app()

if __name__ == '__main__':
    # Run in debug mode for development
    # Set debug=False in production
    app.run(debug=True, host='0.0.0.0', port=5000)
