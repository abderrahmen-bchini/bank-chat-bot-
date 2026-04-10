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

### Branching Strategy

```
main              ← Production-ready (protected)
develop           ← Integration branch (default)
feature/US-XX-*   ← Feature branches
fix/*             ← Bug fixes
```

### Commit Convention

```
feat(scope): description
fix(scope): description
docs: description
test(scope): description
refactor: description
chore: description
```

### Pull Request Process

1. Create feature branch from `develop`
2. Implement changes with tests
3. Push and create PR with title: `[US-XX] Description`
4. Link the related issue
5. Request review
6. After approval: squash and merge

See [CONTRIBUTING.md](CONTRIBUTING.md) for complete guidelines.

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
- [CONTRIBUTING.md](CONTRIBUTING.md) — Development guide
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

