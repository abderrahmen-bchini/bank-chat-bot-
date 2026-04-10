from openai import OpenAI
from src.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def embed_documents(documents):
    texts = [doc.page_content for doc in documents]

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=texts
    )

    embeddings = [item.embedding for item in response.data]
    return embeddings
