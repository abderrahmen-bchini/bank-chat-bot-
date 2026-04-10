# Product Backlog

## Epics Overview

| Epic | Description | Status | Sprints |
|------|-------------|--------|---------|
| **Epic 1** | Infrastructure & Setup | ✅ Done | Sprint 1 |
| **Epic 2** | Document Ingestion | 🟡 In Progress | Sprint 2 |
| **Epic 3** | RAG & Q&A System | ⏳ Planned | Sprint 3 |
| **Epic 4** | Auth & Security | ⏳ Planned | Sprint 4 |
| **Epic 5** | UI & Deployment | ⏳ Planned | Sprint 5 |

---

## Epic 1: Infrastructure & Setup ✅ **SPRINT 1 — DONE**

| US ID | User Story | Priority | Points | Status |
|-------|-----------|----------|--------|--------|
| **US-01** | As a dev, I want a GitHub repo with branching strategy so the team can collaborate | High | 2 | ✅ Done |
| **US-02** | As a dev, I want a Notion documentation pipeline so progress is tracked | High | 2 | ✅ Done |
| **US-03** | As a dev, I want a defined system architecture so everyone aligns on the design | High | 3 | ✅ Done |

**Sprint 1 Points**: 7 | **Completed**: 7 ✅

---

## Epic 2: Document Ingestion Pipeline 🟡 **SPRINT 2 — IN PROGRESS**

| US ID | User Story | Priority | Points | Status |
|-------|-----------|----------|--------|--------|
| **US-04** | As an admin, I want to upload PDF/DOCX/TXT files so they enter the system | High | 5 | 🟡 In Progress |
| **US-05** | As the system, I want to extract and clean text from documents automatically | High | 5 | ⏳ Planned |
| **US-06** | As the system, I want to split documents into chunks preserving context | High | 5 | ⏳ Planned |
| **US-07** | As the system, I want to generate embeddings for each chunk using a local model | High | 8 | ⏳ Planned |
| **US-08** | As the system, I want to store embeddings in Qdrant for retrieval | High | 5 | ⏳ Planned |

**Sprint 2 Points**: 28 | **Completed**: 0 | **In Progress**: 5 | **Planned**: 23

**Acceptance Criteria** (US-04):
- [ ] Admin can upload PDF, DOCX, or TXT files
- [ ] File size limit enforced (default 50MB)
- [ ] File validation (type & integrity)
- [ ] Async processing with status tracking
- [ ] Success/error notifications
- [ ] Files stored in secure location

**Acceptance Criteria** (US-05):
- [ ] Extract plain text from all supported formats
- [ ] Remove headers, footers, and metadata
- [ ] Normalize whitespace and encoding
- [ ] Preserve section structure

**Acceptance Criteria** (US-06):
- [ ] Split into semantic chunks (~1000 tokens)
- [ ] Maintain 200-token overlap
- [ ] Preserve document boundaries
- [ ] Support configurable chunk size

**Acceptance Criteria** (US-07):
- [ ] Use local embedding model (Sentence-BERT)
- [ ] Generate 384D vectors
- [ ] No external API calls
- [ ] Batch processing for efficiency

**Acceptance Criteria** (US-08):
- [ ] Store vectors in Qdrant
- [ ] Include metadata (doc_id, section, access_level)
- [ ] Support fast retrieval (<100ms)
- [ ] Handle duplicate prevention

---

## Epic 3: RAG & Q&A System ⏳ **SPRINT 3 — PLANNED**

| US ID | User Story | Priority | Points | Status |
|-------|-----------|----------|--------|--------|
| **US-09** | As an employee, I want to ask a question in natural language and get an answer | High | 8 | ⏳ Planned |
| **US-10** | As the system, I want to embed the user query and search Qdrant for similar chunks | High | 8 | ⏳ Planned |
| **US-11** | As the system, I want to inject retrieved context into the LLM prompt | High | 5 | ⏳ Planned |
| **US-12** | As the system, I want to perform a hallucination check on the generated answer | Medium | 5 | ⏳ Planned |
| **US-13** | As an employee, I want to see which documents the answer came from (source citation) | Medium | 3 | ⏳ Planned |

**Sprint 3 Points**: 29

---

## Epic 4: Auth & Security ⏳ **SPRINT 4 — PLANNED**

| US ID | User Story | Priority | Points | Status |
|-------|-----------|----------|--------|--------|
| **US-14** | As a user, I want to log in with credentials so access is secure | High | 5 | ⏳ Planned |
| **US-15** | As an admin, I want role-based access so employees only see permitted documents | High | 8 | ⏳ Planned |
| **US-16** | As the system, I want to log all queries and access events for compliance | High | 5 | ⏳ Planned |
| **US-17** | As a dev, I want all data to stay on-premise with no external API calls | High | 3 | ⏳ Planned |

**Sprint 4 Points**: 21

---

## Epic 5: UI & Deployment ⏳ **SPRINT 5 — PLANNED**

| US ID | User Story | Priority | Points | Status |
|-------|-----------|----------|--------|--------|
| **US-18** | As an employee, I want a clean web interface to ask questions and read answers | High | 8 | ⏳ Planned |
| **US-19** | As an admin, I want a panel to upload and manage documents | Medium | 5 | ⏳ Planned |
| **US-20** | As a dev, I want the full system deployable locally with one command | Medium | 5 | ⏳ Planned |
| **US-21** | As a dev, I want system performance tested and documented | Medium | 3 | ⏳ Planned |

**Sprint 5 Points**: 21

---

## Backlog Statistics

| Metric | Value |
|--------|-------|
| **Total User Stories** | 21 |
| **Total Points** | 106 |
| **Completed (Sprint 1)** | 3 US / 7 points |
| **In Progress (Sprint 2)** | 1 US / 5 points |
| **Remaining** | 17 US / 94 points |

---

## Priority Levels

- **High**: Critical for MVP, must complete
- **Medium**: Important but can be deferred
- **Low**: Nice-to-have, lowest priority

## Point Estimation Guide

- **2 points**: Small task, <4 hours
- **3 points**: Medium task, <8 hours
- **5 points**: Larger task, 1-2 days
- **8 points**: Complex task, 2-3 days

---

## Next Steps

1. **Sprint 2 (Current)**:
   - Finalize file upload endpoint (US-04)
   - Implement text extraction (US-05)
   - Begin chunking logic (US-06)

2. **Sprint 3 Prep**:
   - Finish embedding generation (US-07, US-08)
   - Review RAG architecture
   - Set up LLM environment (Ollama)

3. **Sprint 4 Prep**:
   - Design auth schemas
   - Plan RBAC implementation
   - Audit logging requirements

4. **Sprint 5 Prep**:
   - Frontend component design
   - Docker deployment testing
   - Performance profiling strategy

---

**Last Updated**: April 2025  
**Next Review**: End of Sprint 2
