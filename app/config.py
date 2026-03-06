"""
Application configuration.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(override=True)

class Config:
    """Configuration settings."""
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3-flash-preview")
    
    # Max characters sent to Gemini - reduced slightly to avoid SSL EOF issues
    MAX_INPUT_CHARS = 50_000
    
    # Max file size (16MB)
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024
    
    # Validate required settings
    @classmethod
    def validate(cls):
        """Check that all required configs are present."""
        if not cls.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
