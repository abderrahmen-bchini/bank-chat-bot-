from src.loader import load_documents
from src.splitter import split_text
from src.embeddings import embed_documents
from src.vector_store import create_collection, insert_embeddings


def main():
    print("📄 Loading documents...")
    docs = load_documents()
    print(f"Docs loaded: {len(docs)}")

    print("\n✂️ Splitting text...")
    chunks = split_text(docs)
    print(f"Chunks created: {len(chunks)}")

    print("\n🧠 Creating embeddings...")
    embeddings = embed_documents(chunks)
    print(f"Embeddings created: {len(embeddings)}")

    print("\n🗄️ Creating Qdrant collection...")
    vector_size = len(embeddings[0])
    create_collection(vector_size)

    print("\n📥 Inserting into Qdrant...")
    insert_embeddings(chunks, embeddings)

    print("\n✅ Done! Data successfully stored in Qdrant.")


if __name__ == "__main__":
    main()
