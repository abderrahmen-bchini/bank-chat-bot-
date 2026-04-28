"""Embeddings utilities.

This repo originally used SentenceTransformers (as in the `abderrahmen` branch).
To keep the web UI runnable even on minimal installs, we support two modes:

1) If `sentence-transformers` is installed -> use SBERT embeddings (best quality)
2) Otherwise -> fallback to a deterministic hashing-based embedding

No external AI APIs are required.
"""

from __future__ import annotations

import hashlib
import math
import re
from typing import Iterable, List, Optional

from .config import EMBEDDING_MODEL, VECTOR_SIZE


_TOKEN_RE = re.compile(r"\w+", re.UNICODE)
_ST_MODEL: Optional[object] = None


def embedding_backend() -> str:
    """Return which embedding backend will be used (without loading large models)."""

    try:
        import sentence_transformers  # type: ignore  # noqa: F401

        return "sentence-transformers"
    except ModuleNotFoundError:
        return "hash"


def _tokenize(text: str) -> List[str]:
    return _TOKEN_RE.findall((text or "").lower())


def _hash_to_int(token: str) -> int:
    # Stable across runs (unlike Python's built-in hash())
    digest = hashlib.blake2b(token.encode("utf-8"), digest_size=8).digest()
    return int.from_bytes(digest, "little", signed=False)


def _hash_embed(text: str, *, vector_size: int = VECTOR_SIZE) -> List[float]:
    vec = [0.0] * vector_size
    tokens = _tokenize(text)
    if not tokens:
        return vec

    for tok in tokens:
        h = _hash_to_int(tok)
        idx = h % vector_size
        sign = 1.0 if ((h >> 1) & 1) else -1.0
        vec[idx] += sign * (1.0 + min(len(tok), 12) / 12.0)

    norm = math.sqrt(sum(v * v for v in vec))
    if norm > 0:
        vec = [v / norm for v in vec]

    return vec


def _get_sentence_transformer():
    """Lazy-load SentenceTransformer if available."""

    global _ST_MODEL
    if _ST_MODEL is not None:
        return _ST_MODEL

    try:
        from sentence_transformers import SentenceTransformer  # type: ignore
    except ModuleNotFoundError:
        return None

    name = (EMBEDDING_MODEL or "").strip()
    if name and "/" not in name:
        name = f"sentence-transformers/{name}"
    if not name:
        name = "sentence-transformers/all-MiniLM-L6-v2"

    _ST_MODEL = SentenceTransformer(name)
    return _ST_MODEL


def embed_documents(texts: Iterable[str]) -> List[List[float]]:
    """Embed many texts into vectors."""

    texts_list = list(texts)
    model = _get_sentence_transformer()

    if model is None:
        return [_hash_embed(t) for t in texts_list]

    # SentenceTransformers returns a numpy array; .tolist() makes it JSON/Qdrant friendly.
    return model.encode(texts_list).tolist()


def embed_query(query: str) -> List[float]:
    """Embed a user query into a vector."""

    model = _get_sentence_transformer()
    if model is None:
        return _hash_embed(query)

    return model.encode([query])[0].tolist()
