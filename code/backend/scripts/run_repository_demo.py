import sys
import os
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from repository_management.session import get_db
from repository_management.repository_manager import add_repository
from repository_management.repository import get_repository

def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/run_repository_demo.py <github_url>")
        print("Example: python scripts/run_repository_demo.py https://github.com/fastapi/fastapi")
        sys.exit(1)

    github_url = sys.argv[1]
    
    print(f"Adding repository from GitHub: {github_url}")

    db = next(get_db())
    try:
        repo_id, default_branch, commit_sha, name = add_repository(
            db_session=db,
            github_link=github_url
        )
        print(f"\nSuccessfully downloaded and triggered indexing!")
        print(f"Repo ID: {repo_id}")
        print(f"Name: {name}")
        print(f"Branch: {default_branch}")
        print(f"Commit: {commit_sha}")
        
        print("\nWaiting for background indexing to complete...")
        while True:
            # Need to commit or expire to clear session cache in loop
            db.commit()
            repo = get_repository(db, repo_id)
            if repo.status != "indexing":
                print(f"\nIndexing finished. Final status: {repo.status}")
                break
            time.sleep(2)
            print(".", end="", flush=True)

    except Exception as e:
        print(f"Failed to add repository: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    main()
