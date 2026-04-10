from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct

client = QdrantClient(url="http://localhost:6333")

COLLECTION_NAME = "rag_collection"


def create_collection(vector_size: int):
    client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=vector_size,
            distance=Distance.COSINE
        )
    )
def insert_embeddings(chunks, embeddings):
    points = []

    for i, (chunk, vector) in enumerate(zip(chunks, embeddings)):
        points.append(
            PointStruct(
                id=i,
                vector=vector,
                payload={
                    "text": chunk.page_content,
                    "source": chunk.metadata.get("source", "unknown")
                }
            )
        )

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )
