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
qdrant_client = QdrantClient(url="http://localhost:6333")


class DataType(Enum):
    AI = "AI"
    SYSTEM = "SYSTEM"


def create_and_update_memory(collection_name: str, update_data: list[str], data_type: DataType = DataType.SYSTEM):
    print("[SYSTEM]: create and update memory...")
    if update_data is None:
        print("[SYSTEM]: No update_data provided (None). Skipping upsert.")
        return
    if isinstance(update_data, str):
        update_data = [update_data]

    valid_data = [data for data in update_data if isinstance(data, str) and data.strip() != ""]
    if not valid_data:
        print("[SYSTEM]: No non-empty items to upsert. Skipping upsert.")
        return

    if not qdrant_client.collection_exists(collection_name):
        qdrant_client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE,
            ),
        )

    points = []
    for data in valid_data:
        try:
            vector = next(embedder.embed([data]))
        except Exception as e:
            print(f"[SYSTEM]: embedder failed for data (skipping): {e}")
            continue

        points.append(
            PointStruct(
                id=uuid.uuid5(uuid.NAMESPACE_DNS, data).hex,
                vector=vector,
                payload={"type": data_type, "text": data},
            )
        )

    if not points:
        print("[SYSTEM]: No points were created after embedding. Skipping qdrant upsert.")
        return

    print(f"[SYSTEM]: Upserting {len(points)} points to collection '{collection_name}'")
    qdrant_client.upsert(
        collection_name=collection_name,
        points=points,
    )


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

            data = []
            if suffix.lower() == '.txt':
                print(f"[SYSTEM]: Loading TXT file: {file_path.name}")
                with open(file_path, "r") as file:
                    data = [message.replace("\n", '').strip() for message in file.readlines()]

            elif suffix.lower() == '.pdf':
                print(f"[SYSTEM]: Loading PDF file: {file_path.name}")
                with open(file_path, "rb") as file:
                    reader = PdfReader(file)
                    data = [page.extract_text() for page in reader.pages]

            if data:
                create_and_update_memory(
                    collection_name="system-resource",
                    update_data=data,
                    data_type=DataType.SYSTEM
                )
                print(f"[SYSTEM]: Successfully loaded {len(data)} items from {file_path.name}")
