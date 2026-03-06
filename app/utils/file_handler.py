"""
Utilities for handling file uploads and temporary files.
"""
import os
import tempfile
import logging
from werkzeug.utils import secure_filename

# Setup logging
logger = logging.getLogger(__name__)

class FileHandler:
    """Handle temporary file storage and cleanup."""
    
    @staticmethod
    def save_temp_file(uploaded_file) -> str:
        """
        Save an uploaded file to a temporary location.
        """
        filename = secure_filename(uploaded_file.filename)
        if not filename:
            filename = "upload.pdf"
        
        temp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        try:
            uploaded_file.save(temp.name)
        finally:
            temp.close()  # Crucial for Windows: close handle so other processes can access
        logger.debug(f"Saved temporary file: {temp.name}")
        return temp.name
    
    @staticmethod
    def cleanup(file_path: str):
        """Remove temporary file."""
        try:
            if os.path.exists(file_path):
                os.unlink(file_path)
                logger.debug(f"Cleaned up temporary file: {file_path}")
        except Exception as e:
            logger.error(f"Cleanup error for {file_path}: {str(e)}")
