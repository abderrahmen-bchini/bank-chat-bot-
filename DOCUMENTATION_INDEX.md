# Documentation Index

Complete guide to all project documentation and how to navigate it.

## Quick Links

### Getting Started (First Time?)
1. **[README.md](README.md)** ← You are here
2. **[QUICKSTART.md](QUICKSTART.md)** — Get the project running in 5 minutes
3. **[CONTRIBUTING.md](CONTRIBUTING.md)** — How to contribute code

### Understanding the Project
- **[ARCHITECTURE.md](docs/ARCHITECTURE.md)** — System design and components
- **[API.md](docs/API.md)** — REST API endpoints and examples
- **[BACKLOG.md](docs/project/BACKLOG.md)** — All 21 user stories and sprints

### Development Workflow
- **[GIT_WORKFLOW.md](docs/guides/GIT_WORKFLOW.md)** — Branch strategy and conventions
- **[GITHUB_DESKTOP.md](docs/guides/GITHUB_DESKTOP.md)** — Step-by-step GitHub Desktop guide
- **[GITHUB_SETUP.md](docs/guides/GITHUB_SETUP.md)** — Configure GitHub repository

### Project Management
- **[RETROSPECTIVE.md](docs/project/RETROSPECTIVES.md)** — Sprint retrospectives
- **[BACKLOG.md](docs/project/BACKLOG.md)** — Product backlog and acceptance criteria

---

## Directory Structure

### Root Level
- `README.md` — Project overview (main entry point)
- `CONTRIBUTING.md` — Development guidelines
- `QUICKSTART.md` — Quick setup guide
- `docker-compose.yml` — Full stack deployment
- `.env.example` — Configuration template

### `/docs` — Documentation Hub
All project documentation organized by topic.

**Subdirectories:**
- `/guides/` — Setup and workflow guides
- `/project/` — Backlog and retrospectives
- `/templates/` — GitHub issue/PR templates

### `/backend` — Backend Application
Python FastAPI application with all business logic.

### `/frontend` — Frontend Application
React web interface for users.

### `/tests` — Test Suite
Unit and integration tests for the application.

### `/data` — Sample Data
Test documents and sample data for development.

---

## For Different Roles

### Project Manager / Supervisor
- Start with: **[README.md](README.md)**
- Then read: **[BACKLOG.md](docs/project/BACKLOG.md)** and **[RETROSPECTIVE.md](docs/project/RETROSPECTIVES.md)**

### New Developer
1. Read: **[CONTRIBUTING.md](CONTRIBUTING.md)**
2. Follow: **[QUICKSTART.md](QUICKSTART.md)**
3. Learn: **[GIT_WORKFLOW.md](docs/guides/GIT_WORKFLOW.md)** and **[GITHUB_DESKTOP.md](docs/guides/GITHUB_DESKTOP.md)**
4. Understand: **[ARCHITECTURE.md](docs/ARCHITECTURE.md)**

### Backend Developer
1. **[QUICKSTART.md](QUICKSTART.md)** — Local setup
2. **[ARCHITECTURE.md](docs/ARCHITECTURE.md)** — System design
3. **[API.md](docs/API.md)** — API endpoints
4. **[CONTRIBUTING.md](CONTRIBUTING.md)** — Code standards

### Frontend Developer
1. **[QUICKSTART.md](QUICKSTART.md)** — Local setup
2. **[ARCHITECTURE.md](docs/ARCHITECTURE.md)** — System components
3. **[API.md](docs/API.md)** — Available endpoints
4. **[CONTRIBUTING.md](CONTRIBUTING.md)** — Code standards

### DevOps / Infrastructure
- **[QUICKSTART.md](QUICKSTART.md)** — Docker setup
- **[ARCHITECTURE.md](docs/ARCHITECTURE.md)** — Services and dependencies
- `docker-compose.yml` — Full stack configuration

---

## Common Tasks

**I want to...**

### Setup the project locally
→ Follow **[QUICKSTART.md](QUICKSTART.md)**

### Start development on a new feature
→ Follow **[GITHUB_DESKTOP.md](docs/guides/GITHUB_DESKTOP.md)** and **[GIT_WORKFLOW.md](docs/guides/GIT_WORKFLOW.md)**

### Understand the system
→ Read **[ARCHITECTURE.md](docs/ARCHITECTURE.md)**

### See what API endpoints are available
→ Check **[API.md](docs/API.md)**

### Know what to build next
→ Review **[BACKLOG.md](docs/project/BACKLOG.md)**

### Configure GitHub repository
→ Follow **[GITHUB_SETUP.md](docs/guides/GITHUB_SETUP.md)**

---

## File Organization

```
📁 bank-chat-bot-/
├── README.md ← YOU ARE HERE
├── CONTRIBUTING.md
├── QUICKSTART.md
├── REPOSITORY_STRUCTURE.md
├── docker-compose.yml
├── .env.example
├── .gitignore
│
├── 📁 docs/
│   ├── README.md (Documentation Index)
│   ├── ARCHITECTURE.md
│   ├── API.md
│   ├── 📁 guides/
│   │   ├── README.md
│   │   ├── QUICKSTART.md
│   │   ├── GIT_WORKFLOW.md
│   │   ├── GITHUB_SETUP.md
│   │   └── GITHUB_DESKTOP.md
│   ├── 📁 project/
│   │   ├── README.md
│   │   ├── BACKLOG.md
│   │   └── RETROSPECTIVES.md
│   └── 📁 templates/
│       ├── README.md
│       ├── pull_request.md
│       ├── bug_report.md
│       └── feature_request.md
│
├── 📁 backend/
│   ├── README.md
│   ├── api/
│   ├── ingestion/
│   ├── retrieval/
│   ├── llm/
│   ├── auth/
│   ├── requirements.txt
│   └── Dockerfile
│
├── 📁 frontend/
│   ├── README.md
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── Dockerfile
│
├── 📁 tests/
│   └── README.md
│
└── 📁 data/
    └── README.md
```

---

## Next Steps

1. **[QUICKSTART.md](QUICKSTART.md)** — Get project running locally
2. **[CONTRIBUTING.md](CONTRIBUTING.md)** — Read before first commit
3. **[GIT_WORKFLOW.md](docs/guides/GIT_WORKFLOW.md)** — Understand our Git strategy
4. **[GITHUB_DESKTOP.md](docs/guides/GITHUB_DESKTOP.md)** — Daily development workflow

---

**Questions?** Check the relevant documentation file above or ask your team lead.
