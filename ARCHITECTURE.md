# Architecture Documentation

## System Design Overview

The Bank Chatbot is built on a **Retrieval-Augmented Generation (RAG)** architecture that combines document retrieval with large language models to provide accurate, source-cited answers.

### High-Level Components

1. **Frontend** - React web interface for users
2. **Backend API** - FastAPI for request handling & routing
3. **Document Processing** - Pipeline for ingestion & indexing
4. **Vector Store** - Qdrant for semantic search
5. **LLM** - Ollama with local language models
6. **Databases** - PostgreSQL for metadata, Qdrant for embeddings

### Data Flow

```
User Query
    ↓
[Validate & Authenticate]
    ↓
[Embed Query]
    ↓
[Vector Search in Qdrant]
    ↓
[Filter by User Role]
    ↓
[Build Prompt with Context]
    ↓
[Call Local LLM]
    ↓
[Validate Answer]
    ↓
[Return with Citations]
    ↓
[Log to Audit Trail]
```

### Document Ingestion

```
File Upload
    ↓
[Extract Text] (PDF/DOCX/TXT)
    ↓
[Clean & Normalize]
    ↓
[Split into Chunks]
    ↓
[Generate Embeddings]
    ↓
[Store in Qdrant]
    ↓
[Store Metadata in PostgreSQL]
```

## Key Technologies

| Layer | Tech | Purpose |
|-------|------|---------|
| **Frontend** | React, Axios | User interface & API client |
| **Backend** | FastAPI, Pydantic | API routes, validation, auth |
| **LLM** | Ollama, Mistral/Llama 2 | Answer generation |
| **Embeddings** | Sentence-BERT | Vector representations |
| **Vector DB** | Qdrant | Fast semantic search |
| **Metadata DB** | PostgreSQL | User, document, query logs |
| **Auth** | JWT | Stateless authentication |
| **Deployment** | Docker, Docker Compose | Containerization |

## Security Architecture

- **Authentication**: JWT tokens with configurable expiration
- **Authorization**: Role-Based Access Control (RBAC)
- **Data Privacy**: On-premise deployment, no external APIs
- **Audit Trail**: All queries and admin actions logged
- **Input Validation**: File type & size checks, query validation

## Scalability Considerations

**Current**: Single-machine Docker Compose  
**Future**: Kubernetes, load balancing, distributed caching

---

See [docs/ARCHITECTURE.md](ARCHITECTURE.md) for detailed technical specifications.
