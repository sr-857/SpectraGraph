import os

async def test_github_access():
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("Error: GITHUB_TOKEN environment variable not set")
        return
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json"
    }
    
    async with httpx.AsyncClient() as client:
        print("Testing rate limit...")
        # Test rate limit
        response = await client.get(
            "https://api.github.com/rate_limit",
            headers=headers
        )
        print(f"Status: {response.status_code}")
        print(response.json())
        
        print("\nTesting search...")
        # Test search
        response = await client.get(
            "https://api.github.com/search/users",
            params={"q": "anthropic.com", "type": "org"},
            headers=headers
        )
        print(f"Status: {response.status_code}")
        print(response.json())

if __name__ == "__main__":
    asyncio.run(test_github_access())
