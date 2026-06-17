from models import Repository, RepoMetrics
import os
import httpx
from dotenv import load_dotenv

load_dotenv()


async def search_repositories(query: str, limit: int) -> list[Repository]:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.github.com/search/repositories",
            headers={
                "Authorization": f"Bearer {os.getenv('GITHUB_TOKEN')}",
                "X-GitHub-Api-Version": "2026-03-10",
                "Accept": "application/vnd.github+json",
            },

            params={
                "q": query,
                "sort": "stars",
                "order": "desc",
                "per_page": limit
            }
        )
    data = response.json()
    repos = [Repository.model_validate(item) for item in data["items"]]
    return repos


async def fetch_repo_metrics(full_name: str) -> RepoMetrics:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.github.com/repos/{full_name}",
            headers={
                "Authorization": f"Bearer {os.getenv('GITHUB_TOKEN')}",
                "X-GitHub-Api-Version": "2026-03-10",
                "Accept": "application/vnd.github+json",
            }
        )
        data = response.json()
        return RepoMetrics.model_validate(data)

