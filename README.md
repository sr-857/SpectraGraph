# 🌌 SpectraGraph

<div align="center">

![SWoC 2026](https://img.shields.io/badge/SWoC-2026-orange?style=for-the-badge)
![License: AGPL-3.0](https://img.shields.io/badge/License-AGPL--3.0-blue.svg?style=for-the-badge)
![Docker Support](https://img.shields.io/badge/Docker-Supported-blue?style=for-the-badge&logo=docker)
![Build Status](https://img.shields.io/badge/Build-Passing-brightgreen?style=for-the-badge)

**The Open-Source OSINT Intelligence Studio** *Ethical investigations, transparent reporting, and repeatable graph analysis.*

[Explore Live Demo](https://sr-857.github.io/SpectraGraph/landing/) • [Report a Bug](https://github.com/your-repo/issues) • [SWoC Guide](./docs/HACKATHON_BOOTSTRAP.md)

</div>

---

## ✨ Why SpectraGraph?
SpectraGraph empowers analysts, journalists, and incident responders to map relationships across digital footprints without sacrificing data custody.

- ⚡️ **Graph-first workspace** with fluid rendering and multiple visual modes.
- 🧠 **Live, modular transforms** that enrich entities as you explore.
- 🛡️ **Built for rigor**, ensuring investigation workflows are defensible end-to-end.

---

## 🏗 System Architecture
Understanding the flow between the distributed components is essential for contributors. SpectraGraph uses a **Producer-Consumer** model to handle heavy OSINT workloads.

```mermaid
graph TD
    subgraph "Frontend Layer"
        UI[Vite/React Dashboard]
    end

    subgraph "API Gateway (FastAPI)"
        API[FastAPI Router]
        Vault[Vault Secret Manager]
    end

    subgraph "Orchestration"
        Broker((Redis Queue))
        Worker[Celery Transform Worker]
    end

    subgraph "Persistence Layer"
        PG[(PostgreSQL: Facts)]
        Graph[(Neo4j: Relationships)]
    end

    UI -->|Trigger Investigation| API
    API -->|Encrypt Secrets| Vault
    API -->|Enqueue Task| Broker
    Broker -->|Execute| Worker
    Worker -->|Fetch Signals| ExternalAPI[OSINT APIs]
    Worker -->|Store Facts| PG
    Worker -->|Map Edges| Graph
    Graph -->|Visual Sync| UI
```

---

## 🚀 1-Minute Quick Start
Get the "Command Center" running in under 60 seconds.

# 1. Clone the repo
```
git clone [https://github.com/sr-857/SpectraGraph.git](https://github.com/sr-857/SpectraGraph.git)
cd SpectraGraph
```

# 2. Initialize Environment
```
cp .env.example .env
```

# 3. Launch the Stack (Docker Required)
```
make dev
```

| Service | URL | Purpose |
| :--- | :--- | :--- |
| **Frontend** | `http://localhost:3000` | Investigative UI & Dashboard |
| **API Docs** | `http://localhost:5001/docs` | Swagger/OpenAPI interactive docs |
| **Neo4j** | `http://localhost:7474` | Direct Graph Database access |

--- 

## 🧩 Anatomy of a Transform
Adding a new OSINT source is modular. Every transform follows a strict lifecycle within the `spectragraph-transforms/` package.

### Logic Flow
1. **Preprocess:** Validate the entity (e.g., Is this a valid IPv4?).
2. **Scan:** Authenticate with Vault and call the external OSINT API.
3. **Normalize:** Map the raw JSON response to **Shared Pydantic Types**.

### Code Template
```python
class NewOSINTTransform(BaseTransform):
    """
    To contribute a new transform, subclass BaseTransform 
    and implement the scan logic.
    """
    def scan(self, target: str, api_key: str):
        # Your logic here
        results = call_external_api(target, api_key)
        return self.normalize(results)
```

---

## ⚙️ Configuration
The system environment is split into logical categories for better scannability.

<details>
<summary><b>🔑 Core & Security (Click to expand)</b></summary>

| Variable | Purpose | Default |
| :--- | :--- | :--- |
| `NODE_ENV` | Build mode | `development` |
| `MASTER_VAULT_KEY_V1` | 32-byte base64 key for encryption | `Required` |

</details>

<details>
<summary><b>🗄️ Database & Broker (Click to expand)</b></summary>

| Variable | Purpose | Example |
| :--- | :--- | :--- |
| `DATABASE_URL` | Postgres Connection | `postgresql://user:pass@localhost:5433/db` |
| `NEO4J_URI_BOLT` | Neo4j Connection | `bolt://neo4j:7687` |
| `REDIS_URL` | Celery Broker | `redis://redis:6379/0` |

</details>

<details>
<summary><b>🛰️ Transform API Keys (Click to expand)</b></summary>

| Variable | Source |
| :--- | :--- |
| `VT_API_KEY` | VirusTotal Intelligence |
| `SHODAN_KEY` | Shodan.io Search |

</details>

---

## ❓ Troubleshooting

### Database Connection Issues

If you see database connection errors during startup:

1. **Check Docker is running**: `docker ps`
2. **Start services**: `make dev`
3. **Check health**: `curl http://localhost:5001/health/db`
4. **View logs**: `docker-compose logs postgres`

The application will automatically retry connections (5 times) and provide a detailed diagnostic message if it fails.

| Issue | Symptom | Solution |
| :--- | :--- | :--- |
| **Database Connection** | `Connection Refused` | Ensure Docker is running and ports `5433` (Postgres) and `7687` (Neo4j) are free. |
| **Celery Tasks Stuck** | Tasks remain 'Pending' | Check Redis logs: `docker logs spectragraph-redis`. Ensure the worker is initialized. |
| **UI Blank Screen** | `VITE_API_URL` error | Ensure `.env` has the correct API host (usually `http://localhost:5001`). |

For additional setup issues and resolutions, see the full [Troubleshooting Guide](./docs/TROUBLESHOOTING.md).

---

## 🗺 SWoC 2026 Roadmap

- [ ] **Websocket Streams:** Real-time investigation status updates.
- [ ] **Transform Marketplace:** Plugin-style architecture for easy community PRs.
- [ ] **Visual Overhaul:** Dark-mode "Command Center" UI aesthetics.

**Contributing:** Please read [CONTRIBUTING.md](./CONTRIBUTING.md) and look for the `SWoC` label on issues!

---

## 📄 License

Licensed under **AGPL-3.0**. See the [LICENSE](./LICENSE) file for the full text.

---

> **Note:** SpectraGraph is built for ethical investigations. Please ensure your use cases adhere to our [Ethics & Safety Guidelines](./ETHICS.md).
