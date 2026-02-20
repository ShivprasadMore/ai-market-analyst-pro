"""
Client for interacting with Google Gemini API.
"""
import google.generativeai as genai
from typing import Optional

class GeminiClient:
    """Handles communication with Gemini models."""
    
    def __init__(self, api_key: str, model: str = "gemini-1.5-pro"):
        """
        Initialize the Gemini client.
        
        Args:
            api_key: Your Google Gemini API key.
            model: The model to use (default: gemini-1.5-pro).
        """
        self.api_key = api_key
        self.model_name = model
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model)
    
    def generate_content(self, prompt: str, text: str) -> Optional[str]:
        """
        Send prompt + text to Gemini and return response.
        
        Args:
            prompt: System prompt / instructions.
            text: The business report text.
            
        Returns:
            Response text, or None if error.
        """
        try:
            full_input = f"{prompt}\n\n{text}"
            response = self.model.generate_content(full_input)
            return response.text
        except Exception as e:
            print(f"Gemini API error: {e}")
            return None
