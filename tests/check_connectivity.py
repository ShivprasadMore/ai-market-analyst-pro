import os
import sys
import logging
from google import genai
from google.genai import types
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("test")

load_dotenv(override=True)

api_key = os.getenv("GEMINI_API_KEY")
model = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

print(f"Python Version: {sys.version}")
print(f"GEMINI_MODEL: {model}")
print(f"API Key present: {'Yes' if api_key else 'No'}")

client = genai.Client(api_key=api_key)

try:
    print(f"Attempting to call {model} with 60k payload...")
    large_content = "X" * 60000
    response = client.models.generate_content(
        model=model,
        contents=f"Analyze this: {large_content}",
        config=types.GenerateContentConfig(temperature=0)
    )
    print(f"Success! Response: {response.text[:100]}...")
except Exception as e:
    print(f"Error with large payload: {e}")

