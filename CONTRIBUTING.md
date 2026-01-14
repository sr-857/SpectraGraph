# Contributing to SpectraGraph

Thank you for your interest in contributing to **SpectraGraph** 🌌  
SpectraGraph is a **production-grade OSINT intelligence platform** designed for ethical investigations, transparent reporting, and repeatable graph-based analysis.

Because SpectraGraph operates across **multiple services**, handles **sensitive intelligence workflows**, and enforces **strict ethical boundaries**, contributions must follow clearly defined rules.

This document explains:
- How to get started
- How the architecture is structured
- Where different kinds of changes belong
- How to submit high-quality, reviewable pull requests

> ⚠️ Please read this document fully before contributing.  
> Pull requests that do not follow these guidelines may be closed without review.

---

## 🧠 Project Philosophy (Non-Negotiable)

SpectraGraph is built around three core principles.  
All contributions are evaluated against them.

### 1. Architectural Integrity
- Clear, enforced boundaries between services
- Strict dependency direction
- No hidden coupling or shortcuts

### 2. Ethical OSINT Practices
- No intrusive scanning
- No abuse-enabling features
- No unsafe defaults
- No functionality designed to evade safeguards

### 3. Production-Grade Reliability
- Typed data models
- Test coverage where applicable
- Predictable, repeatable workflows

❌ Contributions that violate these principles **will not be accepted**.

---

## 🧩 Repository Architecture & Dependency Model

SpectraGraph is a **monorepo** with a **strict, one-directional dependency flow**:


Dependencies may only flow **downward**.

---

## 📁 Repository Layout

```
SpectraGraph/
├── spectragraph-core/ # Orchestration, Celery, vault, graph logic
│ ├── workflows/ # Investigation & execution workflows
│ ├── graph/ # Graph construction & traversal logic
│ ├── vault/ # Secrets & credential access layer
│ ├── tasks/ # Celery task definitions
│ └── tests/
│
├── spectragraph-types/ # Shared Pydantic schemas (single source of truth)
│ ├── entities/ # Entity models (IP, Domain, Email, etc.)
│ ├── relations/ # Graph edge definitions
│ └── tests/
│
├── spectragraph-transforms/ # Stateless OSINT enrichment plugins
│ ├── features/ # Individual enrichment features / transforms
│ │ ├── domain/ # Domain-related transforms
│ │ ├── ip/ # IP-related transforms
│ │ └── email/ # Email-related transforms
│ ├── base.py # Transform base class
│ └── tests/
│
├── spectragraph-api/ # FastAPI service layer
│ ├── routes/ # API route definitions
│ ├── schemas/ # Request/response validation
│ ├── dependencies/ # Auth, context, lifecycle hooks
│ └── tests/
│
├── spectragraph-app/ # Vite + React frontend
│ ├── features/ # UI feature modules
│ ├── components/ # Reusable UI components
│ ├── pages/ # Route-level pages
│ └── tests/
│
├── docker-compose*.yml
├── Makefile
├── ETHICS.md
├── DISCLAIMER.md
└── CONTRIBUTING.md
```


---

## 🧱 Architectural Rules (Strictly Enforced)

### Frontend
- May communicate **only** with the API
- No direct access to databases, Core, or Transforms
- Must respect investigation workflows and safety constraints

### API
- Handles request validation and response shaping
- May call Core and read storage
- ❌ Must not contain business or orchestration logic

### Core
- Central orchestration layer
- Manages Celery tasks, secrets, and execution flow
- Acts as the system’s control plane

### Transforms
- Must be **stateless and isolated**
- No shared state
- No orchestration logic
- No direct database access

### Types
- Single source of truth for schemas
- Shared across all services
- Pydantic models only

❌ No circular dependencies  
❌ No bypassing Core to call Transforms directly  
❌ No schema duplication outside `spectragraph-types`

---

## 🚀 Getting Started (Development Setup)

### Prerequisites
- Docker (**required**)
- Python 3.10+
- Poetry
- Node.js (for frontend)

---

### Clone the Repository

```bash
git clone https://github.com/<your-username>/spectragraph.git
cd spectragraph
```
Environment Configuration
```
cp .env.example .env
```
Install Dependencies Python (workspace)
```bash
poetry install
```
Frontend
```bash
cd spectragraph-app
npm install

```
Start the Development Stack
```bash
make dev
```

## ▶️ Start the Development Stack

```bash
# Start all services
make dev

# Access the UI
# http://localhost:3000

# Stop all services
make down

##Services Started

PostgreSQL
Redis
Neo4j
FastAPI
Celery worker
Frontend UI

```
🧪 Testing Requirements

```bash
# Core tests
cd spectragraph-core
poetry run pytest

# Transform tests
cd spectragraph-transforms
poetry run pytest

# API tests
cd spectragraph-api
poetry run pytest

```
Test Policy

✅ All tests must pass before opening a PR

❌ PRs without tests (where applicable) may be rejected

---

## 🧱 Where to Add Changes

### ➕ Adding a New Transform
**Location:** `spectragraph-transforms/features/`

**Requirements:**
- Must subclass `Transform`
- Must declare `params_schema`
- Must implement:
  - `preprocess()`
  - `scan()`
- Secrets must be retrieved via Vault
- No intrusive scanning or scraping beyond ethical OSINT norms

---

### 🧬 Adding or Modifying Entity Schemas
**Location:** `spectragraph-types/`

**Rules:**
- Pydantic models only
- Changes impact multiple services
- Breaking schema changes require prior discussion

---

### 🌐 API Changes
**Location:** `spectragraph-api/`

**Rules:**
- Follow FastAPI routing conventions
- Validate inputs strictly
- No business logic leakage into routes

---

### 🎨 Frontend Changes
**Location:** `spectragraph-app/`

**Rules:**
- Must respect investigation workflows
- Must not expose unsafe or misleading actions
- UX should reinforce ethical usage

---

## 🌿 Branching & Commit Guidelines

### Branch Naming
```text
feature/<short-description>
fix/<short-description>
docs/<short-description>

```

## 🔁 Pull Request Guidelines

### When opening a Pull Request:
- Target the `main` branch
- Keep PRs focused (one concern per PR)
- Clearly explain **what changed** and **why**
- Link related issues or discussions
- Include screenshots for UI changes (if applicable)

### PRs may be requested to:
- Add or improve tests
- Split changes into smaller PRs
- Adjust architectural placement to respect boundaries

---

## 🔐 Ethics, Safety & Responsible Disclosure

SpectraGraph is an **OSINT intelligence platform**.  
All contributors must follow strict ethical guidelines.

### Required:
- Read and follow `ETHICS.md`

### Do **NOT** add features that:
- Enable intrusive scanning
- Circumvent safeguards
- Encourage misuse or harm

### Security Disclosure:
- 🔒 Security vulnerabilities must be reported **privately**
- Do **not** disclose security issues via public issues or PRs

If you are unsure about a feature’s ethical or safety impact,  
**open a discussion before coding**.

---

## 📎 Final Notes

SpectraGraph is intentionally strict about structure, safety, and ethics.

This discipline keeps the platform:
- Reliable
- Defensible
- Scalable
- Trusted

**Thank you for contributing responsibly to SpectraGraph** 🌌
