import os
import shutil
import threading
from typing import Tuple
import uuid

from config import SNAPSHOTS_DIR, GITHUB_TOKEN
from repository_management.session import SessionLocal
from repository_management.repository import create_repository, get_repository, update_repository_status
from indexing.service import run_indexing
from repository_management.github_utils import fetch_github_metadata, download_and_extract_zip

def _async_index_task(repo_id: uuid.UUID, commit_sha: str, snapshot_path: str):
    """Runs the indexing pipeline in the background and updates the repository status."""
    db = SessionLocal()
    try:
        print(f"[{repo_id}] Starting indexing pipeline on {snapshot_path}...")
        result = run_indexing(str(repo_id), commit_sha, snapshot_path)
        
        if result.errors:
            print(f"[{repo_id}] Indexing finished with errors.")
            update_repository_status(db, repo_id, "failed")
        else:
            print(f"[{repo_id}] Indexing completed successfully.")
            update_repository_status(db, repo_id, "ready")
        db.commit()
    except Exception as e:
        print(f"[{repo_id}] Exception during indexing: {e}")
        update_repository_status(db, repo_id, "failed")
        db.commit()
    finally:
        db.close()



def add_repository(db_session, github_link: str) -> Tuple[uuid.UUID, str, str, str]:
    """Adds a repository organically using the GitHub REST API"""
    link = github_link.rstrip('/').split('/')
    if len(link) < 2:
        raise ValueError(f"Invalid GitHub link format: {github_link}")
    owner, repo_name = link[-2], link[-1]

    name, default_branch, commit_sha = fetch_github_metadata(owner, repo_name)
    
    repo = create_repository(
        db=db_session, 
        name=name, 
        github_url=github_link,
        default_branch=default_branch,
        snapshot_path="pending", 
        commit_sha=commit_sha
    )
    db_session.commit()
    db_session.refresh(repo)
    
    target_dir_name = f"{name}_{str(repo.id)[:8]}"
    target_path = os.path.abspath(os.path.join(SNAPSHOTS_DIR, target_dir_name))
    
    try:
        download_and_extract_zip(owner, repo_name, commit_sha, target_path)
        
        repo.snapshot_path = target_path
        db_session.commit()
        db_session.refresh(repo)
        
        retry_indexing(db_session, repo.id)
        return (repo.id, repo.default_branch, repo.commit_sha, repo.name)
        
    except Exception as e:
        db_session.delete(repo)
        db_session.commit()
        if os.path.exists(target_path):
            shutil.rmtree(target_path)
        raise e

def retry_indexing(db_session, repo_id: uuid.UUID):
    """Retries indexing for an existing repository."""
    repo = get_repository(db_session, repo_id)
    if not repo:
        raise ValueError(f"Repository {repo_id} not found.")
    
    if not os.path.exists(repo.snapshot_path):
        raise ValueError(f"Snapshot path {repo.snapshot_path} does not exist.")
        
    repo.status = "indexing"
    db_session.commit()
    
    thread = threading.Thread(
        target=_async_index_task, 
        args=(repo.id, repo.commit_sha, repo.snapshot_path),
        daemon=True
    )
    thread.start()

def refresh_repository(db_session, repo_id: uuid.UUID) -> bool:
    """Pulls the latest changes (if any) and reindexes the repository."""
    repo = get_repository(db_session, repo_id)
    if not repo:
        raise ValueError(f"Repository {repo_id} not found.")
        
    link = repo.github_url.rstrip('/').split('/')
    owner, repo_name = link[-2], link[-1]
    
    _, _, commit_sha = fetch_github_metadata(owner, repo_name)
    
    if commit_sha == repo.commit_sha:
        print(f"[{repo_id}] Already up-to-date at commit {commit_sha}")
        return False
        
    print(f"[{repo_id}] New commit found: {commit_sha} (old: {repo.commit_sha})")
    download_and_extract_zip(owner, repo_name, commit_sha, repo.snapshot_path)
    
    repo.commit_sha = commit_sha
    repo.status = "indexing"
    db_session.commit()
    
    retry_indexing(db_session, repo.id)
    return True
