import uuid

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.session import get_db
from repository_management.crud import get_all_repositories, get_repository, create_feedback, update_feedback
from repository_management.manager import (
    add_repository,
    delete_repository,
    refresh_repository,
    retry_indexing,
)
from api.schemas import (
    AddRepositoryIn,
    RefreshOut,
    RepositoryAddedOut,
    RepositoryOut,
    RepositoryStatusOut,
    FeedbackCreateIn,
    FeedbackUpdateIn,
    FeedbackOut,
)

router = APIRouter(prefix="/repositories", tags=["repositories"])


@router.get("", response_model=list[RepositoryOut])
def list_repositories_endpoint(db: Session = Depends(get_db)):
    return [
        RepositoryOut(
            id=r.id,
            name=r.name,
            github_url=r.github_url,
            default_branch=r.default_branch,
            commit_sha=r.commit_sha,
            status=r.status,
            created_at=r.created_at,
        )
        for r in get_all_repositories(db)
    ]


@router.post("", response_model=RepositoryAddedOut, status_code=status.HTTP_201_CREATED)
def add_repository_endpoint(
    payload: AddRepositoryIn,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    repo_id, default_branch, commit_sha, name = add_repository(
        db_session=db,
        github_link=payload.github_url,
        background_tasks=background_tasks,
    )
    return RepositoryAddedOut(
        id=repo_id,
        name=name,
        default_branch=default_branch,
        commit_sha=commit_sha,
    )


@router.post("/{repo_id}/refresh", response_model=RefreshOut)
def refresh_repository_endpoint(
    repo_id: uuid.UUID,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    updated = refresh_repository(
        db_session=db,
        repo_id=repo_id,
        background_tasks=background_tasks,
    )
    return RefreshOut(updated=updated)


@router.post("/{repo_id}/retry", status_code=status.HTTP_202_ACCEPTED)
def retry_indexing_endpoint(
    repo_id: uuid.UUID,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    retry_indexing(
        db_session=db,
        repo_id=repo_id,
        background_tasks=background_tasks,
    )
    return {"status": "scheduled"}


@router.delete("/{repo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_repository_endpoint(
    repo_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    delete_repository(db_session=db, repo_id=repo_id)


@router.get("/{repo_id}/status", response_model=RepositoryStatusOut)
def get_repository_status_endpoint(
    repo_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    repo = get_repository(db, repo_id)
    if not repo:
        raise HTTPException(status_code=404, detail=f"Repository {repo_id} not found.")
    return RepositoryStatusOut(id=repo.id, status=repo.status, commit_sha=repo.commit_sha)


@router.patch("/{repo_id}/feedback/{feedback_id}", response_model=FeedbackOut)
def update_feedback_endpoint(
    repo_id: uuid.UUID,
    feedback_id: uuid.UUID,
    payload: FeedbackUpdateIn,
    db: Session = Depends(get_db),
):
    repo = get_repository(db, repo_id)
    if not repo:
        raise HTTPException(status_code=404, detail=f"Repository {repo_id} not found.")
        
    feedback = update_feedback(
        db=db,
        feedback_id=feedback_id,
        chosen=payload.chosen_response,
        rejected=payload.rejected_response
    )
    if not feedback:
        raise HTTPException(status_code=404, detail=f"Feedback {feedback_id} not found.")
    
    db.commit()
    db.refresh(feedback)
    
    return FeedbackOut(
        id=feedback.id,
        repository_id=feedback.repository_id,
        prompt=feedback.prompt,
        chosen_response=feedback.chosen_response,
        rejected_response=feedback.rejected_response,
        created_at=feedback.created_at
    )
