from dotenv import load_dotenv
import os

load_dotenv()

# Groq (optional)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

# Qdrant config
# - Local (Windows): defaults to http://127.0.0.1:6333
# - Docker compose: set QDRANT_URL=http://qdrant:6333 in the app service
QDRANT_URL = os.getenv("QDRANT_URL")
if not QDRANT_URL:
    host = os.getenv("QDRANT_HOST", "127.0.0.1")
    port = os.getenv("QDRANT_PORT", "6333")
    QDRANT_URL = f"http://{host}:{port}"

QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_TIMEOUT_SECONDS = int(os.getenv("QDRANT_TIMEOUT_SECONDS", "120"))
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "rag_collection")

# Embedding model config
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
VECTOR_SIZE = int(os.getenv("VECTOR_SIZE", "384"))  # must match the model

# Data locations (legacy; most of the web flow uses src/document_ingestion.py)
DATA_INPUT_PATH = os.getenv("DATA_INPUT_PATH", "data")
DATA_OUTPUT_PATH = os.getenv("DATA_OUTPUT_PATH", "data")
