from __future__ import annotations

import os

try:
    from dotenv import load_dotenv  # type: ignore
except ModuleNotFoundError:
    load_dotenv = None

if load_dotenv:
    load_dotenv()

# Groq API Key (kept for future experiments; not used by the current offline chatbot)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Qdrant config
# IMPORTANT: default to 127.0.0.1 (not localhost) to avoid IPv6 ::1 resolution issues on Windows.
QDRANT_HOST = os.getenv("QDRANT_HOST", "127.0.0.1")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", "6333"))
QDRANT_URL = os.getenv("QDRANT_URL") or f"http://{QDRANT_HOST}:{QDRANT_PORT}"
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

COLLECTION_NAME = "rag_collection"

# Embedding config
# NOTE: We use a hashing-based embedding in src/embeddings.py.
VECTOR_SIZE = 384

# Kept for backward compatibility with older code in the repo.
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
