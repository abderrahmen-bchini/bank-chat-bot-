from config import COLLECTION_NAME, EMBEDDING_MODEL
from loader import load_documents
from splitter import split_text
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct
from sentence_transformers import SentenceTransformer


client = QdrantClient("localhost", port=6333)
model = SentenceTransformer(f"sentence-transformers/{EMBEDDING_MODEL}")

# load and split
raw_docs = load_documents()
chunks = split_text(raw_docs)

if not chunks:
    raise ValueError("No chunks were created. Check your data path and markdown files.")

# change from document object to string
texts = [chunk.page_content for chunk in chunks]

embeddings = model.encode(texts)

points = [
    PointStruct(
        id=i,
        vector=embedding.tolist(),
        payload={
            "text": chunk.page_content,
            "source": chunk.metadata.get("source")
        }
    )
    for i, (embedding, chunk) in enumerate(zip(embeddings, chunks))
]

client.upsert(
    collection_name=COLLECTION_NAME,
    points=points
)

print(f"Inserted {len(points)} points into Qdrant")



# this code below is used to create a collection in qdrant 
#client.create_collection(collection_name=COLLECTION_NAME , vectors_config=models.VectorParams(size=VECTOR_SIZE , distance=models.Distance.COSINE))
# this code checks if the collection exits 
# print(client.collection_exists(COLLECTION_NAME))

