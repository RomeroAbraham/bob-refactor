"""
Run this script to see which Gemini models are available for your API key.
Usage:  python list_models.py
"""
from google import genai

# ← Paste your real API key here (starts with AIza...)
API_KEY = "TU_API_KEY_AQUI"

client = genai.Client(
    api_key=API_KEY,
    http_options={"api_version": "v1"},
)

print("Fetching available models...\n")
try:
    models = list(client.models.list())
    gemini_models = [
        getattr(m, 'name', str(m))
        for m in models
        if 'gemini' in getattr(m, 'name', str(m)).lower()
    ]
    if gemini_models:
        print(f"Found {len(gemini_models)} Gemini models available for your key:\n")
        for name in sorted(gemini_models):
            print(f"  {name}")
    else:
        print("No Gemini models found — check your API key.")
except Exception as e:
    print(f"Error: {e}")
