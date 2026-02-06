from __future__ import annotations
from enum import Enum
import uuid

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from fastembed import TextEmbedding

embedder = TextEmbedding(
    model_name="BAAI/bge-small-en-v1.5"
)
qdrant_client = QdrantClient(":memory:")


class DataType(Enum):
    AI = "AI"
    SYSTEM = "SYSTEM"


def create_and_update_memory(collection_name: str, update_data: list[str], data_type: DataType = DataType.SYSTEM):
    print("[SYSTEM]: create and update memory...\n")
    if not qdrant_client.collection_exists(collection_name):
        qdrant_client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE,
            ),
        )

    qdrant_client.upsert(
        collection_name=collection_name,
        points=[
            PointStruct(
                id=uuid.uuid5(
                    uuid.NAMESPACE_DNS,
                    data
                ).hex,
                vector=next(embedder.embed([data])),
                payload={"type": data_type, "text": data}
            ) for data in update_data if data != ""],
    )


def search_memery(search_info, collection_name: str = "ai-collection"):
    print("[SYSTEM]: Search memory...\n")
    if qdrant_client.collection_exists(collection_name):
        return qdrant_client.query_points(
            collection_name=collection_name,
            query=next(embedder.embed([f"query: {search_info}"])),
            with_payload=True,
            limit=3,
        ).points[::-1]
    else:
        return None
