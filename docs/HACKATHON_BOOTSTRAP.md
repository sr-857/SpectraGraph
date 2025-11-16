# SpectraGraph Hackathon Bootstrap

## 1. Environment Setup

### Install tooling

1. **Node & npm** (>= v22 recommended)
2. **Python** 3.12+
3. **Poetry** (`pipx install poetry`)
4. **Docker Desktop / Podman** with Compose plugin
5. Optional: `just`, `make`

### System dependencies

```bash
# Fedora / RHEL
yum install -y cairo-devel pkg-config python3-devel libjpeg-turbo-devel # Cairo, imaging

# Debian / Ubuntu
sudo apt-get update && sudo apt-get install -y libcairo2-dev pkg-config python3-dev libjpeg-dev
```

## 2. Project bootstrap

```bash
# 1. Clone
 git clone https://github.com/sr-857/SpectraGraph.git
 cd SpectraGraph

# 2. Python deps
poetry env use 3.12
poetry install --with dev

# 3. Frontend deps
cd spectragraph-app
npm install
cd ..

# 4. Environment variables
cp .env.example .env
```

Populate `.env` with credentials, pointing vault-backed secrets to placeholder values for local testing.

## 3. Services & data

```bash
# Start backing services
Docker compose -f docker-compose.dev.yml up postgres redis neo4j -d

# Run migrations & seeds
poetry run alembic upgrade head
poetry run spectragraph-core/bin/seed_demo_data.py
```

## 4. Running the stack

```bash
# API + workers
poetry run uvicorn spectragraph_api.main:app --reload
poetry run celery -A spectragraph_core.tasks worker -l info

# Frontend (new terminal)
cd spectragraph-app
npm run dev -- --host 0.0.0.0 --port 5173
```

Visit:
- API health: `http://localhost:5001/health`
- Web UI: `http://localhost:5173`

## 5. Test & build smoke checks

```bash
poetry run pytest spectragraph-core
cd spectragraph-app && npm run build && cd ..
```

## 6. Demo script

1. **Brief architecture overview** using README diagram + ASCII flow.
2. **Launch UI**, log in, and trigger a transform from catalog.
3. Show **live job status** in UI (Redis/Celery pipeline).
4. Open Neo4j Bloom (optional) for graph visualization.
5. Close with **automation story**: Celery workers, typed models, vault secrets.

## 7. Troubleshooting quick hits

| Symptom | Fix |
| --- | --- |
| `poetry install` fails on Cairo | Install `cairo-devel`/`libcairo2-dev` |
| Docker not found | Install Docker CLI or `podman-docker` |
| Vault secret missing | Transform logs now report missing keys clearly |
| Frontend ws errors | Ensure API running on `http://localhost:5001` |

## 8. Optional polish

- Run `npm audit fix` ahead of judging.
- Pre-load demo data + saved graph views in Neo4j.
- Record short video walkthrough for asynchronous judging.
