"""Check which models work with your key and network, independent of the app."""
from google import genai

from config import LLM_MODELS

client = genai.Client()  # uses GEMINI_API_KEY
for model in LLM_MODELS:
    try:
        r = client.models.generate_content(model=model, contents="Reply with: working")
        print(f"OK    {model}: {r.text.strip()}")
    except Exception as e:
        print(f"FAIL  {model}: {type(e).__name__}: {str(e)[:150]}")