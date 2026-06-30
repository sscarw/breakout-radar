import asyncio
from agents import Runner
from db import get_metrics_history
from pipeline import analyst_agent
from scoring import calculate_momentum_score


REPOSITORY_ID = 1
REPOSITORY_FULL_NAME = "iOfficeAI/AionUi"


async def main() -> None:
    history = get_metrics_history(REPOSITORY_ID)
    momentum = calculate_momentum_score(history)

    print(f"Precomputed momentum: {momentum}")

    prompt = f"""
Analyze this specific repository.

Repository full name: {REPOSITORY_FULL_NAME}
Repository database id: {REPOSITORY_ID}
Precomputed momentum_score: {momentum}

Use the provided momentum_score value exactly.
Do not compute, estimate, or invent momentum_score.

Call the repository metrics tool for this repository.
Call the semantic discussion search tool for relevant developer discussions.
Return ProjectAnalysis.
"""

    result = await Runner.run(analyst_agent, prompt)

    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())