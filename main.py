from db import save_scan_run, save_repository, save_metrics
from github_client import search_repositories, fetch_repo_metrics
from hn_client import search_hackernews
from vector_store import get_qdrant_client, ensure_collection, save_discussion, search_discussions
import asyncio
from dotenv import load_dotenv

load_dotenv()


async def main():
    query = "ai skills for it"
    scan_id = save_scan_run(query)
    repos = await search_repositories(query, limit=5)
    for repo in repos:
        repo_db_id = save_repository(repo)
        metrics = await fetch_repo_metrics(repo.name)
        save_metrics(repo_db_id, scan_id, metrics)
        print(repo_db_id)

    print(f"Saved {len(repos)} repos for scan run {scan_id}")

    client = get_qdrant_client()
    ensure_collection(client, "discussions")
    stories = await search_hackernews("ai agent framework")
    for story in stories:
        save_discussion(client, "discussions", story)
    print(f"Indexed {len(stories)} discussions")

    results = search_discussions(client, "discussions", "tools for building autonomous AI agents", limit=5)
    for r in results:
        print(f"{r['score']:.3f}  {r['title']}")


if __name__ == "__main__":
    asyncio.run(main())
