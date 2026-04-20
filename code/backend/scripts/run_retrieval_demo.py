"""
Usage:
    python scripts/run_retrieval_demo.py <repo_id> <commit_sha> <query>
    
Example:
    python scripts/run_retrieval_demo.py my-repo abc1234 "where is embed_query defined"
    python scripts/run_retrieval_demo.py test-repo main "find the parser function"
"""

from pathlib import Path
import sys

# Add project root to path for imports
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from retrieval import retrieve_for_query


def main(repo_id: str, commit_sha: str, query: str):
    
    print(f"Repository: {repo_id}")
    print(f"Commit: {commit_sha}")
    print(f"Query: {query}")
    print()
    
    try:
        evidence = retrieve_for_query(
            query=query,
            repo_id=repo_id,
            commit_sha=commit_sha,
            num_candidates=20,
            max_chunks_in_package=5,
        )
        
        print(f"Total chunks found: {evidence.total_chunks}")
        print(f"Groups: {len(evidence.groups)}")
        print()
        
        for group in evidence.groups:
            print(f"{group.role}: {group.description}")
            for chunk in group.chunks:
                print(
                    f"- {chunk.file_path}:{chunk.start_line}-{chunk.end_line} "
                    f"{chunk.symbol_name} "
                    f"(vector={chunk.vector_score:.3f}, final={chunk.final_score:.3f})"
                )
            print()
        
        print("Retrieval completed successfully!")
    
    except Exception as e:
        print(f"Error during retrieval: {e}")
        raise


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python scripts/run_retrieval_demo.py <repo_id> <commit_sha> <query>")
        print()
        print("Example:")
        print('  python scripts/run_retrieval_demo.py my-repo abc1234 "where is embed_query defined"')
        sys.exit(1)
    
    repo_id = sys.argv[1]
    commit_sha = sys.argv[2]
    query = sys.argv[3]
    
    main(repo_id, commit_sha, query)
