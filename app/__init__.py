"""
Application factory for creating Flask app instance.
"""
from flask import Flask
from .config import Config

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(Config)
    
    # Validate configuration
    Config.validate()
    
    # Register blueprints (routes)
    from .routes import main_bp
    app.register_blueprint(main_bp)
    
    return app
