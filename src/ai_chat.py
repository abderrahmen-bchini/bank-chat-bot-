"""CLI chat (admin/testing).

The `abderrahmen` branch had a CLI chatbot that used Groq.
This version stays offline: it retrieves from Qdrant and prints the best
matching snippets + sources.
"""

from __future__ import annotations

from .embeddings import embed_query
from .vector_store import search


def start_chat_bot() -> None:
    print("Wifak Assistant (CLI) — type 'exit' to quit")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in {"exit", "quit"}:
            break
        if not user_input:
            continue

        try:
            qvec = embed_query(user_input)
            results = search(qvec, limit=3)
        except Exception as ex:  # noqa: BLE001
            print(f"Error: {type(ex).__name__}")
            continue

        if not results:
            print("Assistant: No results found. Ask an admin to ingest documents.")
            continue

        print("Assistant: Top internal references:")
        for r in results:
            pl = getattr(r, "payload", None) or {}
            src = pl.get("source") or "Unknown source"
            txt = (pl.get("text") or "").strip().replace("\n", " ")
            print(f"- {src}: {txt[:220]}{'…' if len(txt) > 220 else ''}")
        print("")
