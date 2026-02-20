"""
Application configuration.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration settings."""
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    
    # Max file size (16MB)
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    
    # Validate required settings
    @classmethod
    def validate(cls):
        """Check that all required configs are present."""
        if not cls.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
