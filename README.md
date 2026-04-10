# Bank Chatbot - Internal Knowledge Assistant

Intelligent chatbot system for Wifak Bank to assist employees with internal procedures, policies, and processes through natural language question answering.

Capstone Project | Software Engineering Degree

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Architecture](#architecture)
- [Sprints](#sprints)
- [Contributing](#contributing)
- [Team](#team)

---

## Overview

### Problem
Bank employees struggle to find information across multiple documentation sources, resulting in inefficiency and time waste. No centralized system exists to answer questions about bank procedures and policies.

### Solution
A Retrieval-Augmented Generation (RAG) chatbot that:
- Ingests PDF/DOCX/TXT documents
- Generates embeddings locally for semantic search
- Provides accurate answers with source citations
- Enforces role-based access control
- Maintains audit logs for compliance

### Key Features

- Document ingestion pipeline
- Semantic search and retrieval
- Natural language question answering
- Source attribution
- Role-based access control
- On-premise deployment
- Query audit logging

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Backend | FastAPI (Python 3.10+) |
| Frontend | React 18 |
| Vector Database | Qdrant |
| Embeddings | Sentence-BERT (local) |
| Language Model | Ollama with Mistral/Llama 2 |
| Metadata Database | PostgreSQL |
| Authentication | JWT + RBAC |
| Deployment | Docker Compose |

---

## Quick Start

### Using Docker Compose (Recommended)

```bash
git clone https://github.com/abderrahmen-bchini/bank-chat-bot-.git
cd bank-chat-bot-

cp .env.example .env
docker-compose up -d

# Services available at:
# API: http://localhost:8000
# Frontend: http://localhost:3000
# Qdrant: http://localhost:6333/dashboard
```

### Manual Setup

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn api.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm start
```

See [QUICKSTART.md](QUICKSTART.md) for detailed setup instructions.

---

## Project Structure

```
bank-chat-bot-/
├── backend/
│   ├── api/              # FastAPI routes
│   ├── ingestion/        # Document processing
│   ├── retrieval/        # Vector search
│   ├── llm/              # LLM integration
│   ├── auth/             # Authentication
│   └── requirements.txt
├── frontend/             # React application
├── data/                 # Sample documents
├── tests/                # Unit & integration tests
├── docker-compose.yml    # Full stack deployment
├── .env.example          # Configuration template
├── README.md             # This file
├── CONTRIBUTING.md       # Development guidelines
├── ARCHITECTURE.md       # System design
├── BACKLOG.md           # Product backlog
├── API.md               # API reference
├── QUICKSTART.md        # Setup guide
└── RETROSPECTIVE.md     # Sprint retrospectives
```

---

## Architecture

### System Components

- **API Layer**: FastAPI for request handling and routing
- **Ingestion**: Document parsing, text cleaning, chunking, embedding generation
- **Retrieval**: Vector similarity search with Qdrant
- **Generation**: LLM context injection and answer generation
- **Storage**: PostgreSQL for metadata, Qdrant for embeddings
- **Auth**: JWT-based authentication with role-based access

### Data Flow

```
User Query → Validate → Embed → Search Qdrant → Filter by Role 
→ Build Prompt → Call LLM → Validate → Return with Citations → Log
```

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed system design.

---

## Sprints

### Sprint 1: Infrastructure & Setup
Complete
- US-01: GitHub repo with branching strategy
- US-02: Notion documentation pipeline
- US-03: System architecture

### Sprint 2: Document Ingestion Pipeline
In Progress
- US-04: File upload (PDF/DOCX/TXT)
- US-05: Text extraction & cleaning
- US-06: Document chunking
- US-07: Embedding generation
- US-08: Qdrant storage

### Sprint 3: RAG & Q&A System
Planned
- US-09: Natural language Q&A
- US-10: Query embedding & search
- US-11: Context injection
- US-12: Hallucination check
- US-13: Source citations

### Sprint 4: Auth & Security
Planned
- US-14: User authentication
- US-15: Role-based access
- US-16: Audit logging
- US-17: On-premise deployment

### Sprint 5: UI & Deployment
Planned
- US-18: Web interface
- US-19: Admin panel
- US-20: One-command deployment
- US-21: Performance testing

See [BACKLOG.md](BACKLOG.md) for complete product backlog.

---

## Git Workflow

### Why We Use Branches

We protect `main` by requiring all code to go through feature branches and pull requests:
- Prevents untested code reaching production
- Ensures peer review before merging
- Allows parallel work on multiple features
- Maintains code quality and traceability

### Branching Strategy

```
main              ← Production-ready (protected)
develop           ← Integration branch (default)
feature/US-XX-*   ← Feature branches
fix/*             ← Bug fixes
```

### Using GitHub Desktop

We use **GitHub Desktop** for branch management:

1. **Create branch**: Current Branch → New Branch → Name → Create
2. **Make changes**: Edit files → Commit → Push origin
3. **Create PR**: After push → Create Pull Request
4. **Review & Merge**: Team reviews → Squash and merge

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed GitHub Desktop steps.

### Commit Convention

```
feat(scope): description
fix(scope): description
docs: description
```

### Pull Request Process

1. Create feature branch from `develop`
2. Implement changes with tests
3. Push to origin
4. Create PR on GitHub
5. Link issue: `Closes #XX`
6. Request review
7. After approval: squash and merge

---

## Contributing

All contributors must follow the guidelines in [CONTRIBUTING.md](CONTRIBUTING.md).

Quick checklist:
- Read CONTRIBUTING.md
- Follow git workflow
- Write tests for new features
- Follow code standards
- Request peer review before merging

---

## Team

| Role | Name | Email |
|------|------|-------|
| Project Lead | [Name] | [email] |
| Backend | [Name] | [email] |
| Frontend | [Name] | [email] |
| DevOps | [Name] | [email] |
| Supervisor | [Name] | [email] |

**University**: [Institution]  
**Department**: Software Engineering  
**Period**: [Start] — [End]

---

## Documentation

- [QUICKSTART.md](QUICKSTART.md) — Setup and run locally
- [ARCHITECTURE.md](ARCHITECTURE.md) — System design
- [API.md](API.md) — REST API reference
- [BACKLOG.md](BACKLOG.md) — Product backlog
- [CONTRIBUTING.md](CONTRIBUTING.md) — Development guide and workflows
- [GITHUB_DESKTOP.md](GITHUB_DESKTOP.md) — GitHub Desktop step-by-step guide
- [RETROSPECTIVE.md](RETROSPECTIVE.md) — Sprint retrospectives
- [GITHUB_SETUP.md](GITHUB_SETUP.md) — GitHub configuration

---

## License

This project is the intellectual property of [Institution]. For educational use only.

---

## Support

For questions:
1. Check existing GitHub Issues
2. Review documentation
3. Open new issue with relevant label
4. Contact team via supervisor

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Python, FastAPI |
| **Document Processing** | PyPDF2, python-docx, Langchain |
| **Vector Store** | Qdrant (local) |
| **Embeddings** | Local embedding model (Sentence-BERT, MiniLM) |
| **LLM** | Ollama / Local LLM (Mistral, Llama 2) |
| **Frontend** | React/Vue.js (Sprint 5) or HTML/CSS/JS |
| **Deployment** | Docker, Docker Compose |
| **Database** | PostgreSQL (metadata), Qdrant (vectors) |
| **Auth** | JWT + Role-Based Access Control |

---

## 🚀 Quick Start

### Prerequisites
- Git
- Docker & Docker Compose
- Python 3.10+
- 8GB RAM (16GB recommended for LLM)

### Installation & Local Deployment

```bash
# 1. Clone the repository
git clone https://github.com/abderrahmen-bchini/bank-chat-bot-.git
cd bank-chat-bot-

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# 4. Start with Docker Compose (one command)
docker-compose up -d

# 5. Access the system
# Backend API: http://localhost:8000
# Frontend: http://localhost:3000
# Qdrant UI: http://localhost:6333/dashboard
```

### Manual Setup (Development)

```bash
# Backend
cd backend
pip install -r requirements.txt
python -m uvicorn api.main:app --reload

# Frontend (separate terminal)
cd frontend
npm install
npm start

# Qdrant (Docker)
docker run -p 6333:6333 qdrant/qdrant
```

---

## 📁 Repository Structure

```
bank-chat-bot-/
├── backend/
│   ├── api/                    # FastAPI routes
│   │   ├── main.py
│   │   ├── auth.py            # JWT & role management
│   │   └── documents.py        # File upload endpoints
│   ├── ingestion/              # Document processing
│   │   ├── loader.py           # PDF/DOCX/TXT extraction
│   │   ├── cleaner.py          # Text cleaning & normalization
│   │   ├── chunker.py          # Semantic chunking
│   │   └── embedder.py         # Embedding generation
│   ├── retrieval/              # Vector search
│   │   ├── qdrant_client.py    # Qdrant integration
│   │   └── retriever.py        # Semantic search logic
│   ├── llm/                    # LLM integration
│   │   ├── prompt_builder.py   # Context injection
│   │   ├── generator.py        # Answer generation
│   │   └── hallucination_check.py  # Fact validation
│   ├── auth/                   # Authentication & security
│   │   ├── jwt_handler.py
│   │   ├── rbac.py             # Role-based access
│   │   └── audit.py            # Query logging
│   ├── config.py               # Configuration
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatInterface.js
│   │   │   ├── DocumentUpload.js
│   │   │   └── AdminPanel.js
│   │   └── App.js
│   ├── package.json
│   └── .env.example
├── data/
│   ├── sample_documents/       # Test PDFs (no real data)
│   └── embeddings/             # Cache
├── tests/
│   ├── test_ingestion.py
│   ├── test_retrieval.py
│   ├── test_llm.py
│   └── test_auth.py
├── docs/
│   ├── ARCHITECTURE.md         # System design
│   ├── API.md                  # API documentation
│   ├── DEPLOYMENT.md           # Deployment guide
│   └── diagrams/               # Architecture diagrams
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   └── PULL_REQUEST_TEMPLATE.md
├── docker-compose.yml
├── Dockerfile
├── .gitignore
├── README.md
├── CONTRIBUTING.md
└── LICENSE
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     USER INTERFACE                          │
│              (React Web, Mobile Friendly)                   │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│                   FASTAPI BACKEND                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Query Router │  │ Auth/RBAC    │  │ Upload API   │      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
└─────────┼──────────────────┼──────────────────┼─────────────┘
          │                  │                  │
    ┌─────▼────────┬─────────▼──────┬──────────▼──────┐
    │              │                │                 │
┌───▼──────────┐ ┌─▼────────────┐ ┌─▼──────────────┐ │
│   RETRIEVAL  │ │ INGESTION    │ │    STORAGE     │ │
│              │ │              │ │                │ │
│ • Qdrant     │ │ • PDF loader │ │ • PostgreSQL   │ │
│   Search     │ │ • DOCX loader│ │   (metadata)   │ │
│ • Embedding  │ │ • Chunker    │ │ • Qdrant       │ │
│   Model      │ │ • Cleaner    │ │   (vectors)    │ │
└──────────────┘ └──────────────┘ └────────────────┘ │
    │                                                  │
└────┬──────────────────────────────────────────────────┘
     │
┌────▼──────────────────────────────────────────────────┐
│              LLM LAYER (LOCAL)                        │
│  ┌──────────────────────────────────────────────┐   │
│  │  Ollama / Local LLM (Mistral, Llama 2)       │   │
│  │  • Context Injection                         │   │
│  │  • Answer Generation                         │   │
│  │  • Hallucination Check                       │   │
│  └──────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

---

## 📊 Sprints & Progress

### Epic 1: Infrastructure & Setup ✅ **SPRINT 1 — DONE**
- [x] US-01: GitHub repo with branching strategy
- [x] US-02: Notion documentation pipeline
- [x] US-03: System architecture definition

### Epic 2: Document Ingestion Pipeline 🟡 **SPRINT 2 — IN PROGRESS**
- [ ] US-04: PDF/DOCX/TXT file upload
- [ ] US-05: Text extraction & cleaning
- [ ] US-06: Document chunking
- [ ] US-07: Embedding generation
- [ ] US-08: Qdrant storage integration

### Epic 3: RAG & Q&A System ⏳ **SPRINT 3 — PLANNED**
- [ ] US-09: Natural language Q&A
- [ ] US-10: Query embedding & semantic search
- [ ] US-11: Context injection into LLM
- [ ] US-12: Hallucination check
- [ ] US-13: Source citation

### Epic 4: Auth & Security ⏳ **SPRINT 4 — PLANNED**
- [ ] US-14: User login & authentication
- [ ] US-15: Role-based access control
- [ ] US-16: Query/access audit logging
- [ ] US-17: On-premise, zero external APIs

### Epic 5: UI & Deployment ⏳ **SPRINT 5 — PLANNED**
- [ ] US-18: Web interface for Q&A
- [ ] US-19: Admin document management panel
- [ ] US-20: One-command local deployment
- [ ] US-21: Performance testing & docs

---

## 🔄 Git Workflow

### Branching Strategy (Git Flow)
```
main               ← Production-ready only
├── develop        ← Integration branch
│   ├── feature/US-04-pdf-upload
│   ├── feature/US-05-text-extraction
│   ├── fix/bug-embedding-timeout
│   └── ...
```

### Branch Naming
- **Features**: `feature/US-XX-short-description`
- **Fixes**: `fix/short-description`
- **Docs**: `docs/short-description`
- **Hotfixes**: `hotfix/short-description`

### Commit Convention
```
feat(ingestion): add PDF text extraction module
fix(api): resolve timeout on large document uploads
docs(readme): add local setup instructions
test(retrieval): add Qdrant search tests

Prefixes: feat, fix, docs, test, refactor, chore
```

### Pull Request Process
1. Create feature branch from `develop`
2. Make changes & commit
3. Push & create PR with title: `[US-XX] Short Description`
4. Link the related GitHub Issue
5. Get at least 1 team member review
6. Squash & merge to `develop`
7. After sprint, merge `develop` → `main`

---

## 📝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed contribution guidelines.

### Quick Checklist
- [ ] Fork and create a feature branch
- [ ] Write tests for new features
- [ ] Follow commit message convention
- [ ] Submit PR with issue reference
- [ ] Wait for review approval

---

## 👥 Team

| Role | Name | Email |
|------|------|-------|
| **Project Lead** | [Your Name] | [email] |
| **Backend Lead** | [Name] | [email] |
| **Frontend Lead** | [Name] | [email] |
| **DevOps/Infra** | [Name] | [email] |
| **Supervisor** | [Supervisor Name] | [email] |

**University**: [Your University]  
**Department**: Software Engineering  
**Capstone Period**: [Dates]

---

## 📚 Documentation

- **[Architecture](docs/ARCHITECTURE.md)** — System design & components
- **[API Reference](docs/API.md)** — Backend endpoints
- **[Deployment Guide](docs/DEPLOYMENT.md)** — Production setup
- **[Development Setup](CONTRIBUTING.md)** — How to set up dev environment

---

## ⚖️ License

This project is the intellectual property of [Your University/Organization]. For educational use only.

---

## 📞 Support

For questions or issues:
1. Check existing [GitHub Issues](https://github.com/abderrahmen-bchini/bank-chat-bot-/issues)
2. Review [documentation](docs/)
3. Open a new issue with `bug` or `question` label
4. Contact team via supervisor

---

**Last Updated**: April 2025  
**Project Status**: Sprint 2 - Document Ingestion Pipeline
