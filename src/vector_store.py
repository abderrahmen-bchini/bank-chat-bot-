from config import *
from loader import load_documents
from splitter import split_text
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import PointStruct
from sentence_transformers import SentenceTransformer


def _qdrant_client():
    kwargs = {"url": QDRANT_URL, "timeout": QDRANT_TIMEOUT_SECONDS}
    if QDRANT_API_KEY:
        kwargs["api_key"] = QDRANT_API_KEY
    return QdrantClient(**kwargs)

def embed_database():
    client = _qdrant_client()
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
    return len(points)


def create_qdrant_collection():
    client = _qdrant_client()
    vector_params = models.VectorParams(size=VECTOR_SIZE,distance=models.Distance.COSINE)
    client.create_collection(collection_name=COLLECTION_NAME , vectors_config=vector_params)
    if client.collection_exists(COLLECTION_NAME) :
        print ("collection has been created ")
def check_database(): 
    client = _qdrant_client()
    if client.collection_exists(COLLECTION_NAME) : 
        return True 
    else : 
        return False 


def count_points():
    client = _qdrant_client()
    result = client.count(collection_name=COLLECTION_NAME, exact=True)
    return int(result.count)
