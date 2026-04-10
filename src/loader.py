from langchain_core.documents import Document
from pathlib import Path

DATA_PATH = "/home/zlk/rag_project/data/"

def load_documents():
    documents = []

    for file in Path(DATA_PATH).glob("*.md"):
        with open(file, "r", encoding="utf-8") as f:
            text = f.read()

        documents.append(
            Document(
                page_content=text,
                metadata={"source": file.name}
            )
        )

    return documents
