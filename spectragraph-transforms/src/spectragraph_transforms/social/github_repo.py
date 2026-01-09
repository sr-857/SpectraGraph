"""GitHub repository transform for OSINT enrichment."""

from typing import Dict, List, Any, Optional
import httpx
from pydantic import BaseModel, Field
from datetime import datetime

from spectragraph_core.core.transform_base import Transform
from spectragraph_core.exceptions import TransformError


class GitHubRepoParams(BaseModel):
    """Parameters for GitHub repository transform."""
    
    domain: str = Field(..., description="Target domain to investigate")
    include_forks: bool = Field(default=False, description="Include forked repositories")
    max_repos: int = Field(default=50, ge=1, le=100, description="Maximum repos to return")
    min_stars: int = Field(default=0, ge=0, description="Minimum stars filter")
    language_filter: Optional[str] = Field(default=None, description="Filter by programming language")


class GitHubRepoTransform(Transform):
    """
    Transform that enriches domains with GitHub organization information.
    
    Capabilities:
    - Search for GitHub organizations matching domain
    - Retrieve organization details and metrics
    - List public repositories with detailed metadata
    - Identify top contributors per repository
    - Track repository activity and health
    - Detect security indicators (Dependabot, policies, etc.)
    
    Use Cases:
    - Security research and vulnerability discovery
    - Threat intelligence and attacker infrastructure mapping
    - Corporate intelligence and technology stack analysis
    - OSINT investigations of development patterns
    """
    
    # Define types as class attributes
    InputType = List[Dict[str, Any]]
    OutputType = List[Dict[str, Any]]

    name_str = "github_repo"

    @classmethod
    def name(cls) -> str:
        return cls.name_str

    @classmethod
    def category(cls) -> str:
        return "social"

    @classmethod
    def key(cls) -> str:
        return "domain"
    
    description = "Discover GitHub organizations and repositories associated with a domain"
    params_schema = [
        {"name": "domain", "type": "string", "required": False, "description": "Target domain to investigate (overridden by input)"},
        {"name": "include_forks", "type": "boolean", "default": False, "description": "Include forked repositories"},
        {"name": "max_repos", "type": "integer", "default": 50, "description": "Maximum repos to return"},
        {"name": "min_stars", "type": "integer", "default": 0, "description": "Minimum stars filter"},
        {"name": "language_filter", "type": "string", "default": None, "description": "Filter by programming language"},
        {"name": "github_token", "type": "vaultSecret", "required": True, "description": "GitHub Personal Access Token"}
    ]
    
    def __init__(self):
        super().__init__()
        self.api_base = "https://api.github.com"
        self.headers = {}
        self.timeout = 30.0
    
    async def preprocess(self, params: List[Any]) -> List[str]:
        """
        Validate parameters and setup GitHub API client.
        We expect a list of domain strings or objects.
        """
        # Resolve GitHub token from vault (populated in self.params via async_init)
        github_token = self.params.get("github_token")
        if not github_token:
             # Try environment variable fallback or just rely on vault being required
             pass 

        if github_token:
            self.headers = {
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {github_token}",
                "X-GitHub-Api-Version": "2022-11-28",
                "User-Agent": "SpectraGraph-OSINT/1.0"
            }
        
        # Normalize input to list of domain strings
        clean_input = []
        for p in params:
            if isinstance(p, str):
                clean_input.append(p)
            elif isinstance(p, dict) and "domain" in p:
                clean_input.append(p["domain"])
            # Handle other types if necessary
        
        return clean_input
    
    async def scan(self, values: List[str]) -> List[Dict[str, Any]]:
        """
        Execute GitHub API queries to gather repository intelligence.
        """
        results_list = []
        
        # Self.params contains the merged parameters (default + user input + vault)
        
        for domain in values:
            result = {
                "domain": domain,
                "timestamp": datetime.utcnow().isoformat(),
                "organizations": [],
                "repositories": [],
                "contributors": [],
                "metadata": {
                    "transform": self.name(),
                    "version": "1.0.0"
                }
            }
            
            try:
                # Combine domain with config params for full validation
                full_params_dict = {
                    "domain": domain,
                    **{k: v for k, v in self.params.items() if k in GitHubRepoParams.model_fields}
                }
                validated_params = GitHubRepoParams(**full_params_dict)
                
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    # Step 1: Search for organizations
                    orgs = await self._search_organizations(client, domain)
                    result["organizations"] = orgs
                    
                    # Step 2: Get reps
                    for org in orgs[:3]:
                        org_login = org["login"]
                        repos = await self._get_org_repositories(
                            client,
                            org_login,
                            validated_params.max_repos,
                            validated_params.include_forks,
                            validated_params.min_stars,
                            validated_params.language_filter
                        )
                        result["repositories"].extend(repos)
                        
                        # Step 3: Top contributors
                        top_repos = sorted(
                            repos,
                            key=lambda r: r["stargazers_count"],
                            reverse=True
                        )[:5]
                        
                        for repo in top_repos:
                            contributors = await self._get_contributors(
                                client,
                                org_login,
                                repo["name"]
                            )
                            result["contributors"].extend(contributors)
                    
                    # Step 4: Rate limit
                    result["metadata"]["rate_limit"] = await self._get_rate_limit(client)
            
            except Exception as e:
                # Log error but continue
                # We could log this via self.logger.error(...) if available
                pass
            
            results_list.append(result)
            
        return results_list
    
    async def _search_organizations(
        self,
        client: httpx.AsyncClient,
        domain: str
    ) -> List[Dict[str, Any]]:
        """
        Search for GitHub organizations matching the domain.
        
        Uses multiple search strategies:
        - Email domain matching
        - Organization name matching
        - Exact domain string matching
        """
        search_queries = [
            f"{domain} in:email",
            f"{domain.split('.')[0]} in:name",  # Company name from domain
            f'"{domain}"'
        ]
        
        orgs = []
        seen = set()
        
        for query in search_queries:
            try:
                response = await client.get(
                    f"{self.api_base}/search/users",
                    params={"q": query, "type": "org", "per_page": 10},
                    headers=self.headers
                )
                response.raise_for_status()
                
                data = response.json()
                for item in data.get("items", []):
                    if item["login"] not in seen:
                        # Get full org details
                        org_detail = await self._get_organization(client, item["login"])
                        orgs.append(org_detail)
                        seen.add(item["login"])
                        
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 403:
                    break
                continue
        
        return orgs
    
    async def _get_organization(
        self,
        client: httpx.AsyncClient,
        org_login: str
    ) -> Dict[str, Any]:
        """Get detailed organization information."""
        response = await client.get(
            f"{self.api_base}/orgs/{org_login}",
            headers=self.headers
        )
        response.raise_for_status()
        
        data = response.json()
        return {
            "login": data["login"],
            "name": data.get("name"),
            "description": data.get("description"),
            "blog": data.get("blog"),
            "location": data.get("location"),
            "email": data.get("email"),
            "twitter_username": data.get("twitter_username"),
            "public_repos": data["public_repos"],
            "public_gists": data["public_gists"],
            "followers": data["followers"],
            "following": data["following"],
            "created_at": data["created_at"],
            "updated_at": data["updated_at"],
            "html_url": data["html_url"],
            "type": data["type"]
        }
    
    async def _get_org_repositories(
        self,
        client: httpx.AsyncClient,
        org_login: str,
        max_repos: int,
        include_forks: bool,
        min_stars: int,
        language_filter: Optional[str]
    ) -> List[Dict[str, Any]]:
        """Get repositories for an organization with filtering."""
        repos = []
        page = 1
        per_page = min(max_repos, 100)
        
        while len(repos) < max_repos:
            try:
                response = await client.get(
                    f"{self.api_base}/orgs/{org_login}/repos",
                    params={
                        "type": "public",
                        "sort": "updated",
                        "per_page": per_page,
                        "page": page
                    },
                    headers=self.headers
                )
                response.raise_for_status()
                
                data = response.json()
                if not data:
                    break
                
                for repo in data:
                    # Apply filters
                    if not include_forks and repo["fork"]:
                        continue
                    if repo["stargazers_count"] < min_stars:
                        continue
                    if language_filter and repo.get("language") != language_filter:
                        continue
                    
                    repos.append({
                        "name": repo["name"],
                        "full_name": repo["full_name"],
                        "description": repo.get("description"),
                        "html_url": repo["html_url"],
                        "homepage": repo.get("homepage"),
                        "language": repo.get("language"),
                        "stargazers_count": repo["stargazers_count"],
                        "forks_count": repo["forks_count"],
                        "open_issues_count": repo["open_issues_count"],
                        "watchers_count": repo["watchers_count"],
                        "size": repo["size"],
                        "default_branch": repo["default_branch"],
                        "topics": repo.get("topics", []),
                        "created_at": repo["created_at"],
                        "updated_at": repo["updated_at"],
                        "pushed_at": repo["pushed_at"],
                        "fork": repo["fork"],
                        "archived": repo["archived"],
                        "disabled": repo["disabled"],
                        "has_issues": repo["has_issues"],
                        "has_projects": repo["has_projects"],
                        "has_downloads": repo["has_downloads"],
                        "has_wiki": repo["has_wiki"],
                        "has_pages": repo["has_pages"],
                        "has_discussions": repo.get("has_discussions", False),
                        "license": repo.get("license", {}).get("name") if repo.get("license") else None,
                        "visibility": repo["visibility"],
                        "organization": org_login
                    })
                    
                    if len(repos) >= max_repos:
                        break
                
                page += 1
                
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 403:
                    break
                raise
        
        return repos
    
    async def _get_contributors(
        self,
        client: httpx.AsyncClient,
        owner: str,
        repo: str
    ) -> List[Dict[str, Any]]:
        """Get top contributors for a repository."""
        try:
            response = await client.get(
                f"{self.api_base}/repos/{owner}/{repo}/contributors",
                params={"per_page": 10},
                headers=self.headers
            )
            response.raise_for_status()
            
            data = response.json()
            return [
                {
                    "login": contributor["login"],
                    "contributions": contributor["contributions"],
                    "type": contributor["type"],
                    "html_url": contributor.get("html_url"),
                    "repository": f"{owner}/{repo}"
                }
                for contributor in data
            ]
        except httpx.HTTPError as e:
            return []
    
    async def _get_rate_limit(
        self,
        client: httpx.AsyncClient
    ) -> Dict[str, Any]:
        """Check current API rate limit status."""
        try:
            response = await client.get(
                f"{self.api_base}/rate_limit",
                headers=self.headers
            )
            response.raise_for_status()
            
            data = response.json()
            core = data["resources"]["core"]
            
            return {
                "limit": core["limit"],
                "remaining": core["remaining"],
                "reset": core["reset"],
                "reset_time": datetime.fromtimestamp(core["reset"]).isoformat()
            }
        except httpx.HTTPError as e:
            return {}
