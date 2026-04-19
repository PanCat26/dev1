import uuid
from typing import Any

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    FieldCondition,
    Filter,
    FilterSelector,
    MatchValue,
    PointStruct,
    VectorParams,
)
import config

from indexing.types import Chunk

DISTANCE_MAP = {
    "Cosine": Distance.COSINE,
    "Euclid": Distance.EUCLID,
    "Dot": Distance.DOT,
}


def ensure_collection_exists(client: QdrantClient) -> None:
    """Create the configured collection if it does not already exist."""
    collection_name = config.QDRANT_COLLECTION_NAME
    existing = [c.name for c in client.get_collections().collections]

    if collection_name in existing:
        print(f"Collection '{collection_name}' already exists, skipping creation.")
        return

    distance = DISTANCE_MAP.get(config.QDRANT_DISTANCE_METRIC, Distance.COSINE)

    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(
            size=config.QDRANT_VECTOR_SIZE,
            distance=distance,
        ),
    )
    print(f"Collection '{collection_name}' created (size={config.QDRANT_VECTOR_SIZE}, distance={config.QDRANT_DISTANCE_METRIC}).")


def upsert_chunks(
    client: QdrantClient,
    chunks: list[Chunk],
    vectors: list[list[float]],
    batch_size: int = 100,
) -> int:
    """Upsert chunks with their embedding vectors into Qdrant.

    Returns the number of points upserted.
    """
    collection_name = config.QDRANT_COLLECTION_NAME
    points = []

    for chunk, vector in zip(chunks, vectors):
        # Deterministic id so re-indexing the same chunk updates the point
        # instead of creating a duplicate.
        point_key = "|".join([
            chunk.repo_id,
            chunk.commit_sha,
            chunk.file_path,
            chunk.chunk_type,
            chunk.symbol_name,
            f"{chunk.start_line}-{chunk.end_line}",
        ])
        point_id = str(uuid.uuid5(uuid.NAMESPACE_URL, point_key))

        points.append(PointStruct(
            id=point_id,
            vector=vector,
            payload={
                "repo_id": chunk.repo_id,
                "commit_sha": chunk.commit_sha,
                "file_path": chunk.file_path,
                "chunk_type": chunk.chunk_type,
                "symbol_name": chunk.symbol_name,
                "start_line": chunk.start_line,
                "end_line": chunk.end_line,
                "text": chunk.text,
            },
        ))

    # Insert or update records in batches
    for i in range(0, len(points), batch_size):
        batch = points[i : i + batch_size]
        client.upsert(collection_name=collection_name, points=batch)

    return len(points)


def delete_chunks(client: QdrantClient, fields: dict[str, Any]) -> None:
    """Delete points from the configured collection whose payload matches all given fields.
    Intended primarily for deleting by `repo_id`, but works with any exact-match payload fields.
    """
    if not fields:
        raise ValueError("delete_chunks requires at least one field to match on.")

    conditions = [
        FieldCondition(key=key, match=MatchValue(value=value))
        for key, value in fields.items()
    ]

    client.delete(
        collection_name=config.QDRANT_COLLECTION_NAME,
        points_selector=FilterSelector(filter=Filter(must=conditions)),
    )
