# 🛠 Troubleshooting Guide

This document lists common setup and development issues encountered while running SpectraGraph locally, along with their causes and resolutions.
If you encounter an issue not listed here, feel free to open an issue or submit a PR.

## Docker Services (Neo4j & Redis)

### Symptom
- `Connection refused` errors on ports `7474` (Neo4j) or `6379` (Redis)
- API fails to start or background tasks remain pending

### Cause
- Docker containers are not running
- Containers failed during startup
- Docker daemon is not active

### Solution
1. Verify Docker is running:
```bash
docker ps
```
2. Check container status:
```bash
docker-compose ps
```
3. Inspect logs for failing services:
```bash
docker-compose logs neo4j
docker-compose logs redis
```
4. Restart the stack:
```bash
make dev
```

## Vault Secret Integration

### Symptom
- Errors related to `MASTER_VAULT_KEY`
- API crashes during startup or secret access
- Integration tests involving Vault fail

### Cause
- Vault service is not running or unsealed
- Required Vault environment variables are missing
- Vault keys are not exported in the current shell

### Solution
1. Ensure the Vault container is running:
```bash
docker ps
```
2. Verify required environment variables are set:
```bash
echo $MASTER_VAULT_KEY_V1
```
3. If Vault was restarted, re-export keys and tokens before retrying.
4. Re-run the stack after fixing Vault configuration:
```bash
make dev
```

## Python / Poetry Environment Issues

### Symptom
- `pyproject.toml` installation failures
- Dependency conflicts across `api`, `core`, or `transforms`
- Poetry commands behave inconsistently

### Cause
- Poetry cache corruption
- Python version mismatch
- Manual setup instead of standardized Makefile workflow

### Solution
1. Prefer using the Makefile for setup:
```bash
make dev
```
2. Clear Poetry cache if installation fails:
```bash
poetry cache clear pypi --all
```
3. Ensure the correct Python version is active:
```bash
python --version
```
4. Retry installation after clearing cache.

## Common Port Conflicts

### Symptom
- `Address already in use`
- Services fail to bind to ports `3000`, `5001`, or `5432`

### Cause
- Another local service is already using the required port

### Solution
1. Identify the process using the port:
```bash
lsof -i :3000
```
2. Stop the conflicting process or free the port:
```bash
kill -9 <PID>
```
3. Restart the SpectraGraph stack:
```bash
make dev
```