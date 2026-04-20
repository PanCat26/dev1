import os
import sys

# setup path
sys.path.append("/Users/cristian.steopei/Desktop/Learning/UBB-CS/ThirdYear/Dev1/dev1/code/backend")

from database.session import SessionLocal
from repository_management.crud import get_repository

def check():
    db = SessionLocal()
    repo_id = "6203f486-d823-42ce-bd27-bdcfef39782b"
    repo = get_repository(db, repo_id)
    if not repo:
        print("Repo not found")
        return
    print(f"Status: {repo.status}")
    print(f"Snapshot path: {repo.snapshot_path}")

if __name__ == "__main__":
    check()
