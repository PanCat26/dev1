from sqlalchemy.orm import Session
import uuid
from database.models.repository import Repository
from database.models.conversation import Conversation
from typing import List, Optional

def create_repository(db: Session, name: str, github_url: str, default_branch: str, snapshot_path: str, commit_sha: str = None) -> Repository:
    db_repo = Repository(
        name=name,
        github_url=github_url,
        default_branch=default_branch,
        snapshot_path=snapshot_path,
        commit_sha=commit_sha
    )
    db.add(db_repo)
    return db_repo

def get_repository(db: Session, repo_id: uuid.UUID) -> Optional[Repository]:
    return db.query(Repository).filter(Repository.id == repo_id).first()

def update_repository_status(db: Session, repo_id: uuid.UUID, status: str) -> Optional[Repository]:
    db_repo = get_repository(db, repo_id)
    if db_repo:
        db_repo.status = status
    return db_repo

def get_all_repositories(db: Session) -> List[Repository]:
    return db.query(Repository).all()

def create_conversation(db: Session, repo_id: uuid.UUID) -> Conversation:
    db_conv = Conversation(repository_id=repo_id)
    db.add(db_conv)
    return db_conv

def get_conversations(db: Session, repo_id: uuid.UUID) -> List[Conversation]:
    return db.query(Conversation).filter(Conversation.repository_id == repo_id).all()
