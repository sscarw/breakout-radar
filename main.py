from agents import Runner
from db import save_scan_run, save_repository, save_metrics, get_metrics_history
from scoring import calculate_momentum_score
from github_client import search_repositories, fetch_repo_metrics
from hn_client import search_hackernews
from vector_store import get_qdrant_client, ensure_collection, save_discussion
from report_formatter import format_report
import pipeline
import asyncio
from dotenv import load_dotenv

load_dotenv()


async def main():
    query = input("Describe the projects you're looking for: ")
    plan = (await Runner.run(pipeline.query_planner_agent, query)).final_output
    scan_id = save_scan_run(query)
    client = get_qdrant_client()
    ensure_collection(client, "discussions")
    stories = await search_hackernews(plan.hn_query)
    for story in stories:
        save_discussion(client, "discussions", story)

    repos = await search_repositories(plan.github_query, limit=5)
    analyses = []
    for repo in repos:
        repo_db_id = save_repository(repo)
        metrics = await fetch_repo_metrics(repo.name)
        save_metrics(repo_db_id, scan_id, metrics)
        momentum = calculate_momentum_score(get_metrics_history(repo_db_id))
        prompt = f"""
        Repository: {repo.name}
        Repository ID: {repo_db_id}
        Precomputed momentum_score: {momentum}

        Analyze this repository.
        Use the provided momentum_score exactly.
        Do not estimate or invent momentum_score.
        """
        analysis = (await Runner.run(pipeline.analyst_agent, prompt)).final_output
        analyses.append(analysis)

    analyses_text = "\n\n".join(a.model_dump_json(indent=2) for a in analyses)
    report = (await Runner.run(pipeline.report_agent, analyses_text)).final_output
    print(report)


if __name__ == "__main__":
    asyncio.run(main())
