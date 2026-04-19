from dotenv import load_dotenv
import os

load_dotenv()

# Groq API Key (for later use with LLM)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Qdrant config
QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "rag_collection"

# Embedding model config
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
VECTOR_SIZE = 384  # IMPORTANT (must match model)
