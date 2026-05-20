# Wifak Assistant — Internal Bank Chatbot

An on-premise RAG (Retrieval-Augmented Generation) chatbot for Wifak Bank employees. Ask questions in plain language and get accurate answers drawn directly from the bank's internal policy and procedure documents — no external data leaves the organisation.

> Capstone Project — Software Engineering Degree, MUST University (Feb – Jun 2026)

---

## Preview

> Screenshots below show the live application. Replace the placeholder paths with real captures once the app is running.

| Chat Interface | Admin Panel |
|:-:|:-:|
| ![Chat UI](docs/screenshots/chat.png) | ![Admin Panel](docs/screenshots/admin.png) |

| Document Library | Ingestion Preview |
|:-:|:-:|
| ![Library](docs/screenshots/library.png) | ![Ingestion](docs/screenshots/ingestion.png) |

> **To add your own screenshots:** run the app, capture the pages, and save them under `docs/screenshots/`.

---

## Features

- **Natural language Q&A** over internal bank documents
- **Document ingestion** — upload PDF, DOCX, TXT, or images (OCR) via the admin panel; they are automatically converted to Markdown and indexed
- **Semantic search** using locally generated embeddings (no external embedding API)
- **Source-grounded answers** — the LLM is only given retrieved context, reducing hallucination
- **Admin panel** — system status, one-click re-indexing, document library, ingestion preview with chunk-level inspection
- **Session-based admin auth** — username/password protected admin routes
- **On-premise deployment** — all embedding runs locally; only the final LLM call goes to Groq's API
- **One-command Docker deployment**

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                        Browser                          │
│         Chat UI  (/）           Admin Panel (/admin)    │
└────────────────┬────────────────────────┬───────────────┘
                 │  HTTP                  │  HTTP
┌────────────────▼────────────────────────▼───────────────┐
│              Flask Web App  (src/web_app.py)             │
│                                                         │
│  POST /chat          →  ai_chat.get_chat_response()     │
│  POST /admin/upload  →  document_ingestion + embed      │
│  POST /admin/ingest  →  vector_store.embed_database()   │
└──────────┬──────────────────────────────┬───────────────┘
           │                              │
┌──────────▼──────────┐      ┌────────────▼──────────────┐
│  Sentence-BERT      │      │  Qdrant Vector DB          │
│  all-MiniLM-L6-v2   │      │  Collection: rag_collection│
│  (runs locally)     │      │  Vector size: 384          │
└──────────┬──────────┘      └────────────┬──────────────┘
           │  embed query                 │  top-5 results
           └──────────────────────────────┘
                          │
               ┌──────────▼──────────┐
               │  Groq API           │
               │  llama-3.3-70b-     │
               │  versatile          │
               └─────────────────────┘
```

### Document Ingestion Flow

```
Upload (PDF / DOCX / TXT / PNG / JPG)
         │
         ▼
  document_ingestion.py          ← converts to Markdown
         │
         ▼
     data/ingested/*.md
         │
         ▼
     loader.py                   ← reads all *.md under data/
         │
         ▼
     splitter.py                 ← 500-char chunks, 50-char overlap
         │
         ▼
  sentence-transformers           ← 384-dimensional vectors
         │
         ▼
     Qdrant upsert               ← stores text + source metadata
```

---

## Folder Structure

```
bank-chat-bot-/
├── data/                        # Document storage (git-ignored)
│   └── ingested/                # Markdown output from uploads
├── docs/
│   ├── screenshots/             # Add your screenshots here
│   ├── ARCHITECTURE.md
│   ├── API.md
│   └── guides/
├── src/
│   ├── web/
│   │   ├── templates/           # Jinja2 HTML templates
│   │   │   ├── index.html       # Chat UI
│   │   │   ├── admin.html       # Admin dashboard
│   │   │   ├── library.html     # Document library
│   │   │   └── ingestion_*.html # Chunk inspector
│   │   └── static/
│   │       ├── css/style.css
│   │       ├── js/chat.js
│   │       └── img/
│   ├── web_app.py               # Flask app — main entry point
│   ├── ai_chat.py               # RAG query + Groq LLM call
│   ├── vector_store.py          # Qdrant create / upsert / count
│   ├── document_ingestion.py    # File-to-Markdown conversion
│   ├── loader.py                # Load *.md files into LangChain docs
│   ├── splitter.py              # Chunk documents
│   └── config.py                # Central config (reads .env)
├── .env.example                 # Environment variable template
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

---

## RAG Pipeline

**Retrieval-Augmented Generation** grounds every answer in documents retrieved from the vector store, rather than relying on the model's training data alone.

1. **Ingest** — internal documents are uploaded, converted to Markdown, chunked into 500-character segments, and embedded with Sentence-BERT.
2. **Store** — each chunk's embedding and its raw text are stored as a Qdrant point.
3. **Query** — the user's question is embedded with the same model, and the 5 most similar chunks are retrieved by cosine similarity.
4. **Generate** — the retrieved chunks are injected as context into a prompt sent to the LLM. The model is instructed to answer only from the provided context.
5. **Respond** — the answer is returned to the user in the chat interface.

---

## Embedding Model

| Property | Value |
|----------|-------|
| Model | `sentence-transformers/all-MiniLM-L6-v2` |
| Runs | Locally inside the Docker container (no API call) |
| Vector size | **384** — this must match `VECTOR_SIZE` in `config.py` |
| Distance metric | Cosine similarity |

> **Important:** if you change the embedding model you must drop the existing Qdrant collection and re-index all documents, because the vector dimensions will differ.

---

## Installation

### Prerequisites

| Requirement | Notes |
|-------------|-------|
| Docker & Docker Compose | Version 20+ recommended |
| Groq API key | Free at [console.groq.com](https://console.groq.com) |
| 4 GB RAM minimum | The embedding model loads fully into memory |
| Internet access (first run) | Docker pulls the Qdrant image and downloads the embedding model on first start |

> **No Python installation is needed** when using Docker. For local (non-Docker) setup see below.

---

### Option A — Docker (recommended)

```bash
# 1. Clone the repository
git clone https://github.com/abderrahmen-bchini/bank-chat-bot-.git
cd bank-chat-bot-

# 2. Create your environment file
cp .env.example .env
```

Open `.env` and set at minimum:

```env
GROQ_API_KEY=gsk_...          # your Groq key
FLASK_SECRET_KEY=change-me    # any random string
ADMIN_USERNAME=admin          # admin panel login
ADMIN_PASSWORD=admin123       # admin panel password
```

```bash
# 3. Build and start all services
docker compose up --build
```

Services started:
| Service | URL |
|---------|-----|
| Chat interface | http://localhost:5000 |
| Admin panel | http://localhost:5000/admin |
| Qdrant dashboard | http://localhost:6333/dashboard |

On first start the app automatically creates the Qdrant collection and indexes any Markdown files found in `data/`. Subsequent starts only re-index if the point count has changed.

---

### Option B — Local (without Docker)

**Additional prerequisites:** Python 3.10+, a running Qdrant instance, and `qdrant` resolvable as a hostname (add `127.0.0.1 qdrant` to `/etc/hosts` or change the host values in `vector_store.py` and `ai_chat.py` to `localhost`).

```bash
# 1. Start Qdrant separately
docker run -p 6333:6333 qdrant/qdrant

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set environment variables (or populate .env)
export GROQ_API_KEY=gsk_...
export FLASK_SECRET_KEY=change-me

# 4. Run the app
python src/web_app.py
```

---

## Usage

### Chatting

1. Open http://localhost:5000.
2. Type a question in the input bar, or click one of the quick-topic buttons (Onboarding, Leave Policy, IT Support, etc.).
3. The assistant retrieves relevant chunks from the indexed documents and returns a grounded answer.

### Uploading documents (Admin)

1. Go to http://localhost:5000/admin and log in.
2. Under **Documents**, choose one or more files (PDF, DOCX, TXT, PNG, JPG).
3. Tick **Index immediately** to convert and embed in one step, or upload first and click **Re-index** later.
4. Use **Document Library** to browse and preview converted Markdown files.
5. Use **Ingestion Preview** to inspect how each document is split into chunks before embedding.

### Re-indexing

Click **Re-index** on the admin dashboard to re-embed all documents currently in `data/`. This is necessary after manually adding or editing files in the `data/` folder outside the upload form.

---

## Screenshots

> Replace the images below with actual captures from your running instance. Save screenshots to `docs/screenshots/`.

**Chat interface** — employees ask questions and receive answers grounded in bank documents.

```
docs/screenshots/chat.png
```

**Admin dashboard** — shows Qdrant status, point counts, and upload controls.

```
docs/screenshots/admin.png
```

**Document library** — browse all indexed Markdown files, view or download them.

```
docs/screenshots/library.png
```

**Ingestion preview** — inspect chunk boundaries and point IDs before committing to the index.

```
docs/screenshots/ingestion.png
```

---

## License

This project is the intellectual property of **Abderrahmen Bchini** and **Yassine Ncib**.
For educational use only. Commercial use requires written permission from the repository owner.
