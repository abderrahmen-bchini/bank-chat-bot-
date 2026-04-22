from dotenv import load_dotenv 
import os
from groq import Groq 
from qdrant_client import QdrantClient 
from sentence_transformers import SentenceTransformer 
from config import EMBEDDING_MODEL , COLLECTION_NAME

load_dotenv("/home/zlk/github/bank-chat-bot-/.env")
llm = Groq(api_key=os.getenv("GROQ_API_KEY"))
qdrant = QdrantClient(host="localhost" , port=6333)
embedder = SentenceTransformer(f"sentence-transformers/all-MiniLM-L6-v2")
messages = [{"role": "system" , "content" : "you are a helpful assistant" "Answer using the provided context when relevant" "if the context does not contain the answer , say so " }]

while True :
    user_input = input("type your message here : ")
    if user_input.lower() in ["exit" , "quit"] : 
        break 
    query_vector = embedder.encode(user_input).tolist()
    search_info = qdrant.query_points(collection_name=COLLECTION_NAME , query=query_vector , limit=5).points
    context_chunks = []
    for info in search_info:
        text = info.payload.get("text" , "")
        context_chunks.append(text)
    context = "\n\n".join(context_chunks)
    rag_prompt = f"""
    Context:
    {context}
    Question:
    {user_input}

    Answer the question using only the context above when possible.
    """
    messages.append({"role": "user" , "content" : rag_prompt})
    response = llm.chat.completions.create(model="llama-3.3-70b-versatile", messages=messages, temperature=0.2)
    reply = response.choices[0].message.content
    print("\nAI : " , reply , "\n")
    messages.append({"role" : "assistant" , "content" : reply})




