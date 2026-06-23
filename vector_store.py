import os
from qdrant_client import QdrantClient, models
from qdrant_client.models import Distance
from dotenv import load_dotenv

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
