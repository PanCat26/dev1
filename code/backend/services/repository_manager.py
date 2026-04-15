import os
import shutil
import threading
from typing import Optional
import uuid

from config import SNAPSHOTS_DIR
from database.session import SessionLocal
from database.crud.repository import RepositoryService
from indexing.service import run_indexing

class RepositoryManager:
    @staticmethod
    def _async_index_task(repo_id: uuid.UUID, commit_sha: str, snapshot_path: str):
        """Runs the indexing pipeline in the background and updates the repository status."""
        db = SessionLocal()
        try:
            # Run the indexing pipeline
            print(f"[{repo_id}] Starting indexing pipeline on {snapshot_path}...")
            result = run_indexing(str(repo_id), commit_sha, snapshot_path)
            
            if result.errors:
                print(f"[{repo_id}] Indexing finished with errors.")
                RepositoryService.update_repository_status(db, repo_id, "failed")
            else:
                print(f"[{repo_id}] Indexing completed successfully.")
                RepositoryService.update_repository_status(db, repo_id, "ready")
        except Exception as e:
            print(f"[{repo_id}] Exception during indexing: {e}")
            RepositoryService.update_repository_status(db, repo_id, "failed")
        finally:
            db.close()

    @staticmethod
    def add_local_repository(db_session, name: str, source_path: str, commit_sha: str = "unknown"):
        """
        Creates a repository entry, snapshots the source directory to disk, 
        and triggers the indexing pipeline asynchronously.
        """
        if not os.path.exists(source_path):
            raise ValueError(f"Source path {source_path} does not exist.")

        # 1. Create a placeholder repository to get the UUID
        repo = RepositoryService.create_repository(
            db=db_session, 
            name=name, 
            snapshot_path="pending", 
            commit_sha=commit_sha
        )
        
        # 2. Define target snapshot directory
        target_dir_name = f"{name}_{str(repo.id)[:8]}"
        target_path = os.path.abspath(os.path.join(SNAPSHOTS_DIR, target_dir_name))
        
        # 3. Copy files bypassing large generated directories
        print(f"Copying snapshot from {source_path} to {target_path}...")
        ignore_patterns = shutil.ignore_patterns('.git', '.venv', 'venv', 'node_modules', '__pycache__', '.pytest_cache', 'alembic', 'storage')
        shutil.copytree(source_path, target_path, ignore=ignore_patterns, dirs_exist_ok=True)
        
        # 4. Update the DB repo with actual snapshot path
        repo.snapshot_path = target_path
        db_session.commit()
        db_session.refresh(repo)

        # 5. Trigger async indexing
        thread = threading.Thread(
            target=RepositoryManager._async_index_task, 
            args=(repo.id, commit_sha, target_path),
            daemon=True
        )
        thread.start()
        
        return repo
