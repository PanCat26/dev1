"""
Run the full indexing pipeline on a repository snapshot.

Usage:
    python scripts/run_indexing_demo.py <snapshot_path> [repo_id] [commit_sha]

Example:
    python scripts/run_indexing_demo.py ../../../some-repo my-repo abc1234
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from indexing.service import run_indexing


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/run_indexing_demo.py <snapshot_path> [repo_id] [commit_sha]")
        sys.exit(1)

    snapshot_path = sys.argv[1]
    repo_id = sys.argv[2] if len(sys.argv) > 2 else "demo-repo"
    commit_sha = sys.argv[3] if len(sys.argv) > 3 else "unknown"

    print(f"Indexing repo_id={repo_id}, commit_sha={commit_sha}")
    print(f"Snapshot path: {os.path.abspath(snapshot_path)}\n")

    result = run_indexing(repo_id, commit_sha, snapshot_path)

    print("\nIndexing Result\n")
    print(f"Files scanned: {result.files_scanned}")
    print(f"Chunks created: {result.chunks_created}")
    print(f"Chunks upserted: {result.chunks_upserted}")
    if result.errors:
        print(f"  Errors ({len(result.errors)}):")
        for err in result.errors:
            print(f" - {err}")
    else:
        print("  Errors: none")


if __name__ == "__main__":
    main()
