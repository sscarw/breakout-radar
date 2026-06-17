from db import save_scan_run, save_repository, save_metrics
from github_client import search_repositories, fetch_repo_metrics
from hn_client import search_hackernews
import asyncio
from dotenv import load_dotenv

load_dotenv()


async def main():
    query = "ai agents for games"
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
