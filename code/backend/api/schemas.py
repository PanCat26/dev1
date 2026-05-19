import uuid
from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class AddRepositoryIn(BaseModel):
    github_url: str


class RepositoryAddedOut(BaseModel):
    id: uuid.UUID
    name: str
    default_branch: str
    commit_sha: str
    status: str = "indexing"


class RefreshOut(BaseModel):
    updated: bool


class RepositoryStatusOut(BaseModel):
    id: uuid.UUID
    status: str
    commit_sha: str


class RepositoryOut(BaseModel):
    id: uuid.UUID
    name: str
    github_url: str
    default_branch: str
    commit_sha: str
    status: str
    created_at: datetime


class ConversationOut(BaseModel):
    id: uuid.UUID
    repository_id: uuid.UUID
    created_at: datetime


class MessageCreateIn(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str


class MessageOut(BaseModel):
    id: uuid.UUID
    conversation_id: uuid.UUID
    role: str
    content: str
    created_at: datetime


class FeedbackCreateIn(BaseModel):
    prompt: str
    chosen_response: str
    rejected_response: str


from typing import Literal, Optional

class FeedbackUpdateIn(BaseModel):
    chosen_response: str
    rejected_response: str
    message_id: Optional[uuid.UUID] = None


class FeedbackOut(BaseModel):
    id: uuid.UUID
    repository_id: uuid.UUID
    prompt: str
    chosen_response: str
    rejected_response: str
    created_at: datetime
