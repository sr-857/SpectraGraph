# Contributing to SpectraGraph

Thank you for your interest in contributing to **SpectraGraph** 🌌  
SpectraGraph is a production-grade OSINT intelligence platform designed for ethical investigations, transparent reporting, and repeatable graph analysis.

Because of its **multi-service architecture** and **ethical constraints**, contributions must follow clear guidelines. This document explains how to get started, where changes belong, and how to submit high-quality pull requests.

Please read this document fully before contributing.

---

## 🧠 Project Philosophy

SpectraGraph is built around three core principles:

1. **Architectural integrity**  
   Clear boundaries between frontend, API, orchestration, transforms, and shared types.

2. **Ethical OSINT practices**  
   No intrusive scanning, no abuse-enabling features, no unsafe defaults.

3. **Production-grade reliability**  
   Typed data models, test coverage, and predictable workflows.

Contributions that violate these principles will not be accepted.

---

## 🧩 Repository Overview & Architecture Boundaries

SpectraGraph is a monorepo with **strict dependency direction**:
**Frontend → API → Core → Transforms → Types** 

### Monorepo Layout
SpectraGraph/
├── spectragraph-core/ # Orchestration, Celery, vault, graph logic
├── spectragraph-types/ # Shared Pydantic entity models
├── spectragraph-transforms/ # OSINT enrichment plugins
├── spectragraph-api/ # FastAPI service
├── spectragraph-app/ # Vite/React frontend
├── docker-compose*.yml
├── Makefile
├── ETHICS.md
├── DISCLAIMER.md
└── CONTRIBUTING.md


### Architectural Rules (Important)

- **Frontend** may only talk to the API
- **API** may call Core and read storage
- **Core** orchestrates Celery tasks and secrets
- **Transforms** must be stateless and isolated
- **Types** are the single source of truth for schemas

❌ Do not introduce circular dependencies  
❌ Do not bypass Core to call Transforms directly  
❌ Do not duplicate entity schemas outside `spectragraph-types`

---

## 🚀 Getting Started (Development Setup)

### Prerequisites

- Docker (required)
- Python 3.10+
- Poetry
- Node.js (for frontend)

---

### Clone the Repository

```bash
git clone https://github.com/<your-username>/spectragraph.git
cd spectragraph
```

### Environment Setup
```cp .env.example .env```


Populate required environment variables before starting services.

**Install Dependencies**
+ Python (workspace)
```poetry install```

+ Frontend
```bash
cd spectragraph-app
npm install
```

+ Start the Development Stack
```make dev```


***This launches:***

* Postgres
* Redis
* Neo4j
* FastAPI
* Celery worker
* Fronend UI

***Access the UI at:***
```http://localhost:3000```


***Stop everything with:***
```make down```

### 🧪 Testing Requirements

**Each module has its own test suite.**

***Core**
```bash
cd spectragraph-core
poetry run pytest
```

***Transforms***
```bash
cd spectragraph-transforms
poetry run pytest
```

***API***
```bash
cd spectragraph-api
poetry run pytest
```

**✅ Tests must pass before opening a PR**
**❌ PRs without tests (where applicable) may be rejected**

### 🧱 Where to Add Changes
**Adding a New Transform**
* Location: spectragraph-transforms/

* Must subclass Transform
* Must declare params_schema
* Must implement:
    + preprocess()
    + scan()
    + Secrets must be retrieved via Vault
    + No direct network abuse or scraping beyond ethical OSINT norms

**Adding or Modifying Entity Schemas**
* Location: spectragraph-types/
* Use Pydantic models only
* Changes here impact multiple services
* Breaking schema changes require discussion first

**API Changes**
* Location: spectragraph-api/
* Use FastAPI routing conventions
* Validate inputs strictly
* No business logic leakage into API routes

**Frontend Changes**
* Location: spectragraph-app/
* Must respect investigation workflows
* UI should not expose unsafe or misleading actions

### 🌿 Branching & Commit Guidelines
***Branch Naming***
```bash
feature/<short-description>
fix/<short-description>
docs/<short-description>
```

Example:
`git checkout -b feature/domain-transform`

***Commit Messages***
Use clear, descriptive messages:
```bash
feat: add domain enrichment transform
fix: handle missing vault secrets gracefully
docs: clarify investigation workflow
```

### 🔁 Pull Request Guidelines

When opening a PR:
* Target the main branch
* Keep PRs focused (one concern per PR)
* Explain what changed and why
* Link related issues if applicable
* Include screenshots for UI changes
* PRs may be requested to:
* Add tests
* Split changes
* Adjust architecture placement

### 🔐 Ethics, Safety & Responsible Disclosure

SpectraGraph is an OSINT platform. All contributors must follow ethical guidelines.

**Read and follow ETHICS.md**
+ Do not add features that:
+ Enable intrusive scanning
+ Circumvent safeguards
+ Encourage misuse
+ Security issues should be reported privately, not via public issues
+ If unsure, open a discussion before coding.

### 📎 Final Notes

***SpectraGraph is intentionally strict about structure and ethics.***
***This keeps the platform reliable, defensible, and scalable.***

**Thank you for contributing responsibly 🌌**