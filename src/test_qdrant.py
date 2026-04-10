from src.loader import load_documents
from src.splitter import split_text
from src.embeddings import embed_documents
from src.vector_store import create_collection, insert_embeddings

# 1. Load + split
docs = load_documents()
chunks = split_text(docs)

print("Chunks:", len(chunks))

# 2. Embeddings
embeddings = embed_documents(chunks)

print("Embedding size:", len(embeddings[0]))

# 3. Create DB collection
create_collection(len(embeddings[0]))

# 4. Save to Qdrant
insert_embeddings(chunks, embeddings)

print("✅ Data inserted into Qdrant")
