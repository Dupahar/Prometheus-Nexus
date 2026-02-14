import os
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

try:
    from google import genai
    print("Successfully imported google.genai")
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY not found")
        exit(1)
        
    print(f"API Key starts with: {api_key[:4]}")
    
    client = genai.Client(api_key=api_key)
    
    print("Attempting to list models (if supported) or generate content...")
    
    try:
        # Try a simple generation
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents="Hello, are you there?"
        )
        print(f"Success! Response: {response.text}")
    except Exception as e:
        print(f"Generation failed: {e}")
        
except ImportError:
    print("Could not import google.genai")
    try:
        import google.generativeai as genai_old
        print("Found google.generativeai instead.")
        print(f"Version: {genai_old.__version__}")
    except ImportError:
        print("Neither SDK found.")
