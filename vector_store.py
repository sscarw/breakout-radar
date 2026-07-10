import os
from qdrant_client import QdrantClient, models
from qdrant_client.models import Distance, PointStruct
from dotenv import load_dotenv
from models import HNStory
from embeddings import get_embedding

load_dotenv()


def get_qdrant_client() -> QdrantClient:
    client = QdrantClient(url=os.getenv('QDRANT_URL'))
    return client


def ensure_collection(client: QdrantClient, collection_name: str) -> None:
    if not client.collection_exists(collection_name):
        client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(
                size=1536,
                distance=Distance.COSINE
            ),
        )


def save_discussion(client: QdrantClient, collection_name: str, story: HNStory) -> None:
    if not story.title:
        return
    vector = get_embedding(story.title)
    points = [
        PointStruct(
            id=int(story.object_id),
            vector=vector,
            payload={"title": story.title, "url": story.url, "points": story.points}
        )
    ]

    client.upsert(
        collection_name=collection_name,
        points=points,
    )


def search_discussions(client: QdrantClient, collection_name: str, query: str, limit: int = 5) -> list[dict]:
    query_vector = get_embedding(query)
    results = client.query_points(
        collection_name=collection_name,
        query=query_vector,
        limit=limit,
        with_payload=True
    )
    return [
        {
            "title": point.payload["title"],
            "url": point.payload["url"],
            "points": point.payload["points"],
            "score": point.score
        }
        for point in results.points
    ]
