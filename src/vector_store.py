"""Qdrant vector store helpers (admin pipeline compatible).

This module keeps Qdrant imports lazy so the Flask web UI can still boot
(e.g., for login page) even if the venv is missing qdrant-client.

The API also provides "old branch" style helpers:
- create_qdrant_collection
- check_database
- embed_database
"""

from __future__ import annotations

import hashlib
from typing import Any, Iterable, List, Tuple

from .config import COLLECTION_NAME, QDRANT_API_KEY, QDRANT_URL, VECTOR_SIZE


def _qdrant() -> Tuple[Any, Any]:
    try:
        from qdrant_client import QdrantClient  # type: ignore
        from qdrant_client.http import models  # type: ignore
    except ModuleNotFoundError as ex:
        raise RuntimeError(
            "Missing dependency: qdrant-client. Install: pip install -r requirements.txt"
        ) from ex

    return QdrantClient, models


def get_client():
    QdrantClient, _models = _qdrant()
    if QDRANT_API_KEY:
        return QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
    return QdrantClient(url=QDRANT_URL)


def create_qdrant_collection(vector_size: int = VECTOR_SIZE) -> None:
    """Create the Qdrant collection if it does not exist."""

    _QdrantClient, models = _qdrant()
    client = get_client()

    if client.collection_exists(COLLECTION_NAME):
        return

    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=models.VectorParams(size=vector_size, distance=models.Distance.COSINE),
    )


# Backward compatible alias (used by newer code)
create_collection = create_qdrant_collection


def check_database() -> bool:
    """Return True if the configured collection exists."""

    client = get_client()
    return bool(client.collection_exists(COLLECTION_NAME))


def count_points() -> int:
    """Return exact points count in the collection."""

    client = get_client()
    res = client.count(collection_name=COLLECTION_NAME, exact=True)
    return int(res.count)


def make_point_id(source: str | None, chunk_index: int) -> str:
    """Stable ID for a (source, chunk_index) pair.

    This prevents duplication on re-ingest by overwriting existing points.
    """

    stable_key = f"{source}|{int(chunk_index)}".encode("utf-8", errors="ignore")
    return hashlib.blake2b(stable_key, digest_size=16).hexdigest()


def insert_embeddings(chunks: Iterable[Any], embeddings: List[List[float]]) -> int:
    _QdrantClient, models = _qdrant()
    client = get_client()

    points: list[Any] = []

    # Use stable IDs so re-ingestion overwrites instead of duplicating points.
    for idx, (chunk, vector) in enumerate(zip(chunks, embeddings)):
        text = getattr(chunk, "page_content", "")
        meta = getattr(chunk, "metadata", {}) or {}
        source = meta.get("source")
        chunk_index = meta.get("chunk_index", idx)

        payload = {
            "text": text,
            "source": source,
            **{k: v for k, v in meta.items() if k not in {"text"}},
        }

        pid = make_point_id(source, int(chunk_index))

        points.append(
            models.PointStruct(
                id=pid,
                vector=vector,
                payload=payload,
            )
        )

    if points:
        client.upsert(collection_name=COLLECTION_NAME, points=points)

    return len(points)


def embed_database() -> int:
    """Admin ingestion pipeline: load -> split -> embed -> upsert."""

    # Lazy imports (ingestion-only dependencies)
    from .embeddings import embed_documents
    from .loader import load_documents
    from .splitter import split_text

    docs = load_documents()
    chunks = split_text(docs)
    texts = [c.page_content for c in chunks]

    embeddings = embed_documents(texts)
    create_qdrant_collection(len(embeddings[0]) if embeddings else VECTOR_SIZE)

    return insert_embeddings(chunks, embeddings)


def search(query_vector: List[float], *, limit: int = 5) -> list[Any]:
    """Vector search in Qdrant."""

    client = get_client()
    return client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=limit,
        with_payload=True,
    )
