"""
Client for interacting with Google Gemini API.
"""
import google.generativeai as genai
from typing import Optional, List

class GeminiClient:
    """Handles communication with Gemini models with fallback options."""
    
    # List of models to try in order
    AVAILABLE_MODELS = [
        "models/gemini-2.0-flash-latest",
        "models/gemini-1.5-pro-latest",
        "models/gemini-1.5-flash-latest",
        "models/gemini-1.5-pro",
        "models/gemini-1.5-flash"
    ]
    
    def __init__(self, api_key: str, model: str = None):
        """
        Initialize the Gemini client.
        
        Args:
            api_key: Your Google Gemini API key.
            model: The model to use. If None, will try available models.
        """
        self.api_key = api_key
        genai.configure(api_key=api_key)
        
        if model:
            self.model_name = model
            self.model = genai.GenerativeModel(model)
        else:
            # Try to find a working model
            self.model = None
            self.model_name = None
            self._find_working_model()
    
    def _find_working_model(self):
        """Try different models until one works."""
        for model_name in self.AVAILABLE_MODELS:
            try:
                # Test the model with a simple prompt
                test_model = genai.GenerativeModel(model_name)
                test_response = test_model.generate_content("test", generation_config={"max_output_tokens": 1})
                self.model = test_model
                self.model_name = model_name
                print(f"✅ Using model: {model_name}")
                return
            except Exception as e:
                print(f"❌ Model {model_name} failed: {e}")
                continue
        
        raise Exception("No working Gemini model found. Please check your API key and quota.")
    
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
