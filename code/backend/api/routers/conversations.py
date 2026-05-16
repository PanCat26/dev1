import uuid
import json

from fastapi import APIRouter, Depends, HTTPException, status, WebSocket, WebSocketDisconnect
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
from orchestration.service import answer_query

router = APIRouter(tags=["conversations"])


def _to_out(conv) -> ConversationOut:
    return ConversationOut(
        id=conv.id,
        repository_id=conv.repository_id,
        created_at=conv.created_at,
    )


def _msg_to_out(m) -> MessageOut:
    return MessageOut(
        id=m.id,
        conversation_id=m.conversation_id,
        role=m.role,
        content=m.content,
        created_at=m.created_at,
    )


@router.get("/repositories/{repo_id}/conversations", response_model=list[ConversationOut])
def list_conversations_endpoint(
    repo_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    repo = get_repository(db, repo_id)
    if not repo:
        raise HTTPException(status_code=404, detail=f"Repository {repo_id} not found.")

    return [_to_out(c) for c in get_conversations(db, repo_id)]


@router.post(
    "/repositories/{repo_id}/conversations",
    response_model=ConversationOut,
    status_code=status.HTTP_201_CREATED,
)
def create_conversation_endpoint(
    repo_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    repo = get_repository(db, repo_id)
    if not repo:
        raise HTTPException(status_code=404, detail=f"Repository {repo_id} not found.")

    conv = create_conversation(db, repo_id)
    db.commit()
    db.refresh(conv)
    return _to_out(conv)


@router.delete("/conversations/{conv_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_conversation_endpoint(
    conv_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    deleted = delete_conversation(db, conv_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Conversation {conv_id} not found.")
    db.commit()


@router.get("/conversations/{conv_id}/messages", response_model=list[MessageOut])
def list_messages_endpoint(
    conv_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    conv = get_conversation(db, conv_id)
    if not conv:
        raise HTTPException(status_code=404, detail=f"Conversation {conv_id} not found.")

    return [_msg_to_out(m) for m in get_messages(db, conv_id)]


@router.post(
    "/conversations/{conv_id}/messages",
    response_model=MessageOut,
    status_code=status.HTTP_201_CREATED,
)
def create_message_endpoint(
    conv_id: uuid.UUID,
    payload: MessageCreateIn,
    db: Session = Depends(get_db),
):
    conv = get_conversation(db, conv_id)
    if not conv:
        raise HTTPException(status_code=404, detail=f"Conversation {conv_id} not found.")

    msg = create_message(db, conv_id, payload.role, payload.content)
    db.commit()
    db.refresh(msg)
    return _msg_to_out(msg)

from fastapi.concurrency import run_in_threadpool

@router.websocket("/conversations/{conv_id}/ws")
async def conversation_websocket(
    websocket: WebSocket,
    conv_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    await websocket.accept()
    
    # We must use run_in_threadpool for all synchronous DB operations inside async route
    conv = await run_in_threadpool(get_conversation, db, conv_id)
    if not conv:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason="Conversation not found")
        return
        
    repo = await run_in_threadpool(get_repository, db, conv.repository_id)
    if not repo:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason="Repository not found")
        return
        
    try:
        while True:
            
            data = await websocket.receive_text()
            
            # Save user query
            await run_in_threadpool(create_message, db, conv_id, "user", data)
            await run_in_threadpool(db.commit)
            
            full_answer = ""
            async for chunk in answer_query(
                str(repo.id),
                repo.commit_sha,
                repo.snapshot_path,
                data,
            ):
                await websocket.send_text(chunk)
                try:
                    event = json.loads(chunk)
                    if event.get("type") == "content":
                        full_answer += event.get("delta", "")
                except json.JSONDecodeError:
                    pass
                    
            if full_answer:
                await run_in_threadpool(create_message, db, conv_id, "assistant", full_answer)
                await run_in_threadpool(db.commit)
                
            # Signal the client that the generation turn has concluded
            await websocket.send_text(json.dumps({"type": "done"}))
                
    except WebSocketDisconnect:
        pass
    except Exception as e:
        await websocket.send_text(json.dumps({"type": "error", "message": str(e)}))
        await websocket.close(code=status.WS_1011_INTERNAL_ERROR)
