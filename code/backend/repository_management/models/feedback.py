import uuid
from datetime import datetime
from sqlalchemy import Column, DateTime, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from .base import Base

class RLHFFeedback(Base):
    __tablename__ = "rlhf_feedback"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    repository_id = Column(UUID(as_uuid=True), ForeignKey("repositories.id", ondelete="CASCADE"), nullable=False)
    prompt = Column(Text, nullable=False)
    chosen_response = Column(Text, nullable=True)
    rejected_response = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
