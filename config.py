import os
from pathlib import Path

DATA_DIR = Path(os.getenv("DOCUMIND_DATA", "data"))
CHROMA_DIR = DATA_DIR / "chroma"

EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

LLM_MODELS = [
    m.strip()
    for m in os.getenv(
        "GEMINI_MODELS",
        "gemini-3.5-flash-lite,gemini-3.1-flash-lite,gemini-3.8-flash",
    ).split(",")
    if m.strip()
]

CHUNK_WORDS = 200
CHUNK_OVERLAP = 40
TOP_K = 5
