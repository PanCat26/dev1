import sys
import os
import threading
import time
import uuid
from contextlib import contextmanager

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from fastapi import BackgroundTasks

from database.session import get_db
from repository_management.manager import add_repository, delete_repository
from repository_management.crud import get_repository


def _run_background_tasks(background_tasks: BackgroundTasks) -> None:
    """Run queued BackgroundTasks in a daemon thread, mirroring FastAPI's
    after-response behavior so the script can keep polling for status.
    """
    def _runner():
        for task in background_tasks.tasks:
            task.func(*task.args, **task.kwargs)

    threading.Thread(target=_runner, daemon=True).start()


USAGE = (
    "Usage:\n"
    "  python scripts/run_repository_demo.py add <github_url>\n"
    "  python scripts/run_repository_demo.py delete <repo_id>\n"
    "\n"
    "Shortcut (backwards compatible):\n"
    "  python scripts/run_repository_demo.py <github_url>"
)


def cmd_add(github_url: str):
    print(f"Adding repository from GitHub: {github_url}")

    background_tasks = BackgroundTasks()

    with contextmanager(get_db)() as db:
        repo_id, default_branch, commit_sha, name = add_repository(
            db_session=db,
            github_link=github_url,
            background_tasks=background_tasks,
        )
        print(f"\nSuccessfully downloaded and triggered indexing!")
        print(f"Repo ID: {repo_id}")
        print(f"Name: {name}")
        print(f"Branch: {default_branch}")
        print(f"Commit: {commit_sha}")

        # No FastAPI request lifecycle here; run the queued tasks ourselves.
        _run_background_tasks(background_tasks)

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


def cmd_delete(repo_id_str: str):
    try:
        repo_id = uuid.UUID(repo_id_str)
    except ValueError:
        print(f"Invalid repo_id (must be a UUID): {repo_id_str}")
        sys.exit(1)

    with contextmanager(get_db)() as db:
        repo = get_repository(db, repo_id)
        if not repo:
            print(f"Repository {repo_id} not found.")
            sys.exit(1)

        print(f"Deleting repository {repo.name} ({repo_id})")
        print(f"  snapshot_path: {repo.snapshot_path}")
        print(f"  status:        {repo.status}")

        delete_repository(db_session=db, repo_id=repo_id)

        print("\nDeletion complete (DB row + Qdrant chunks + snapshot dir).")

        # Verify the repo is really gone from the DB.
        db.commit()
        still_there = get_repository(db, repo_id)
        if still_there is None:
            print("Verified: repository no longer in DB.")
        else:
            print("WARNING: repository still present in DB.")


def main():
    if len(sys.argv) < 2:
        print(USAGE)
        sys.exit(1)

    first = sys.argv[1]

    try:
        if first == "add":
            if len(sys.argv) < 3:
                print(USAGE)
                sys.exit(1)
            cmd_add(sys.argv[2])

        elif first == "delete":
            if len(sys.argv) < 3:
                print(USAGE)
                sys.exit(1)
            cmd_delete(sys.argv[2])

        else:
            # Backwards-compatible: treat a bare argument as a github URL to add.
            cmd_add(first)

    except Exception as e:
        print(f"Command failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
