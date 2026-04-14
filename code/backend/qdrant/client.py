from qdrant_client import QdrantClient
import config


def get_qdrant_client() -> QdrantClient:
    """Return a Qdrant client connected to the configured URL."""
    return QdrantClient(url=config.QDRANT_URL)
