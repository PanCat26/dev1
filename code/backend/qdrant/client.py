import threading

from qdrant_client import QdrantClient
import config

_client: QdrantClient | None = None
_client_lock = threading.Lock()


def get_qdrant_client() -> QdrantClient:
    """Return a Qdrant client connected to the configured URL."""
    global _client
    if _client is None:
        with _client_lock:
            if _client is None:
                _client = QdrantClient(url=config.QDRANT_URL)
    return _client
