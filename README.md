<h1>

  <img src="i.png" width="120" style="vertical-align: middle; margin-right: 6px;" />

  SpectraGraph

</h1>



 The Open-Source OSINT Intelligence Studio , Ethical investigations, transparent reporting, and repeatable graph analysis.



![License: AGPL-3.0](https://img.shields.io/badge/License-AGPL--3.0-blue.svg?style=for-the-badge)

![Docker Support](https://img.shields.io/badge/Docker-Supported-blue?style=for-the-badge&logo=docker)

![Build Status](https://img.shields.io/badge/Build-Passing-brightgreen?style=for-the-badge)



<p align="center">

  <img src="https://img.shields.io/badge/SWoC-2026-orange?style=for-the-badge" alt="SWoC 2026 Badge" />

  &nbsp;&nbsp;

  <img src="i5.png" alt="SWoC Logo" height="100" style="vertical-align: middle;" />

</p>

[Explore Live Demo](https://sr-857.github.io/SpectraGraph/landing/) | [Report a Bug](https://github.com/sr-857/SpectraGraph/issues) | [SWoC Guide](./docs/HACKATHON_BOOTSTRAP.md)

---



## ✨ Why SpectraGraph?



**SpectraGraph** enables analysts, journalists, and incident responders to discover, analyze, and visualize relationships across digital footprints—without compromising data ownership or investigative integrity.



- ⚡ **Graph-first workspace**  

  Intuitive, high-performance graph visualizations with multiple viewing modes for exploring complex relationships.



- 🧠 **Live, modular transforms**  

  Plug-and-play enrichment modules that dynamically expand entities as investigations progress.



- 🛡️ **Built for investigative rigor**  

  End-to-end traceability ensures workflows remain transparent, reproducible, and defensible.



---



## 🏗 System Architecture



SpectraGraph is built using a **Producer–Consumer architecture**, enabling asynchronous processing of OSINT tasks. This design ensures scalability, responsiveness, and fault isolation across distributed components.





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



Get the **SpectraGraph Command Center** running locally in under 60 seconds.



> **Prerequisites**

> - Git installed

> - Docker & Docker Compose installed



### 1️⃣ Clone the Repository

```bash

git clone https://github.com/sr-857/SpectraGraph.git

cd SpectraGraph

```



### 2️⃣ Initialize Environment Variables

```bash

cp .env.example .env

```

💡 You can run SpectraGraph without adding any API keys initially.



### 3️⃣ Launch the Full Stack (Docker Required)

```bash

make dev

```



| Service | URL | Purpose |
| :--- | :--- | :--- |
| **Frontend** | `http://localhost:3000` | Investigative UI & Dashboard |
| **API Docs** | `http://localhost:5001/docs` | Swagger/OpenAPI interactive docs |
| **Neo4j** | `http://localhost:7474` | Direct Graph Database access |





---



## 🧩 Anatomy of a Transform



SpectraGraph uses **Transforms** to connect with external OSINT sources.  

Each transform is a **self-contained, modular unit**, making it easy to add new data sources without affecting the rest of the system.



All transforms live inside the:

```bash

spectragraph-transforms/

```



directory and follow a **consistent lifecycle**.





### 🔄 Transform Logic Flow



Every transform executes in three clear steps:



1. **Preprocess**  

   Validate the input entity  

   _Example: Check whether the provided value is a valid IPv4 address._



2. **Scan**  

   Securely authenticate using Vault and query the external OSINT API.



3. **Normalize**  

   Convert the raw API response into **shared Pydantic data models** so it can be stored and visualized consistently.



---



### 🧪 Minimal Transform Template



```python

class NewOSINTTransform(BaseTransform):

    """

    Example transform template.

    Subclass BaseTransform and implement the scan method.

    """



    def scan(self, target: str, api_key: str):

        # Call the external OSINT service

        results = call_external_api(target, api_key)



        # Normalize results into shared data models

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
| `DATABASE_URL` | PostgreSQL database connection | `postgresql://user:pass@localhost:5433/db` |
| `NEO4J_URI_BOLT` |Neo4j graph database (Bolt)| `bolt://neo4j:7687` |
| `REDIS_URL` | Redis message broker for Celery| `redis://redis:6379/0` |

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



1. **Check Docker is running**: 

```bash

docker ps

```



2. **Start services**: 

```bash

make dev

```

3. **Check health**: 

```bash

curl http://localhost:5001/health/db

```

4. **View logs**: 

```bash

docker-compose logs postgres

```

The application will automatically retry connections (5 times) and provide a detailed diagnostic message if it fails.


| Issue | Symptom | Solution |
| :--- | :--- | :--- |
| **Database Connection** | `Connection Refused` | Ensure Docker is running and ports `5433` (Postgres) and `7687` (Neo4j) are free. |
| **Celery Tasks Stuck** | Tasks remain 'Pending' | Check Redis logs: `docker logs spectragraph-redis`. Ensure the worker is initialized. |
| **UI Blank Screen** | `VITE_API_URL` error | Ensure `.env` has the correct API host (usually `http://localhost:5001`). |



For additional setup issues and resolutions, see the full [Troubleshooting Guide](./docs/TROUBLESHOOTING.md).



---



## 🖼️ View of the Website



Below are previews of the SpectraGraph web interface to help new users understand the look and workflow of the platform.





<img src="i1.png" alt="SpectraGraph Landing Page" width="100%" />



---





<img src="i2.png" alt="SpectraGraph Investigation Dashboard" width="100%" />



---





<img src="i3.png" alt="SpectraGraph Graph View" width="100%" />



---





<img src="i4.png" alt="SpectraGraph Transform Panel" width="100%" />







---



## 🗺 SWoC 2026 Roadmap



- [ ] **Websocket Streams:** Real-time investigation status updates.

- [ ] **Transform Marketplace:** Plugin-style architecture for easy community PRs.

- [ ] **Visual Overhaul:** Dark-mode "Command Center" UI aesthetics.



**Contributing:** Please read [CONTRIBUTING.md](./CONTRIBUTING.md) and look for the `SWoC` label on issues!



---



### 🌟 Hall of Fame



<a href="https://github.com/sr-857/SpectraGraph/graphs/contributors">

  <img src="https://contrib.rocks/image?repo=sr-857/SpectraGraph&max=300" />

</a>



### _Want to see your avatar here? [Make your first contribution today!](CONTRIBUTING.md)_



## 📄 License



Licensed under **AGPL-3.0**. See the [LICENSE](./LICENSE) file for the full text.



---



> **Note:** SpectraGraph is built for ethical investigations. Please ensure your use cases adhere to our [Ethics & Safety Guidelines](./ETHICS.md).

