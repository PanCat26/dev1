import uuid

from fastapi import APIRouter, BackgroundTasks, Depends, status
from sqlalchemy.orm import Session

from database.session import get_db
from repository_management.manager import (
    add_repository,
    delete_repository,
    refresh_repository,
    retry_indexing,
)
from api.schemas import AddRepositoryIn, RefreshOut, RepositoryAddedOut

router = APIRouter(prefix="/repositories", tags=["repositories"])


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
