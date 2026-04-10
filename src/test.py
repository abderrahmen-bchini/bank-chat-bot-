import random
from loader import load_documents
from splitter import split_text

docs = load_documents()
print("Docs loaded:", len(docs))

chunks = split_text(docs)
print("Chunks created:", len(chunks))
c = random.choice(chunks)

print("=== CHUNK ===")
print(c.page_content)

print("\n=== METADATA ===")
print(c.metadata)
