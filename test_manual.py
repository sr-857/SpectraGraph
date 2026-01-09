"""Manual testing script for GitHub transform."""

import asyncio
import os
from spectragraph_transforms.social.github_repo import GitHubRepoTransform


async def test_github_transform():
    """Test the GitHub transform with real API calls."""
    
    transform = GitHubRepoTransform()
    # Manually inject params since we aren't using the full vault infra in this script
    # User's token from previous context
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("Error: GITHUB_TOKEN environment variable not set. Please run: export GITHUB_TOKEN='your_token'")
        return 
    transform.params = {"github_token": token}
    
    # Test 1: Basic scan
    print("=== Test 1: Basic Domain Scan ===")
    
    try:
        # Preprocess manually (usually done by orchestrator)
        input_data = ["anthropic.com"]
        validated_input = await transform.preprocess(input_data)
        print(f"✓ Preprocessing successful")
        
        # Override default params for this run if needed, but since scan takes Values, 
        # config is in transform.params. Let's set max_repos there.
        transform.params["max_repos"] = 5
        
        results = await transform.scan(validated_input)
        result = results[0]
        
        print(f"✓ Found {len(result['organizations'])} organizations")
        print(f"✓ Found {len(result['repositories'])} repositories")
        print(f"✓ Found {len(result['contributors'])} contributors")
        print(f"✓ Rate limit remaining: {result['metadata']['rate_limit']['remaining']}")
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
    
    # Test 2: With filters
    print("\n=== Test 2: Filtered Scan (OpenAI, Python, >100 stars) ===")
    
    try:
        transform.params["max_repos"] = 10
        transform.params["min_stars"] = 100
        transform.params["language_filter"] = "Python"
        
        input_data = ["openai.com"]
        validated_input = await transform.preprocess(input_data)
        results = await transform.scan(validated_input)
        result = results[0]
        
        repos = result['repositories']
        print(f"✓ Found {len(repos)} Python repos with 100+ stars")
        
        if repos:
            top_repo = max(repos, key=lambda r: r['stargazers_count'])
            print(f"✓ Top repo: {top_repo['full_name']} ({top_repo['stargazers_count']} stars)")
    except Exception as e:
        print(f"✗ Error: {e}")

    # Test 3: Include forks
    print("\n=== Test 3: Include Forks (github.com) ===")
    
    try:
        transform.params["include_forks"] = True
        transform.params["max_repos"] = 5
        # Reset other filters
        transform.params["min_stars"] = 0
        transform.params["language_filter"] = None
        
        input_data = ["github.com"]
        validated_input = await transform.preprocess(input_data)
        results = await transform.scan(validated_input)
        result = results[0]
        
        forks = [r for r in result['repositories'] if r['fork']]
        originals = [r for r in result['repositories'] if not r['fork']]
        
        print(f"✓ Total repos: {len(result['repositories'])}")
        print(f"✓ Forks: {len(forks)}")
        print(f"✓ Original: {len(originals)}")
    except Exception as e:
        print(f"✗ Error: {e}")


if __name__ == "__main__":
    asyncio.run(test_github_transform())
