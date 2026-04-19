from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from config import QDRANT_URL, COLLECTION_NAME, VECTOR_SIZE

client = QdrantClient(url=QDRANT_URL)


def create_collection():
    client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=VECTOR_SIZE,
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


def search(query_vector, limit=3):
    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=limit
    )

    return [hit.payload["text"] for hit in results]
