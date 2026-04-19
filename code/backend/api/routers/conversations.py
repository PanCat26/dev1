import asyncio
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.session import get_db
from repository_management.crud import (
    create_conversation,
    create_message,
    delete_conversation,
    get_conversation,
    get_conversations,
    get_messages,
    get_repository,
)
from api.schemas import ConversationOut, MessageCreateIn, MessageOut

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


def _msg_to_out(m) -> MessageOut:
    return MessageOut(
        id=m.id,
        conversation_id=m.conversation_id,
        role=m.role,
        content=m.content,
        created_at=m.created_at,
    )


@router.get("/conversations/{conv_id}/messages", response_model=list[MessageOut])
async def list_messages_endpoint(
    conv_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    conv = await asyncio.to_thread(get_conversation, db, conv_id)
    if not conv:
        raise HTTPException(status_code=404, detail=f"Conversation {conv_id} not found.")

    messages = await asyncio.to_thread(get_messages, db, conv_id)
    return [_msg_to_out(m) for m in messages]


@router.post(
    "/conversations/{conv_id}/messages",
    response_model=MessageOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_message_endpoint(
    conv_id: uuid.UUID,
    payload: MessageCreateIn,
    db: Session = Depends(get_db),
):
    conv = await asyncio.to_thread(get_conversation, db, conv_id)
    if not conv:
        raise HTTPException(status_code=404, detail=f"Conversation {conv_id} not found.")

    msg = await asyncio.to_thread(create_message, db, conv_id, payload.role, payload.content)
    await asyncio.to_thread(db.commit)
    await asyncio.to_thread(db.refresh, msg)
    return _msg_to_out(msg)
