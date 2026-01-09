# GitHub Repository Transform

Enriches domains with GitHub organization and repository intelligence.

## Overview

The `github_repo` transform discovers GitHub organizations associated with a target domain and retrieves detailed information about their repositories and contributors. This transform is essential for understanding the open-source footprint and development activity of an organization.

**Category**: `social`
**Input**: Domain string
**Output**: List of objects containing organization, repository, and contributor data.

## Capabilities

- **Organization Discovery**: Searches for organizations using domain, email, and name matching.
- **Repository Metadata**: Retrieves details like stars, forks, language, and activity for each repository.
- **Contributor Analysis**: Identifies top contributors for the most popular repositories.
- **Filtering**: Supports filtering repositories by star count, language, and fork status.

## Configuration Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `domain` | string | (Input) | The target domain to investigate. |
| `include_forks` | boolean | `False` | Whether to include forked repositories in the results. |
| `max_repos` | integer | `50` | Maximum number of repositories to return per organization. |
| `min_stars` | integer | `0` | Minimum number of stars a repository must have to be included. |
| `language_filter` | string | `None` | Filter repositories by programming language (e.g., "Python"). |
| `github_token` | vaultSecret | (Required) | GitHub Personal Access Token (`public_repo` scope). |

## Usage Example

```python
from spectragraph_transforms import GitHubRepoTransform

transform = GitHubRepoTransform()

# Configure parameters (token should be in vault)
transform.params = {
    "max_repos": 10,
    "min_stars": 50,
    "language_filter": "Python"
}

# Run scan
results = await transform.scan(["anthropic.com"])
```

## Setup

1. Generate a GitHub Personal Access Token (Classic) with `public_repo` scope.
2. Add the token to your SpectraGraph vault:
   ```bash
   spectragraph vault set github_token ghp_YOUR_TOKEN
   ```
3. Or ensure `GITHUB_TOKEN` is available if running manually.

## Output Structure

The transform returns a list of result objects, each containing:
- `domain`: Input domain
- `organizations`: List of matching GitHub organizations
- `repositories`: List of repositories meeting criteria
- `contributors`: List of top contributors
- `metadata`: Execution metadata (rate limits, etc.)
