import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from .base import Base

class Repository(Base):
    __tablename__ = "repositories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    github_url = Column(String, nullable=False)
    default_branch = Column(String, nullable=False)
    commit_sha = Column(String, nullable=False)
    snapshot_path = Column(String, nullable=False)
    status = Column(String, nullable=False, default="indexing")
    created_at = Column(DateTime, default=datetime.utcnow)

