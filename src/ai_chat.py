from typing import Any
from dotenv import load_dotenv
import os
from groq import Groq
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from config import EMBEDDING_MODEL, COLLECTION_NAME, QDRANT_TIMEOUT_SECONDS

load_dotenv()
llm = Groq(api_key=os.getenv("GROQ_API_KEY"))
qdrant = QdrantClient(host="qdrant", port=6333, timeout=QDRANT_TIMEOUT_SECONDS)
embedder = SentenceTransformer(f"sentence-transformers/{EMBEDDING_MODEL}")

SYSTEM_PROMPT = (
    "you are a helpful assistant."
    "Answer using the provided context when relevant."
    "if the context does not contain the answer , say so."
)

def get_chat_response(user_input: str, messages: list[dict[str, str]] | None = None) -> str:
    query_vector = embedder.encode(user_input).tolist()
    search_info = qdrant.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=5,
    ).points
    context_chunks = []
    for info in search_info:
        payload: dict[str, Any] = info.payload or {}
        context_chunks.append(str(payload.get("text", "")))
    context = "\n\n".join(context_chunks)
    rag_prompt = f"""
    you are a helpful assistant.
    use the context below if it is relevant to the question.
    if the context is not useful or does not contain the answer, answer using your general knowledge.
    Context:
    {context}
    Question:
    {user_input}

    Answer the question using only the context above when possible.
    """
    if messages is None:
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.append({"role": "user", "content": rag_prompt})
    response = llm.chat.completions.create(
        model="llama-3.3-70b-versatile",
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

