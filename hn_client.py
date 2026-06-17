import httpx
from models import HNStory


async def search_hackernews(query: str) -> list[HNStory]:
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
