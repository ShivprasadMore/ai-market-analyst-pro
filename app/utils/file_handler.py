"""
Utilities for handling file uploads and temporary files.
"""
import os
import tempfile
from werkzeug.utils import secure_filename

class FileHandler:
    """Handle temporary file storage and cleanup."""
    
    @staticmethod
    def save_temp_file(uploaded_file) -> str:
        """
        Save an uploaded file to a temporary location.
        
        Args:
            uploaded_file: The file object from Flask request.
            
        Returns:
            Path to the temporary file.
        """
        # Create a temporary file with a secure name
        filename = secure_filename(uploaded_file.filename)
        if not filename:
            filename = "upload.pdf"
        
        # Create temp file with .pdf suffix
        temp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        uploaded_file.save(temp.name)
        return temp.name
    
    @staticmethod
    def cleanup(file_path: str):
        """Remove temporary file."""
        try:
            if os.path.exists(file_path):
                os.unlink(file_path)
                print(f"Cleaned up: {file_path}")
        except Exception as e:
            print(f"Cleanup error: {e}")
