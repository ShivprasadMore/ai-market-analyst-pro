import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

print(f"🔑 API Key loaded: {api_key[:10]}..." if api_key else "❌ No API key found")

if not api_key:
    print("❌ No API key found in .env file")
    exit(1)

# Import our client
from app.core.gemini_client import GeminiClient
from app.config import Config

try:
    # Use our client which now handles configuration and fallback
    client = GeminiClient(api_key=Config.GEMINI_API_KEY, model=Config.GEMINI_MODEL)
    print(f"🔍 Testing with model: {Config.GEMINI_MODEL}")
    
    response = client.generate_content(
        "You are a test assistant.", 
        "Say 'Hello, API is working with gemini-2.5-flash!' in one sentence"
    )
    
    if response:
        print("✅ API test successful!")
        print(f"Response: {response}")
    else:
        print("❌ API test failed: No response")
        
except Exception as e:
    print(f"❌ API test failed: {e}")
