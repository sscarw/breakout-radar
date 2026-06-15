import os
import asyncio
from datetime import datetime
import httpx
from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()


class Repository(BaseModel):
    github_id: int = Field(..., alias='id')
    name: str = Field(..., alias='full_name')
    url: str = Field(..., alias='html_url')
    description: str | None = Field(None, alias='description')
    language: str | None = Field(None, alias='language')
    created_at: datetime = Field(..., alias='created_at')


class RepoMetrics(BaseModel):
    stars: int = Field(..., alias='stargazers_count')
    forks: int = Field(..., alias='forks_count')
    open_issues: int = Field(..., alias='open_issues_count')


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


async def main():
    metrics = await fetch_repo_metrics("crewAIInc/crewAI")
    print(metrics.stars, metrics.forks, metrics.open_issues)


if __name__ == "__main__":
    asyncio.run(main())
