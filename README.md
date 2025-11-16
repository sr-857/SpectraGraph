# 🌌 SpectraGraph

[![License: AGPL-3.0](https://img.shields.io/badge/License-AGPL--3.0-blue.svg)](./LICENSE)
[![Ethical Software](https://img.shields.io/badge/ethical-use-blue.svg)](./ETHICS.md)

> _SpectraGraph is an open-source OSINT intelligence studio for ethical investigations, transparent reporting, and repeatable graph analysis._

SpectraGraph empowers analysts, journalists, and incident responders to map relationships across digital footprints without sacrificing data custody.

✨ **Why users love it**

- ⚡️ Graph-first workspace with fluid rendering and multiple visual modes
- 🧠 Live, modular transforms that enrich entities as you explore
- 🛡️ Built for rigorous, defensible investigation workflows end to end

<img width="1439" height="899" alt="SpectraGraph interface" src="https://github.com/user-attachments/assets/01eb128e-bef4-486e-9276-c4da58f829ae" />

---

## 🚀 Quick start

### ✅ Prerequisites

- Docker
- Make

### 🏁 Install & launch (production)

```bash
git clone https://github.com/sr-857/SpectraGraph.git
cd SpectraGraph
make prod
```

Then head to [http://localhost:5173/register](http://localhost:5173/register) to create your first workspace.

> 🔐 SpectraGraph keeps every investigation on your own hardware—perfect for sensitive OSINT.

### 👨‍💻 Development mode

```bash
make dev
```

The live dev environment runs at [http://localhost:5173](http://localhost:5173).

---

## 🧰 Feature catalogue

SpectraGraph ships with an expanding library of transforms that augment your graphs in real time.

### 🌐 Domain transforms

- Reverse DNS Resolution – find domains pointing to an IP
- DNS Resolution – resolve a domain to IP addresses
- Subdomain Discovery – enumerate subdomains
- WHOIS Lookup – retrieve domain registration records
- Domain to Website – convert a domain into a website entity
- Domain to Root Domain – extract the registrable domain
- Domain to ASN – identify autonomous systems for a domain
- Domain History – review historical DNS data

### 🛰️ IP transforms

- IP Information – geolocation and network metadata
- IP to ASN – map an IP address to its AS number

### 🏢 ASN transforms

- ASN to CIDRs – list allocated IP ranges

### 📡 CIDR transforms

- CIDR to IPs – enumerate hosts in a range

### 📱 Social media transforms

- Maigret – sweep usernames across social platforms

### 🏛️ Organisation transforms

- Organisation to ASN – discover owned ASNs
- Organisation Information – enrich with company details
- Organisation to Domains – enumerate related domains

### 💸 Cryptocurrency transforms

- Wallet to Transactions – review transaction history
- Wallet to NFTs – surface associated NFT assets

### 🌍 Website transforms

- Website Crawler – map site structure
- Website to Links – extract outbound links
- Website to Domain – normalise URLs into domains
- Website to Webtrackers – flag analytics and tracking scripts
- Website to Text – capture textual content

### ✉️ Email transforms

- Email to Gravatar – pivot into Gravatar profiles
- Email to Breaches – check breach datasets
- Email to Domains – list domains tied to an address

### ☎️ Phone transforms

- Phone to Breaches – identify breached numbers

### 🧑‍💼 Individual transforms

- Individual to Organisation – surface affiliations
- Individual to Domains – enumerate owned domains

### 🔄 Integration transforms

- n8n Connector – wire SpectraGraph into automation workflows

---

## 🏗️ Architecture at a glance

SpectraGraph is modular by design, with clear contracts between services:

- **flowsint-core** — orchestration utilities, vault, Celery tasks, and base classes
- **flowsint-types** — Pydantic models shared across modules
- **flowsint-transforms** — data collectors and enrichment tooling
- **flowsint-api** — FastAPI service exposing REST endpoints and authentication
- **flowsint-app** — React frontend for graph visualization and case management

Dependencies flow in a single direction:

```
flowsint-app (frontend)
    ↓
flowsint-api (API server)
    ↓
flowsint-core (orchestrator, tasks, vault)
    ↓
flowsint-transforms (transforms & tools)
    ↓
flowsint-types (types)
```

---

## 🔄 Development workflow

1. **Add new types** in `flowsint-types`
2. **Add new transforms** in `flowsint-transforms`
3. **Expose APIs** in `flowsint-api`
4. **Extend utilities** in `flowsint-core`
5. **Update UI** in `flowsint-app`

## ✅ Testing

Each module maintains its own scoped test suite:

```bash
# Test core module
cd flowsint-core
poetry run pytest

# Test types module
cd ../flowsint-types
poetry run pytest

# Test transforms module
cd ../flowsint-transforms
poetry run pytest

# Test API module
cd ../flowsint-api
poetry run pytest
```

---

## 🧑‍🚀 Project steward

- **Lead & Maintainer:** sr-857

For collaboration inquiries, open an issue or reach out directly.

---

## ⚖️ Legal & ethical use

SpectraGraph is designed **strictly for lawful, ethical investigation and research**. Please read [ETHICS.md](./ETHICS.md) before running any operation.

The project exists to support:

- Cybersecurity researchers and threat intelligence teams
- Journalists and OSINT investigators
- Fraud and incident response analysts
- Organisations performing internal risk assessments

**Do not use SpectraGraph for:**

- Unauthorised surveillance or data collection
- Harassment, doxxing, or targeting of individuals
- Disinformation campaigns or privacy violations

Any misuse violates the principles outlined in [ETHICS.md](./ETHICS.md).

---

## 📄 License

Distributed under the [AGPL-3.0 license](./LICENSE).
