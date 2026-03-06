"""
Client for interacting with Google Gemini API using the new google-genai SDK.
"""
import logging
from google import genai
from google.genai import types
import time
from typing import Optional

# Setup logging
logger = logging.getLogger(__name__)

class GeminiClient:
    """Handles communication with Gemini models with automatic fallback."""
    
    def __init__(self, api_key: str, model: str = "gemini-3-flash-preview"):
        """
        Initialize the Gemini client.
        
        Args:
            api_key: Your Google Gemini API key.
            model: The primary model to use.
        """
        self.api_key = api_key
        self.client = genai.Client(
            api_key=api_key,
            http_options=types.HttpOptions(timeout=120_000)  # 120s timeout in milliseconds
        )
        self.primary_model = model
        # Optimized fallback chain for speed: 3-flash → 3.1-lite → 2.5-lite → 2.5-flash
        self.fallback_models = [
            model,
            "gemini-3-flash-preview",
            "gemini-3.1-flash-lite-preview",
            "gemini-2.5-flash-lite",
            "gemini-2.5-flash",
        ]
        # Remove duplicates while preserving order
        self.fallback_models = list(dict.fromkeys(self.fallback_models))
        logger.info(f"Gemini Client initialized with model preferences: {self.fallback_models}")
    
    def generate_content(self, system_prompt: str, user_content: str) -> Optional[str]:
        """
        Send prompt to Gemini for analysis.
        """
        full_input = f"{system_prompt}\n\nCONTENT TO ANALYZE:\n{user_content}"
        
        last_exception = None
        for model_name in self.fallback_models:
            try:
                logger.info(f"Attempting generation with {model_name}...")
                
                config = types.GenerateContentConfig(
                    response_mime_type="application/json",
                    max_output_tokens=8192,
                    temperature=0.0
                )
                
                response = self.client.models.generate_content(
                    model=model_name,
                    contents=full_input,
                    config=config
                )
                
                if response and response.text:
                    raw_preview = response.text[:100].replace('\n', ' ')
                    logger.info(f"Raw response preview: {raw_preview}")
                    if response.candidates and response.candidates[0].finish_reason:
                        logger.info(f"Finish reason: {response.candidates[0].finish_reason}")
                    if model_name != self.primary_model:
                        logger.info(f"Fallback successful! Used {model_name}")
                    return response.text
                    
            except Exception as e:
                # Handle specific errors if possible, otherwise log and try next
                error_str = str(e).lower()
                
                if "429" in error_str or "exhausted" in error_str:
                    logger.warning(f"Rate limit hit for {model_name}. Trying next model...")
                elif "404" in error_str or "not found" in error_str:
                    logger.warning(f"Model {model_name} not found or inaccessible. Trying next...")
                else:
                    logger.error(f"Unexpected error with {model_name}: {str(e)}")
                
                last_exception = e
                # Small delay to avoid hammering the API
                time.sleep(0.5)
                continue
        
        # If we get here, all models failed
        if last_exception:
            logger.error(f"All models failed. Last error: {str(last_exception)}")
            raise last_exception
        
        return None
