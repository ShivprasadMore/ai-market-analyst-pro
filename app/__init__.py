"""
Application factory for creating Flask app instance.
"""
import logging
from flask import Flask
from .config import Config

def create_app():
    """Create and configure the Flask application."""
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(Config)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///analyst.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize Database
    from .models.database import db
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
    
    # Validate configuration
    Config.validate()
    
    # Register blueprints (routes)
    from .routes import main_bp
    app.register_blueprint(main_bp)
    
    return app
