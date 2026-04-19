import uuid
from datetime import datetime

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


class ConversationOut(BaseModel):
    id: uuid.UUID
    repository_id: uuid.UUID
    created_at: datetime
