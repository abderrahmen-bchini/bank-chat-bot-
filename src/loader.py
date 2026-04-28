from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict


@dataclass
class Document:
    page_content: str
    metadata: Dict[str, Any]


# Cross-platform data directory (repo_root/data)
DATA_PATH = Path(__file__).resolve().parents[1] / "data"


def load_documents() -> list[Document]:
    """Load all markdown documents from the data folder."""

    documents: list[Document] = []

    for file in DATA_PATH.rglob("*.md"):
        text = file.read_text(encoding="utf-8", errors="ignore").strip()
        if not text:
            continue

        documents.append(Document(page_content=text, metadata={"source": file.name}))

    return documents
