# spectragraph-transforms
The repository containing open-source transforms for spectragraph.

> ⚠️ 🚧 Work in progress !

## Available Transforms

### GitHub Repository Transform

Enriches domains with GitHub organization and repository intelligence.

**Category:** Social/Development Platform  
**Input:** Domain  
**Output:** Organizations, repositories, contributors, metrics

**Use Cases:**
- Security research and vulnerability discovery
- Threat intelligence mapping
- Corporate technology stack analysis
- Developer activity tracking

**Configuration:**
```python
params = {
    "domain": "example.com",
    "include_forks": False,
    "max_repos": 50,
    "min_stars": 0,
    "language_filter": "Python"
}
```

**Documentation:** [docs/transforms/github_repo.md](../docs/transforms/github_repo.md)
