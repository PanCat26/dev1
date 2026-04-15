import threading

from sentence_transformers import SentenceTransformer
import config

_model: SentenceTransformer | None = None
_model_lock = threading.Lock()


def _get_model() -> SentenceTransformer:
    """Load the embedding model"""
    global _model
    if _model is None:
        with _model_lock:
            if _model is None:
                _model = SentenceTransformer(config.EMBEDDING_MODEL_NAME)
    return _model


def embed_text(text: str) -> list[float]:
    """Return the embedding vector for a single text string."""
    model = _get_model()
    return model.encode(text).tolist()


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Return embedding vectors for a batch of text strings."""
    model = _get_model()
    return model.encode(texts).tolist()
