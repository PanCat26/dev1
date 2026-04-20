import os
import shutil
import threading
from typing import Tuple
import uuid

from config import SNAPSHOTS_DIR
from contextlib import contextmanager
from database.session import get_db
from repository_management.crud import create_repository, get_repository, update_repository_status
from indexing.service import run_indexing
from repository_management.github_utils import fetch_github_metadata, download_and_extract_zip

def _start_indexing_thread(repo_id: uuid.UUID, commit_sha: str, snapshot_path: str):
    thread = threading.Thread(
        target=_async_index_task, 
        args=(repo_id, commit_sha, snapshot_path),
        daemon=True
    )
    thread.start()

def _async_index_task(repo_id: uuid.UUID, commit_sha: str, snapshot_path: str):
    """Runs the indexing pipeline in the background and updates the repository status."""
    with contextmanager(get_db)() as db:
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



def add_repository(db_session, github_link: str) -> Tuple[uuid.UUID, str, str, str]:
    """Adds a repository organically using the GitHub REST API"""
    link = github_link.rstrip('/').split('/')
    if len(link) < 2:
        raise ValueError(f"Invalid GitHub link format: {github_link}")
    owner, repo_name = link[-2], link[-1]

    try:
        name, default_branch, commit_sha = fetch_github_metadata(owner, repo_name)
    except Exception as e:
        raise ValueError(f"Could not reach GitHub or repository not found: {str(e)}")
        
    repo = None
    target_path = None
    try:
        repo = create_repository(
            db=db_session, 
            name=name, 
            github_url=github_link,
            default_branch=default_branch,
            snapshot_path="pending", 
            commit_sha=commit_sha
        )
        db_session.flush()
    
        target_dir_name = f"{name}_{str(repo.id)[:8]}"
        target_path = os.path.abspath(os.path.join(SNAPSHOTS_DIR, target_dir_name))
    
        download_and_extract_zip(owner, repo_name, commit_sha, target_path)
        
        repo.snapshot_path = target_path
        db_session.commit()
        
        _start_indexing_thread(repo.id, commit_sha, target_path)
        return (repo.id, default_branch, commit_sha, name)
        
    except Exception as e:
        db_session.rollback()
        if target_path and os.path.exists(target_path):
            shutil.rmtree(target_path)
        raise

def retry_indexing(db_session, repo_id: uuid.UUID):
    """Retries indexing for an existing repository."""
    repo = get_repository(db_session, repo_id)
    if not repo:
        raise ValueError(f"Repository {repo_id} not found.")
    
    if not os.path.exists(repo.snapshot_path):
        raise ValueError(f"Snapshot path {repo.snapshot_path} does not exist.")
        
    repo.status = "indexing"
    db_session.commit()
    
    _start_indexing_thread(repo.id, repo.commit_sha, repo.snapshot_path)

def refresh_repository(db_session, repo_id: uuid.UUID) -> bool:
    """Pulls the latest changes (if any) and reindexes the repository."""
    repo = get_repository(db_session, repo_id)
    if not repo:
        raise ValueError(f"Repository {repo_id} not found.")
        
    link = repo.github_url.rstrip('/').split('/')
    owner, repo_name = link[-2], link[-1]
    
    try:
        _, _, commit_sha = fetch_github_metadata(owner, repo_name)
    except Exception as e:
        raise ValueError(f"Could not reach GitHub or repository not found: {str(e)}")
    
    if commit_sha == repo.commit_sha:
        print(f"[{repo_id}] Already up-to-date at commit {commit_sha}")
        return False
        
    print(f"[{repo_id}] New commit found: {commit_sha} (old: {repo.commit_sha})")
    original_path = repo.snapshot_path
    temp_path = f"{original_path}_temp"
    backup_path = f"{original_path}_backup"

    # Cleanup potential leftovers from previous botched refreshes
    if os.path.exists(temp_path):
        shutil.rmtree(temp_path)
    if os.path.exists(backup_path):
        shutil.rmtree(backup_path)

    try:
        # 1. Download to temp dir
        download_and_extract_zip(owner, repo_name, commit_sha, temp_path)
        
        # 2. Swap old -> backup, temp -> snapshot
        if os.path.exists(original_path):
            os.rename(original_path, backup_path)
        os.rename(temp_path, original_path)
        
        # 3. Update DB fields + commit
        repo.commit_sha = commit_sha
        repo.status = "indexing"
        db_session.commit()
        
        # 4. Delete backup
        if os.path.exists(backup_path):
            shutil.rmtree(backup_path)
            
        # 5. Start thread
        _start_indexing_thread(repo.id, repo.commit_sha, repo.snapshot_path)
        return True
        
    except Exception as e:
        db_session.rollback()
        
        # Restore backup -> snapshot
        if os.path.exists(backup_path):
            if os.path.exists(original_path):
                shutil.rmtree(original_path)
            os.rename(backup_path, original_path)
            
        # Delete temp
        if os.path.exists(temp_path):
            shutil.rmtree(temp_path)
            
        raise
