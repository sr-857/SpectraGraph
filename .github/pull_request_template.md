## 🌌 SpectraGraph Pull Request

### 🔗 Linked Issue
Closes #

---

### 🛠 Type of Change
- [ ] **New Transform (OSINT Source)** – Adding a modular enrichment tool.
- [ ] **Core Logic / API** – Backend, Database (Postgres/Neo4j), or Celery logic.
- [ ] **UI / Dashboard Enhancement** – Frontend updates to the "Command Center".
- [ ] **Bug Fix** – Resolving an existing issue.
- [ ] **Documentation** – Updates to README or Guides.

---

### 🧩 Transform Lifecycle Checklist
*Only required for contributions in `spectragraph-transforms/`*

- [ ] Does the transform correctly subclass `BaseTransform`?
- [ ] Is there input validation for entities (IP, Domain, Hash, etc.)?
- [ ] Are **Shared Pydantic Types** used for data normalization?
- [ ] Has the API key been added to `.env.example` (if applicable)?

---

### 🧪 Testing Evidence
**Mandatory:** Please provide logs or output demonstrating that your changes work. 
- Output from `make dev`:
```text
# Paste logs here
```

---

### 🖼 Visuals

#### Required for UI/Dashboard enhancements.

##### 🛡 Ethical Review & Quality Assurance
- [ ] I have read the SWoC Guide and `CONTRIBUTING.md`.
- [ ] **Ethical Alignment:** My contribution adheres to the SpectraGraph Ethics & Safety Guidelines for transparent, defensible investigations.
- [ ] My code follows the project's linting and formatting standards.

