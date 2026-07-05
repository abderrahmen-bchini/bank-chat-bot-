from typing import Any

from groq import Groq
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

from config import (
    COLLECTION_NAME,
    EMBEDDING_MODEL,
    GROQ_API_KEY,
    GROQ_MODEL,
    QDRANT_API_KEY,
    QDRANT_TIMEOUT_SECONDS,
    QDRANT_URL,
)

llm = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

_qdrant_kwargs: dict[str, Any] = {"url": QDRANT_URL, "timeout": QDRANT_TIMEOUT_SECONDS}
if QDRANT_API_KEY:
    _qdrant_kwargs["api_key"] = QDRANT_API_KEY
qdrant = QdrantClient(**_qdrant_kwargs)

embedder = SentenceTransformer(f"sentence-transformers/{EMBEDDING_MODEL}")

SYSTEM_PROMPT = (
    "you are a helpful assistant."
    "Answer using the provided context when relevant."
    "if the context does not contain the answer , say so."
)

def _search_qdrant(query_vector: list[float], limit: int = 5):
    """Compatibility wrapper for qdrant-client versions."""
    if hasattr(qdrant, "query_points"):
        result = qdrant.query_points(
            collection_name=COLLECTION_NAME,
            query=query_vector,
            limit=limit,
        )
        return getattr(result, "points", result)

    # Older clients
    return qdrant.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=limit,
    )


def get_chat_response(user_input: str, messages: list[dict[str, str]] | None = None) -> str:
    query_vector = embedder.encode(user_input).tolist()
    search_info = _search_qdrant(query_vector, limit=5)

    context_chunks: list[str] = []
    for info in search_info:
        payload: dict[str, Any] = getattr(info, "payload", None) or {}
        context_chunks.append(str(payload.get("text", "")))

    context = "\n\n".join([c for c in context_chunks if c.strip()])

    if llm is None:
        return (
            "GROQ_API_KEY is not configured, so I can't generate an LLM answer right now.\n"
            "If you want, set GROQ_API_KEY in your .env and restart the app."
        )

    rag_prompt = f"""You are a helpful internal banking assistant.
Use the context below if it is relevant to the question.
If the context does not contain the answer, say so and explain what information is missing.

Context:
{context}

Question:
{user_input}
"""

    if messages is None:
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    messages.append({"role": "user", "content": rag_prompt})
    response = llm.chat.completions.create(
        model=GROQ_MODEL,
        messages=messages,
        temperature=0.2,
    )
    reply = response.choices[0].message.content or ""
    messages.append({"role": "assistant", "content": reply})
    return reply


def start_chat_bot():
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    while True:
        user_input = input("type your message here : ")
        if user_input.strip().lower() in ["exit", "quit"]:
            break
        reply = get_chat_response(user_input=user_input, messages=messages)
        print("\nAI : ", reply, "\n")

