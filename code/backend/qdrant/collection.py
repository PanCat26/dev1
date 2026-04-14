from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
import config

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
