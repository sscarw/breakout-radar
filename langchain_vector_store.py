import asyncio
import os
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from hn_client import search_hackernews

load_dotenv()


async def build_documents(query: str) -> list[Document]:
    stories = await search_hackernews(query)
    documents = []
    for story in stories:
        if not story.title:
            continue
        documents.append(
            Document(
                page_content=story.title,
                metadata={"url": story.url, "points": story.points, "object_id": story.object_id},
            )
        )
    return documents


documents = asyncio.run(build_documents("AI agents"))

embeddings = OpenAIEmbeddings()

qdrant = QdrantVectorStore.from_documents(
    documents,
    embedding=embeddings,
    collection_name="discussions_lc",
    url=os.getenv('QDRANT_URL'),
)


def search_discussions_lc(query: str, limit: int = 5) -> list[dict]:
    results = qdrant.similarity_search_with_score(query, k=limit)

    return [
        {
            "title": doc.page_content,
            "url": doc.metadata["url"],
            "points": doc.metadata["points"],
            "score": score,
        }
        for doc, score in results
    ]
