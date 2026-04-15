import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from database.session import SessionLocal
from services.repository_manager import RepositoryManager
import time


def main():
    if len(sys.argv) < 3:
        print("Usage: python scripts/run_repository_demo.py <source_path> <repo_name> [commit_sha]")
        print("Example: python scripts/run_repository_demo.py ../../../some-repo my-repo abc1234")
        sys.exit(1)

    source_path = sys.argv[1]
    repo_name = sys.argv[2]
    commit_sha = sys.argv[3] if len(sys.argv) > 3 else "unknown"

    print(f"Adding local repository: {repo_name} from {os.path.abspath(source_path)}")

    # Initialize a local DB session
    db = SessionLocal()
    try:
        repo = RepositoryManager.add_local_repository(
            db_session=db,
            name=repo_name,
            source_path=source_path,
            commit_sha=commit_sha
        )
        print(f"\nSuccessfully stored repository snapshot and triggered indexing!")
        print(f"Repo ID: {repo.id}")
        print(f"Status: {repo.status}")
        print(f"Snapshot Location: {repo.snapshot_path}")

        print("\nWaiting for background indexing to complete (so we can print final status)...")
        # Polling DB to see when status changes from 'indexing'
        while True:
            db.refresh(repo)
            if repo.status != "indexing":
                print(f"Indexing finished. Final status: {repo.status}")
                break
            time.sleep(2)
            print(".", end="", flush=True)

    except Exception as e:
        print(f"Failed to add repository: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    main()
