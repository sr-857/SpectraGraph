"""Tests for GitHub repository transform."""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from datetime import datetime
import httpx

from spectragraph_transforms.social.github_repo import (
    GitHubRepoTransform,
    GitHubRepoParams
)
from spectragraph_core.exceptions import TransformError


@pytest.fixture
def transform():
    """Create transform instance."""
    t = GitHubRepoTransform()
    # Mock params to simulate async_init resolution
    t.params = {"github_token": "ghp_fake_token"} 
    return t


@pytest.fixture
def sample_params():
    """Sample valid parameters."""
    return {
        "domain": "anthropic.com",
        "include_forks": False,
        "max_repos": 10,
        "min_stars": 0,
        "language_filter": None
    }


@pytest.fixture
def mock_org_response():
    """Mock GitHub organization API response."""
    return {
        "login": "anthropics",
        "name": "Anthropic",
        "description": "AI safety company",
        "blog": "anthropic.com",
        "location": "San Francisco",
        "email": "hello@anthropic.com",
        "twitter_username": "AnthropicAI",
        "public_repos": 42,
        "public_gists": 0,
        "followers": 1250,
        "following": 0,
        "created_at": "2021-01-15T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z",
        "html_url": "https://github.com/anthropics",
        "type": "Organization"
    }


@pytest.fixture
def mock_repo_response():
    """Mock GitHub repository API response."""
    return {
        "name": "claude-api",
        "full_name": "anthropics/claude-api",
        "description": "Python client for Claude API",
        "html_url": "https://github.com/anthropics/claude-api",
        "homepage": "https://anthropic.com",
        "language": "Python",
        "stargazers_count": 3400,
        "forks_count": 280,
        "open_issues_count": 15,
        "watchers_count": 3400,
        "size": 1024,
        "default_branch": "main",
        "topics": ["ai", "llm", "api"],
        "created_at": "2023-03-15T00:00:00Z",
        "updated_at": "2024-01-05T00:00:00Z",
        "pushed_at": "2024-01-05T00:00:00Z",
        "fork": False,
        "archived": False,
        "disabled": False,
        "has_issues": True,
        "has_projects": True,
        "has_downloads": True,
        "has_wiki": True,
        "has_pages": False,
        "has_discussions": True,
        "license": {"name": "MIT"},
        "visibility": "public"
    }


class TestParams:
    """Test parameter validation."""
    
    def test_valid_params(self):
        """Test valid parameter combinations."""
        # Note: We are testing the Pydantic model directly here
        params = GitHubRepoParams(
            domain="example.com",
            max_repos=25,
            min_stars=10,
            include_forks=True
        )
        assert params.domain == "example.com"
        assert params.max_repos == 25
        assert params.min_stars == 10
        assert params.include_forks is True
    
    def test_defaults(self):
        """Test default parameter values."""
        params = GitHubRepoParams(domain="test.com")
        assert params.include_forks is False
        assert params.max_repos == 50
        assert params.min_stars == 0
        assert params.language_filter is None
    
    def test_max_repos_validation(self):
        """Test max_repos boundary validation."""
        # Too high
        with pytest.raises(ValueError):
            GitHubRepoParams(domain="test.com", max_repos=150)
        
        # Too low
        with pytest.raises(ValueError):
            GitHubRepoParams(domain="test.com", max_repos=0)
        
        # Valid boundaries
        params = GitHubRepoParams(domain="test.com", max_repos=1)
        assert params.max_repos == 1
        
        params = GitHubRepoParams(domain="test.com", max_repos=100)
        assert params.max_repos == 100
    
    def test_min_stars_validation(self):
        """Test min_stars cannot be negative."""
        with pytest.raises(ValueError):
            GitHubRepoParams(domain="test.com", min_stars=-5)
        
        params = GitHubRepoParams(domain="test.com", min_stars=0)
        assert params.min_stars == 0


class TestPreprocess:
    """Test preprocessing logic."""
    
    @pytest.mark.asyncio
    async def test_success(self, transform):
        """Test successful preprocessing."""
        # Preprocess converts input list to cleaned list of domains
        input_data = ["anthropic.com", {"domain": "example.com"}]
        result = await transform.preprocess(input_data)
        
        assert len(result) == 2
        assert "anthropic.com" in result
        assert "example.com" in result
        
        # Check token usage in headers
        assert "Authorization" in transform.headers
        assert "Bearer ghp_fake_token" in transform.headers["Authorization"]


class TestSearch:
    """Test organization search."""
    
    @pytest.mark.asyncio
    async def test_search_organizations(self, transform, mock_org_response):
        """Test successful organization search."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "items": [{"login": "anthropics", "type": "Organization"}]
        }
        mock_response.raise_for_status = MagicMock()
        
        mock_client = AsyncMock()
        mock_client.get.return_value = mock_response
        
        with patch.object(transform, '_get_organization', return_value=mock_org_response):
            orgs = await transform._search_organizations(mock_client, "anthropic.com")
            
            assert len(orgs) >= 1
            assert orgs[0]["login"] == "anthropics"
            assert orgs[0]["name"] == "Anthropic"
    
    @pytest.mark.asyncio
    async def test_search_no_results(self, transform):
        """Test search with no results."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"items": []}
        mock_response.raise_for_status = MagicMock()
        
        mock_client = AsyncMock()
        mock_client.get.return_value = mock_response
        
        orgs = await transform._search_organizations(mock_client, "nonexistent.com")
        assert len(orgs) == 0


class TestRepositories:
    """Test repository retrieval."""
    
    @pytest.mark.asyncio
    async def test_get_repositories(self, transform, mock_repo_response):
        """Test successful repository retrieval."""
        mock_response = MagicMock()
        mock_response.json.return_value = [mock_repo_response]
        mock_response.raise_for_status = MagicMock()
        
        mock_client = AsyncMock()
        mock_client.get.return_value = mock_response
        
        repos = await transform._get_org_repositories(
            mock_client,
            "anthropics",
            max_repos=10,
            include_forks=False,
            min_stars=0,
            language_filter=None
        )
        
        assert len(repos) == 1
        assert repos[0]["name"] == "claude-api"
        assert repos[0]["stargazers_count"] == 3400
        assert repos[0]["language"] == "Python"


class TestFullScan:
    """Test complete scan workflow."""
    
    @pytest.mark.asyncio
    async def test_successful_scan(self, transform, mock_org_response, mock_repo_response):
        """Test complete scan execution."""
        
        with patch('httpx.AsyncClient') as mock_client_class:
            mock_client = AsyncMock()
            mock_client_class.return_value.__aenter__.return_value = mock_client
            
            with patch.object(transform, '_search_organizations', return_value=[mock_org_response]), \
                 patch.object(transform, '_get_org_repositories', return_value=[mock_repo_response]), \
                 patch.object(transform, '_get_contributors', return_value=[{"login": "dev1", "contributions": 100}]), \
                 patch.object(transform, '_get_rate_limit', return_value={"remaining": 4999}):
                
                result = await transform.scan(["anthropic.com"])
                
                assert len(result) == 1
                assert result[0]["domain"] == "anthropic.com"
                assert "timestamp" in result[0]
                assert len(result[0]["organizations"]) == 1
                assert len(result[0]["repositories"]) == 1
                assert "metadata" in result[0]
                assert result[0]["metadata"]["transform"] == "github_repo"
