from dataclasses import dataclass, field

from indexing.scanner import list_supported_files
from indexing.parser import parse_python_file
from indexing.chunking import chunks_from_symbols, chunks_from_markdown
from indexing.embeddings import embed_texts
from indexing.types import Chunk
from qdrant.client import get_qdrant_client
from qdrant.collection import ensure_collection_exists, upsert_chunks


@dataclass
class IndexingResult:
    files_scanned: int = 0
    chunks_created: int = 0
    chunks_upserted: int = 0
    errors: list[str] = field(default_factory=list)


def run_indexing(repo_id: str, commit_sha: str, snapshot_path: str) -> IndexingResult:
    """Run the full indexing pipeline on a repository snapshot.

    Scans files, parses Python, chunks code and docs,
    generates embeddings, and upserts into Qdrant.
    """
    result = IndexingResult()

    # 1. Scan files
    files = list_supported_files(snapshot_path)
    result.files_scanned = len(files)
    print(f"Scanned {len(files)} supported file(s) in {snapshot_path}")

    if not files:
        return result

    # 2. Parse and chunk
    all_chunks: list[Chunk] = []

    for file_path in files:
        try:
            if file_path.endswith(".py"):
                symbols = parse_python_file(file_path)
                all_chunks.extend(chunks_from_symbols(symbols, repo_id, commit_sha))

            elif file_path.endswith(".md"):
                with open(file_path, encoding="utf-8", errors="replace") as f:
                    text = f.read()
                all_chunks.extend(chunks_from_markdown(file_path, text, repo_id, commit_sha))

        except Exception as e:
            msg = f"Error processing {file_path}: {e}"
            print(f"  {msg}")
            result.errors.append(msg)

    result.chunks_created = len(all_chunks)
    print(f"Created {len(all_chunks)} chunk(s)")

    if not all_chunks:
        return result

    # 3. Generate embeddings
    print("Generating embeddings...")
    texts = [c.text for c in all_chunks]
    vectors = embed_texts(texts)
    print(f"Generated {len(vectors)} embedding(s)")

    # 4. Upsert into Qdrant
    print("Upserting into Qdrant...")
    client = get_qdrant_client()
    ensure_collection_exists(client)
    result.chunks_upserted = upsert_chunks(client, all_chunks, vectors)
    print(f"Upserted {result.chunks_upserted} chunk(s) into Qdrant")

    return result
