from agents import function_tool
from github_client import fetch_repo_metrics
from vector_store import get_qdrant_client, search_discussions
from models import RepoMetrics


@function_tool
async def fetch_repo_metrics_tool(full_name: str) -> RepoMetrics:
    """Use this to fetch stars, forks and open issues for a GitHub repository by full name."""
    return await fetch_repo_metrics(full_name)


@function_tool
def search_discussions_tool(query: str, limit: int = 5) -> list[dict]:
    """Use this to search relevant developer discussions from Qdrant by semantic similarity."""
    client = get_qdrant_client()
    collection_name = "discussions"
    return search_discussions(client, collection_name, query, limit)
