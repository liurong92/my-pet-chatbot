from __future__ import annotations
from enum import Enum
import uuid

from pathlib import Path
from pypdf import PdfReader
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
    print("[SYSTEM]: create and update memory...")
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

    # all = qdrant_client.get_collections().collections
    # for item in all:
    #     print("--------------------")
    #     print(qdrant_client.scroll(collection_name=item.name))
    #     print(item, '==============')


def search_memery(search_info, collection_name: str = "ai-collection"):
    print(f"[SYSTEM]: Search memory from {collection_name}...")
    if qdrant_client.collection_exists(collection_name):
        return qdrant_client.query_points(
            collection_name=collection_name,
            query=next(embedder.embed([f"query: {search_info}"])),
            with_payload=True,
            limit=3,
        ).points[::-1]
    else:
        return None


def load_pet_data():
    print("[SYSTEM]: Load resource data...")
    directory_paths = Path('./resource/')

    for file_path in directory_paths.iterdir():
        if file_path.is_file():
            suffix = Path(file_path).suffix

            data = ""
            if suffix.lower() == '.txt':
                with open(file_path, "r") as file:
                    data = [message.replace("\n", '').strip() for message in file.readlines()]

            # if suffix.lower() == '.pdf':
            #     with open(file_path, "rb") as file:
            #         reader = PdfReader(file)
            #         data = [page.extract_text() for page in reader.pages]

            create_and_update_memory(
                collection_name="system-resource",
                update_data=data,
                data_type=DataType.SYSTEM
            )
