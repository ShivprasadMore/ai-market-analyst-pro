import unittest
from unittest.mock import MagicMock, patch
from app.core.gemini_client import GeminiClient

class TestGeminiClientErrorHandling(unittest.TestCase):
    
    @patch('google.genai.Client')
    def test_rate_limit_fallback(self, mock_client_class):
        """Test that the client tries other models when hitting a rate limit."""
        # Setup mocks
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        
        # Configure model to raise exception (ResourceExhausted equivalent string)
        # First call fails with 429, second succeeds
        mock_client.models.generate_content.side_effect = [
            Exception("429 ResourceExhausted: Rate limit hit"),
            MagicMock(text="Success after fallback")
        ]
        
        # Initialize client
        client = GeminiClient(api_key="fake_key", model="gemini-2.0-flash")
        
        # Call generate_content
        result = client.generate_content("test prompt", "test content")
        
        # Verify result
        self.assertEqual(result, "Success after fallback")
        self.assertEqual(mock_client.models.generate_content.call_count, 2)

    @patch('google.genai.Client')
    def test_invalid_model_fallback(self, mock_client_class):
        """Test that the client tries other models if one is not found (404)."""
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        
        # First call fails with 404, second succeeds
        mock_client.models.generate_content.side_effect = [
            Exception("404 NotFound: Model not found"),
            MagicMock(text="Success after invalid model")
        ]
        
        client = GeminiClient(api_key="fake_key", model="invalid-model")
        result = client.generate_content("test prompt", "test content")
        
        self.assertEqual(result, "Success after invalid model")
        self.assertEqual(mock_client.models.generate_content.call_count, 2)

    @patch('google.genai.Client')
    def test_all_models_exhausted(self, mock_client_class):
        """Test that an Exception is raised if all models fail."""
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        mock_client.models.generate_content.side_effect = Exception("Total exhaustion")
        
        client = GeminiClient(api_key="fake_key")
        
        with self.assertRaises(Exception):
            client.generate_content("test prompt", "test content")

if __name__ == '__main__':
    unittest.main()
