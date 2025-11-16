# SpectraGraph
Open-Source OSINT Intelligence Platform
Distributed Transforms • Graph-Driven Enrichment • API + Worker Pipeline • Multi‑Module Architecture

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
SpectraGraph is structured to enforce clean dependency boundaries:

**Frontend → API → Core → Transforms → Types**

This prevents cycles and keeps the system modular.

![SpectraGraph Architecture](docs/assets/architecture.svg)

> Diagram: frontend → API → core → transforms → types with Postgres, Neo4j, Redis, Vault, and Celery worker pool.

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

```mermaid
flowchart LR
  FE[Frontend] -->|WS / REST| API[API (FastAPI)]
  API --> CORE[Core (Orchestrator / Celery)]
  CORE --> TRANS[Transforms (OSINT Enrichers)]
  TRANS --> TYPES[Types (Pydantic Models)]
  CORE -->|writes| PG[(Postgres)]
  CORE -->|writes| NEO[(Neo4j)]
  CORE -->|uses| REDIS[(Redis / Celery Broker)]
  API -->|reads| PG
  API -->|reads| NEO
  API -->|enqueues| REDIS
  FE --- API
```

## 🔄 Data Flow
1. Frontend issues REST/WebSocket call
2. API schedules Celery jobs
3. Core resolves secrets and validates params
4. Transform executes enrichment logic
5. Results persist to Postgres / Neo4j
6. API returns intelligence to the UI

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
