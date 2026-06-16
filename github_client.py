import os
import asyncio
from datetime import datetime, date
import httpx
from dotenv import load_dotenv
from pydantic import BaseModel, Field
import psycopg

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


class HNStory(BaseModel):
    title: str | None = Field(None, alias='title')
    url: str | None = Field(None, alias='url')
    points: int = Field(..., alias='points')
    num_comments: int = Field(..., alias='num_comments')


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


def get_connection():
    conn = psycopg.connect(
        dbname=os.getenv('POSTGRES_DB'),
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD'),
        host=os.getenv('POSTGRES_HOST'),
        port=os.getenv('POSTGRES_PORT'),
    )
    return conn


def save_scan_run(query: str) -> int:
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            row = cur.execute("INSERT INTO scan_runs (query) VALUES (%s) RETURNING id",
                              (query,)).fetchone()
            conn.commit()
        return row[0]
    finally:
        conn.close()


def save_repository(repo: Repository) -> int:
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            row = cur.execute(
                "INSERT INTO repositories (github_id, name, url, description, language, created_at) VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (github_id) DO UPDATE SET name = EXCLUDED.name RETURNING id",
                (repo.github_id, repo.name, repo.url, repo.description, repo.language, repo.created_at,)).fetchone()
            conn.commit()
        return row[0]
    finally:
        conn.close()


def save_metrics(repository_id: int, scan_run_id: int, metrics: RepoMetrics) -> int:
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            row = cur.execute(
                "INSERT INTO repository_metrics (repository_id, scan_run_id, metric_date, stars, forks, open_issues) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id",
                (
                    repository_id, scan_run_id, date.today(), metrics.stars, metrics.forks,
                    metrics.open_issues)).fetchone()
            conn.commit()
        return row[0]
    finally:
        conn.close()


async def search_hackernews(query) -> list[HNStory]:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://hn.algolia.com/api/v1/search",
            params={
                "query": query,
            }
        )
        data = response.json()
        stories = [HNStory.model_validate(item) for item in data["hits"]]
        return stories


async def main():
    query = "ai agents for gym"
    scan_id = save_scan_run(query)
    repos = await search_repositories(query, limit=5)
    for repo in repos:
        repo_db_id = save_repository(repo)
        metrics = await fetch_repo_metrics(repo.name)
        save_metrics(repo_db_id, scan_id, metrics)
        print(repo_db_id)

    print(f"Saved {len(repos)} repos for scan run {scan_id}")

    stories = await search_hackernews("crewai")
    for story in stories:
        print(story.title, story.url, story.points)


if __name__ == "__main__":
    asyncio.run(main())
