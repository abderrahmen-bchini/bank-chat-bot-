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
| Language Model | Ollama with Mistral/Llama 2 / Groq / openai  |
| Metadata Database | Qdrant |
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

# Services available at ( not available yet ):
# API: http://localhost:8000
# Frontend: http://localhost:3000
# Qdrant: http://localhost:6333/dashboard
```

---

## Project Structure

```
``.
├── data
├── docs
│   ├── API.md
│   ├── ARCHITECTURE.md
│   ├── guides
│   ├── project
│   ├── README.md
│   └── templates
├── main.py
├── README.md
├── requirements.txt
├── src
│   ├── config.py
│   ├── embeddings.py
│   ├── loader.py
│   ├── __pycache__
│   ├── splitter.py
│   ├── test_embeddings.py
│   ├── test.py
│   ├── test_qdrant.py
│   └── vector_store.py
└── venv
    ├── bin
    ├── include
    ├── lib
    ├── lib64 -> lib
    ├── pyvenv.cfg
    └── share`

---

## Architecture

### System Components

- **API Layer**: FastAPI for request handling and routing
- **Ingestion**: Document parsing, text cleaning, chunking, embedding generation
- **Retrieval**: Vector similarity search with Qdrant
- **Generation**: LLM context injection and answer generation
- **Auth**: JWT-based authentication with role-based access

### Data Flow

```
User Query → Validate → Embed → Search Qdrant → Filter by Role 
→ Build Prompt → Call LLM → Validate → Return with Citations → Log
```


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
abderrahmen              ← Abderrahmen Bchini branch  
yassine              ← Yassine Ncib Branch  

```

### Using GitHub Desktop (Yassine Ncib)

use **GitHub Desktop** for branch management:

1. **Create branch**: Current Branch → New Branch → Name → Create
2. **Make changes**: Edit files → Commit → Push origin
3. **Create PR**: After push → Create Pull Request
4. **Review & Merge**: Team reviews → Squash and merge
 
### Using remote access fron the terminal (Abderrahmen Bchini)

using the **terminal** for branch management:

1. **Create branch**: git checkout -b branch-name 
2. **Make changes**:
    git add . 
    git commint -m "your message"
    git push -u origin branch-name 
3. **Create Pull Request **: After push → Create a pull request on GitHub 
4. **Review & Merge**: Team reviews → Squash and merge

### Commit Convention

```
docs: description
```

### Pull Request Process (in work)

1. Create feature branch from `develop`
2. Implement changes with tests
3. Push to origin
4. Create PR on GitHub
5. Link issue: `Closes #XX`
6. Request review
7. After approval: squash and merge

---


## Documentation


- [Quick Start](docs/guides/QUICKSTART.md) — Setup and run locally
- [Architecture](docs/ARCHITECTURE.md) — System design
- [API Reference](docs/API.md) — REST API endpoints
- [Product Backlog](docs/project/BACKLOG.md) — User stories and sprints
- [GitHub Desktop Guide](docs/guides/GITHUB_DESKTOP.md) — Branching and PR workflow
- [GitHub Setup](docs/guides/GITHUB_SETUP.md) — Repository configuration

Additional:
- [CONTRIBUTING.md](CONTRIBUTING.md) — Development guidelines

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
| Project Lead | Abderrahmen | abderrahmen.bchini@musteducation.tn |
| Backend | Abderrahmen | abderrahmen.bchini@musteducation.tn |
| Frontend | Yassine | mohamedyassine.ncib@musteducation.tn |
| DevOps | Abderrahmen , Yassine |  abderrahmen.bchini@musteducation.tn , mohamedyassine.ncib@musteducation.tn|
| Supervisor | Naoufel Kraiem | no email |

**University**: MUST University 
**Department**: Software Engineering  
**Period**: Feb 2026 , June 2026


---

## 📚 Documentation

- **[Architecture](docs/ARCHITECTURE.md)** — System design & components
- **[API Reference](docs/API.md)** — Backend endpoints
- **[Deployment Guide](docs/DEPLOYMENT.md)** — Production setup
- **[Development Setup](CONTRIBUTING.md)** — How to set up dev environment

---

## ⚖️ License

This project is the intellectual property of Abderrahmen Bchini & Yassine Ncib For educational use only and it cannot be used for commerical use without the permission of the repo owner .

---
**Last Updated**: April 2026 
**Project Status**: Sprint 2 - Document Ingestion Pipeline
