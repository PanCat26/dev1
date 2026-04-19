import asyncio
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.session import get_db
from repository_management.crud import (
    create_conversation,
    delete_conversation,
    get_conversations,
    get_repository,
)
from api.schemas import ConversationOut

router = APIRouter(tags=["conversations"])


def _to_out(conv) -> ConversationOut:
    return ConversationOut(
        id=conv.id,
        repository_id=conv.repository_id,
        created_at=conv.created_at,
    )


@router.get("/repositories/{repo_id}/conversations", response_model=list[ConversationOut])
async def list_conversations_endpoint(
    repo_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    repo = await asyncio.to_thread(get_repository, db, repo_id)
    if not repo:
        raise HTTPException(status_code=404, detail=f"Repository {repo_id} not found.")

    convs = await asyncio.to_thread(get_conversations, db, repo_id)
    return [_to_out(c) for c in convs]


@router.post(
    "/repositories/{repo_id}/conversations",
    response_model=ConversationOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_conversation_endpoint(
    repo_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    repo = await asyncio.to_thread(get_repository, db, repo_id)
    if not repo:
        raise HTTPException(status_code=404, detail=f"Repository {repo_id} not found.")

    conv = await asyncio.to_thread(create_conversation, db, repo_id)
    await asyncio.to_thread(db.commit)
    await asyncio.to_thread(db.refresh, conv)
    return _to_out(conv)


@router.delete("/conversations/{conv_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_conversation_endpoint(
    conv_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    deleted = await asyncio.to_thread(delete_conversation, db, conv_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Conversation {conv_id} not found.")
    await asyncio.to_thread(db.commit)
