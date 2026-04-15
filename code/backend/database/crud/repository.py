from sqlalchemy.orm import Session
import uuid
from database.models.repository import Repository
from database.models.conversation import Conversation
from typing import List, Optional

class RepositoryService:
    @staticmethod
    def create_repository(db: Session, name: str, snapshot_path: str, commit_sha: str = None) -> Repository:
        db_repo = Repository(
            name=name,
            snapshot_path=snapshot_path,
            commit_sha=commit_sha
        )
        db.add(db_repo)
        db.commit()
        db.refresh(db_repo)
        return db_repo

    @staticmethod
    def get_repository(db: Session, repo_id: uuid.UUID) -> Optional[Repository]:
        return db.query(Repository).filter(Repository.id == repo_id).first()

    @staticmethod
    def update_repository_status(db: Session, repo_id: uuid.UUID, status: str) -> Optional[Repository]:
        db_repo = RepositoryService.get_repository(db, repo_id)
        if db_repo:
            db_repo.status = status
            db.commit()
            db.refresh(db_repo)
        return db_repo

    @staticmethod
    def get_all_repositories(db: Session) -> List[Repository]:
        return db.query(Repository).all()

    @staticmethod
    def create_conversation(db: Session, repo_id: uuid.UUID) -> Conversation:
        db_conv = Conversation(repository_id=repo_id)
        db.add(db_conv)
        db.commit()
        db.refresh(db_conv)
        return db_conv

    @staticmethod
    def get_conversations(db: Session, repo_id: uuid.UUID) -> List[Conversation]:
        return db.query(Conversation).filter(Conversation.repository_id == repo_id).all()
