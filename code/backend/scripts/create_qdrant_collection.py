"""
Script to create the Qdrant collection for the indexing service.
Run from code/backend/:  python scripts/create_qdrant_collection.py
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from qdrant.client import get_qdrant_client
from qdrant.collection import ensure_collection_exists


def main():
    client = get_qdrant_client()
    ensure_collection_exists(client)


if __name__ == "__main__":
    main()
