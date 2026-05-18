from sqlalchemy.orm import Session
import uuid
from repository_management.models.repository import Repository
from repository_management.models.conversation import Conversation
from repository_management.models.message import Message
from repository_management.models.feedback import RLHFFeedback
from typing import List, Optional

def create_repository(db: Session, name: str, github_url: str, default_branch: str, snapshot_path: str, commit_sha: str) -> Repository:
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

def get_conversation(db: Session, conv_id: uuid.UUID) -> Optional[Conversation]:
    return db.query(Conversation).filter(Conversation.id == conv_id).first()

def delete_conversation(db: Session, conv_id: uuid.UUID) -> bool:
    db_conv = get_conversation(db, conv_id)
    if not db_conv:
        return False
    db.delete(db_conv)
    return True

def get_messages(db: Session, conv_id: uuid.UUID) -> List[Message]:
    return (
        db.query(Message)
        .filter(Message.conversation_id == conv_id)
        .order_by(Message.created_at)
        .all()
    )

def create_message(db: Session, conv_id: uuid.UUID, role: str, content: str) -> Message:
    db_msg = Message(conversation_id=conv_id, role=role, content=content)
    db.add(db_msg)
    return db_msg

def create_feedback(db: Session, repo_id: uuid.UUID, prompt: str, chosen: Optional[str] = None, rejected: Optional[str] = None) -> RLHFFeedback:
    db_feedback = RLHFFeedback(
        repository_id=repo_id,
        prompt=prompt,
        chosen_response=chosen,
        rejected_response=rejected
    )
    db.add(db_feedback)
    return db_feedback

def update_feedback(db: Session, feedback_id: uuid.UUID, chosen: str, rejected: str) -> Optional[RLHFFeedback]:
    db_feedback = db.query(RLHFFeedback).filter(RLHFFeedback.id == feedback_id).first()
    if db_feedback:
        db_feedback.chosen_response = chosen
        db_feedback.rejected_response = rejected
    return db_feedback
