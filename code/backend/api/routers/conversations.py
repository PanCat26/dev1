import uuid
import json

from fastapi import APIRouter, Depends, HTTPException, status, WebSocket, WebSocketDisconnect
from fastapi.concurrency import run_in_threadpool
from sqlalchemy.orm import Session

from database.session import SessionLocal, get_db
from repository_management.crud import (
    create_conversation,
    create_message,
    delete_conversation,
    get_conversation,
    get_conversations,
    get_messages,
    get_repository,
    create_feedback,
)
from api.schemas import ConversationOut, MessageCreateIn, MessageOut
from orchestration.history import bounded_history_for_llm
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


def _ws_persist_message(conv_id: uuid.UUID, role: str, content: str) -> None:
    db = SessionLocal()
    try:
        create_message(db, conv_id, role, content)
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def _ws_persist_rlhf_prompt(repo_id: uuid.UUID, prompt: str) -> str:
    db = SessionLocal()
    try:
        feedback = create_feedback(db, repo_id, prompt)
        db.commit()
        return str(feedback.id)
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def _ws_load_repo_context_and_history(
    conv_id: uuid.UUID,
) -> tuple[tuple[str, str, str], list[dict[str, str]]] | None:
    """One DB session: fresh repo id/commit/snapshot plus bounded history (before this turn's user row)."""
    db = SessionLocal()
    try:
        conv = get_conversation(db, conv_id)
        if not conv:
            return None
        repo = get_repository(db, conv.repository_id)
        if not repo:
            return None
        msgs = get_messages(db, conv_id)
        history = bounded_history_for_llm(msgs)
        ctx = (str(repo.id), repo.commit_sha, repo.snapshot_path)
        return (ctx, history)
    finally:
        db.close()


@router.websocket("/conversations/{conv_id}/ws")
async def conversation_websocket(
    websocket: WebSocket,
    conv_id: uuid.UUID,
):
    await websocket.accept()

    async def _safe_send(text: str) -> bool:
        try:
            await websocket.send_text(text)
            return True
        except Exception:
            return False

    try:
        while True:
            data = (await websocket.receive_text()).strip()
            if not data:
                await _safe_send(json.dumps({"type": "error", "message": "Empty message."}))
                continue

            try:
                loaded = await run_in_threadpool(_ws_load_repo_context_and_history, conv_id)
            except Exception as e:
                await _safe_send(
                    json.dumps({"type": "error", "message": f"Failed to load conversation context: {e}"})
                )
                continue
            if loaded is None:
                await _safe_send(
                    json.dumps({"type": "error", "message": "Conversation or repository not found."})
                )
                continue
            (repo_id, commit_sha, snapshot_path), history_messages = loaded

            try:
                await run_in_threadpool(_ws_persist_message, conv_id, "user", data)
            except Exception as e:
                await _safe_send(
                    json.dumps({"type": "error", "message": f"Failed to save user message: {e}"})
                )
                continue

            full_answer = ""
            gen = None
            try:
                gen = answer_query(
                    repo_id,
                    commit_sha,
                    snapshot_path,
                    data,
                    history_messages=history_messages,
                )
                async for chunk in gen:
                    if not await _safe_send(chunk):
                        break
                    try:
                        event = json.loads(chunk)
                        if event.get("type") == "content":
                            full_answer += event.get("delta", "") or ""
                        elif event.get("type") == "rlhf_prompt":
                            prompt_str = event.get("prompt", "")
                            feedback_id = await run_in_threadpool(_ws_persist_rlhf_prompt, uuid.UUID(repo_id), prompt_str)
                            await _safe_send(json.dumps({"type": "rlhf_feedback_id", "id": feedback_id}))
                    except json.JSONDecodeError:
                        pass
            except Exception as e:
                await _safe_send(json.dumps({"type": "error", "message": f"Generation failed: {e}"}))
            finally:
                if gen is not None:
                    await gen.aclose()

            if full_answer:
                try:
                    await run_in_threadpool(_ws_persist_message, conv_id, "assistant", full_answer)
                except Exception as e:
                    await _safe_send(
                        json.dumps({"type": "error", "message": f"Failed to save assistant message: {e}"})
                    )

            await _safe_send(json.dumps({"type": "done"}))

    except WebSocketDisconnect:
        pass
    except Exception as e:
        try:
            await _safe_send(json.dumps({"type": "error", "message": str(e)}))
            await websocket.close(code=status.WS_1011_INTERNAL_ERROR)
        except Exception:
            pass
