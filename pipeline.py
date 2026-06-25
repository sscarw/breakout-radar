from agents import Agent

from agent_tools import fetch_repo_metrics_tool, search_discussions_tool
from models import SearchPlan, ProjectAnalysis

query_planner_agent = Agent(
    name="Query Planner",
    instructions="""Role: Convert a user's request into an optimized search plan.
        
        Your task is to generate:
        1. A GitHub search query using GitHub search qualifiers.
        2. A Hacker News search phrase.
        3. A short explanation of why these queries were chosen.
        
        Focus on discovering small, fast-growing open-source projects rather than already popular repositories.
        
        Prefer GitHub qualifiers such as:
        - stars:100..2000
        - language:<language if specified>
        - created:>2024-01-01 (or another recent date)
        - topic:<topic when appropriate>
        
        Avoid repositories with extremely high star counts unless the user explicitly requests them.""",
    output_type=SearchPlan
)

analyst_agent = Agent(
    name="Analyst",
    instructions="""Role: Analyze an open-source repository and determine whether it shows strong breakout potential.
        
        Your responsibilities:
        
        1. Fetch the current repository metrics using the repository metrics tool.
        2. Retrieve the most relevant developer discussions using the semantic discussion search tool.
        3. Analyze the repository momentum score together with GitHub metrics.
        4. Evaluate the overall community sentiment from the retrieved discussions.
        5. Determine the project's growth status based on available evidence.
        6. Explain which signals indicate future growth or decline.
        7. Produce a structured ProjectAnalysis output.
        
        Guidelines:
        
        - Base every conclusion on available metrics and retrieved discussions.
        - Do not invent information that was not provided by the tools.
        - Consider repository activity, community discussions, and momentum score together.
        - A high momentum score alone is not sufficient if community sentiment is strongly negative.
        - A positive sentiment alone is not sufficient if repository activity is declining.
        - Explain the reasoning behind the verdict using concise growth signals.
        - Focus on identifying promising early-stage open-source projects rather than already mature projects.""",
    tools=[
        fetch_repo_metrics_tool, search_discussions_tool
    ],
    output_type=ProjectAnalysis
)
