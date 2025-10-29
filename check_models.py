import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load your .env file
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# List all available models and their supported methods
print("\nAvailable Gemini Models:\n")
for m in genai.list_models():
    print(f"Name: {m.name}")
    if hasattr(m, "supported_generation_methods"):
        print(f"Supported methods: {m.supported_generation_methods}")
    print("-" * 50)
