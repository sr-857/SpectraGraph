# 🌌 SpectraGraph

[![License: AGPL-3.0](https://img.shields.io/badge/License-AGPL--3.0-blue.svg)](./LICENSE)
[![Ethical Software](https://img.shields.io/badge/ethical-use-blue.svg)](./ETHICS.md)

> _SpectraGraph is an open-source OSINT intelligence studio for ethical investigations, transparent reporting, and repeatable graph analysis._

SpectraGraph empowers analysts, journalists, and incident responders to map relationships across digital footprints without sacrificing data custody.

✨ **Why users love it**

- ⚡️ Graph-first workspace with fluid rendering and multiple visual modes
- 🧠 Live, modular transforms that enrich entities as you explore
- 🛡️ Built for rigorous, defensible investigation workflows end to end

## 🚀 Overview
SpectraGraph is a modular OSINT enrichment platform built as a production‑grade distributed system, designed for scalable intelligence gathering. It uses a layered architecture—frontend → API → orchestration core → transforms → shared types—and integrates Postgres, Redis, and Neo4j through a Celery‑based workflow engine.

This structure allows SpectraGraph to ingest an entity (domain, IP, phone, crypto, org, etc.), schedule distributed enrichments, and return structured intelligence suitable for graphs, investigations, and automated analytics.

SpectraGraph is built for teams that need:

- Extensible OSINT transforms
- Distributed execution at scale
- Typed entities across multiple data sources
- Real-time investigation workflows

## 🧩 Monorepo Layout
SpectraGraph uses a Poetry workspace with multiple Python packages and a separate frontend.

```
SpectraGraph/
│
├── spectragraph-core/         # Orchestration, Celery, vault, graph & utils
├── spectragraph-types/        # Pydantic entity models shared everywhere
├── spectragraph-transforms/   # All OSINT transforms (domain, IP, crypto…)
├── spectragraph-api/          # FastAPI service, routers, migrations
├── spectragraph-app/          # Vite/React frontend
│
├── docker-compose.yml         # Base Compose
├── docker-compose.dev.yml     # Dev stack (Postgres, Redis, Neo4j, API, worker)
├── docker-compose.prod.yml    # Prod stack
├── Makefile                   # Dev / prod / install workflows
├── README.md                  # Docs
├── ETHICS.md                  # Responsible use guidelines
└── DISCLAIMER.md              # Legal positioning
```

## 🏗 Architecture

![SpectraGraph Architecture](docs/assets/architecture.svg)

> Diagram: Frontend → API → Core (Orchestrator/Celery) → Transforms → Types.  
> Datastores: Postgres, Neo4j. Broker: Redis. Vault for secrets. Worker pool executes transforms.

**How judges should test (30–60s):**
1. Start dev stack: `make dev` (requires Docker).  
2. Open UI: `http://localhost:3000` (or deployed URL).  
3. Trigger an investigation for `example.com` or `demo.owasp-juice.shop`.  
4. Verify: transform results appear, graph links stored in Neo4j, HTML report downloadable.

SpectraGraph is structured to enforce clean dependency boundaries:

**Frontend → API → Core → Transforms → Types**

This prevents cycles and keeps the system modular.

### 🔹 Frontend (`spectragraph-app/`)
- Vite + React
- Investigation UI, entity views, and transform triggers

### 🔹 API (`spectragraph-api/`)
- FastAPI service
- Routes: investigations, transforms, health, sketches
- Alembic migrations for Postgres
- Orchestrates Celery tasks

### 🔹 Core (`spectragraph-core/`)
- Celery worker setup
- Vault + secret resolution
- Graph clients
- Base `Transform` class
- Task lifecycle: init → preprocess → scan → normalize

### 🔹 Transforms (`spectragraph-transforms/`)
- OSINT enrichers for:
  - Domain
  - IP
  - Email
  - Phone
  - Crypto
  - Social
  - Leak databases
- Each transform:
  - Subclasses `Transform`
  - Declares `params_schema`
  - Uses vault-secured secrets when required
  - Implements `preprocess()` and `scan()`

### 🔹 Types (`spectragraph-types/`)
- Shared Pydantic models defining all entity types
- Consumed across API, core, and transforms

```
Frontend (Vite/React)
   │
   ▼
API (FastAPI)
   │
   ▼
Core (Celery Orchestrator)
   │
   ▼
Transforms (OSINT Enrichers)
   │
   ▼
Types (Pydantic Models)

Core → Postgres (relational storage)
Core → Neo4j (graph index)
Core → Redis (Celery broker)
API  → Postgres / Neo4j / Redis for reads & task enqueueing
```

> Architecture cheat sheet

| Layer | Primary Tech | Responsibilities | Key Integrations |
| --- | --- | --- | --- |
| 🎨 Frontend | Vite · React · TypeScript | Drive investigative UI, dashboards, live updates | REST + WebSocket calls to API |
| 🚪 API Gateway | FastAPI | Auth, validation, rate limiting, GraphQL-ready endpoints | Calls Core, reads Postgres/Neo4j |
| 🧠 Core Orchestrator | Celery · Async I/O | Dispatch transforms, manage jobs, marshal secrets | Uses Redis broker, persists to Postgres/Neo4j |
| 🔍 Transform Workers | Python OSINT plugins | Run enrichment scans, normalize outputs | Pull secrets from Vault, reuse Shared Types |
| 🧱 Shared Types | Pydantic models | Single source of truth for domain schemas | Imported across API/Core/Transforms |
| 🗄️ Storage Layer | Postgres · Neo4j | Persist entities, relationships, audit logs | Read by API/Core, visualized in UI |
| ⚡ Messaging | Redis | Task queue + cache for hot entities | Backed by Celery + API prefetch |

## 📸 Preview

![SpectraGraph dashboard](docs/assets/screenshots/dashboard.png)

> Dashboard layout showing timeline widgets, trend cards, and investigation queue.

**Mission pipeline**

1. 🧑‍💻 Analyst triggers scan from the UI.
2. 🚀 API validates payload, enriches with baseline context.
3. 🧠 Core fans out Celery tasks with vault-secured parameters.
4. 🛰️ Transforms gather OSINT signals and emit typed intel.
5. 🗃️ Results land in Postgres (facts) and Neo4j (graph edges).
6. 📊 UI auto-refreshes dashboards via websockets + cached reads.

## 🔄 Data Flow
1. Frontend issues REST/WebSocket call
2. API schedules Celery jobs
3. Core resolves secrets and validates params
4. Transform executes enrichment logic
5. Results persist to Postgres / Neo4j
6. API returns intelligence to the UI

## ⚙️ Setup
1. Clone the repository and enter the workspace.
2. Copy the sample environment file: `cp .env.example .env`.
3. Update secrets and connection strings before running services.

### Required environment variables

| Variable | Purpose | Example |
| --- | --- | --- |
| `NODE_ENV` | Sets frontend build mode | `development` |
| `MASTER_VAULT_KEY_V1` | 32-byte base64 key for vault encryption | `base64:qnHTmwYb...` |
| `DATABASE_URL` | Postgres DSN for API and workers | `postgresql://spectragraph:spectragraph@localhost:5433/spectragraph` |
| `NEO4J_URI_BOLT` | Neo4j connection string | `bolt://neo4j:7687` |
| `NEO4J_USERNAME` / `NEO4J_PASSWORD` | Neo4j credentials | `neo4j` / `password` |
| `REDIS_URL` | Celery broker / cache endpoint | `redis://redis:6379/0` |
| `VITE_API_URL` | Frontend → API base URL | `http://127.0.0.1:5001` |

> Tip: regenerate `MASTER_VAULT_KEY_V1` via `python -c "import os, base64; print('base64:' + base64.b64encode(os.urandom(32)).decode())"` for production deployments.

## 🛠 Development Workflow

Install Python deps:

```bash
poetry install
```

Install frontend deps:

```bash
npm install
```

Start the dev environment (Postgres, Redis, Neo4j, API, Worker, Frontend):

```bash
make dev
```

Docker is required. On systems without Docker, install Docker CLI or Podman with Docker compatibility.

## 🔗 Demo Checklist
- Start the full stack: `make dev` (brings up Postgres, Redis, Neo4j, API, worker, frontend).
- Open the UI at `http://localhost:3000` (or your deployed URL) and log in if required.
- Launch an investigation for `example.com` or `demo.owasp-juice.shop`.
- Confirm results populate the dashboard, graph links land in Neo4j, and the HTML report is downloadable.
- Review `docs/HACKATHON_BOOTSTRAP.md` for the end-to-end judge script and troubleshooting tips.

## 🧪 Testing
Each module has its own pytest suite:

```bash
cd spectragraph-core && poetry run pytest
cd ../spectragraph-transforms && poetry run pytest
cd ../spectragraph-api && poetry run pytest
```

### Known Issues
- Vault tests expect soft-fail behavior; `resolve_params()` currently raises when secrets are missing. Decide whether to revert to logging fallback or update tests to match the stricter behavior.
- Postgres connection errors occur when Docker is not running.

## 🐳 Production Deployment

```bash
make prod
```

This brings up FastAPI (uvicorn), a Celery worker, Postgres, Redis, and Neo4j. Alembic migrations run automatically.

## 🔐 Ethics & Safety
SpectraGraph is an OSINT enrichment tool. It:

- Does not perform intrusive scanning
- Requires API keys for sensitive integrations
- Adheres to responsible-use policies (see `ETHICS.md`)

## 🗺 Roadmap
- Websocket investigation streams
- Transform marketplace
- Entity graph visualizations
- Rate-limited API gateway
- Advanced entity linking

## 📄 License
AGPL-3.0

## 🙌 Credits
Built for scalable OSINT investigations, distributed enrichment, and real-time intelligence workflows.
