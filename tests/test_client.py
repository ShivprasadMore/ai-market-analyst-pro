import os
from dotenv import load_dotenv
from app.core.gemini_client import GeminiClient

def test_gemini():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ GEMINI_API_KEY not found in .env")
        return

    client = GeminiClient(api_key=api_key)
    print("Testing generate_content...")
    try:
        response = client.generate_content("You are a helpful assistant.", "Say 'Hello, I am working!'")
        if response:
            print(f"✅ Success! Response: {response}")
        else:
            print("❌ No response received.")
    except Exception as e:
        print(f"❌ Error during test: {e}")

if __name__ == "__main__":
    test_gemini()
