import os
from dotenv import load_dotenv

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "repo_snapshots")
QDRANT_VECTOR_SIZE = int(os.getenv("QDRANT_VECTOR_SIZE", "384"))
QDRANT_DISTANCE_METRIC = os.getenv("QDRANT_DISTANCE_METRIC", "Cosine")

EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "all-MiniLM-L6-v2")
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://dev1:dev1@127.0.0.1:5433/dev1db")

SNAPSHOTS_DIR = os.getenv("SNAPSHOTS_DIR", os.path.join(os.path.dirname(__file__), "storage", "snapshots"))
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", None)
