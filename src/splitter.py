from __future__ import annotations

from typing import List

from .loader import Document


def split_text(
    documents: List[Document],
    *,
    chunk_size: int = 500,
    chunk_overlap: int = 50,
) -> List[Document]:
    """Split documents into overlapping character chunks.

    This replaces the old LangChain splitter to keep installs lightweight.

    Metadata added per chunk:
      - chunk_index
      - chunk_start
      - chunk_end
      - chunk_size
      - chunk_overlap
    """

    if chunk_size <= 0:
        raise ValueError("chunk_size must be > 0")
    if chunk_overlap < 0:
        raise ValueError("chunk_overlap must be >= 0")

    step = max(1, chunk_size - chunk_overlap)
    chunks: List[Document] = []

    for doc in documents:
        text = doc.page_content or ""
        if not text.strip():
            continue

        idx = 0
        for start in range(0, len(text), step):
            end = min(len(text), start + chunk_size)
            piece = text[start:end].strip()
            if not piece:
                continue

            meta = dict(doc.metadata or {})
            meta["chunk_index"] = idx
            meta["chunk_start"] = int(start)
            meta["chunk_end"] = int(end)
            meta["chunk_size"] = int(chunk_size)
            meta["chunk_overlap"] = int(chunk_overlap)

            chunks.append(Document(page_content=piece, metadata=meta))
            idx += 1

            if end >= len(text):
                break

    return chunks
