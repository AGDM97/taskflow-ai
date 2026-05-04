from fastapi import APIRouter, HTTPException, status

from app.schemas.task_schema import (
    CreateTaskRequest,
    TaskResponse,
    UpdateTaskStatusRequest,
)
from app.services.task_service import task_service

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(request: CreateTaskRequest) -> TaskResponse:
    return task_service.create_task(request)


@router.get("", response_model=list[TaskResponse])
def list_tasks() -> list[TaskResponse]:
    return task_service.list_tasks()


@router.get("/{task_id}", response_model=TaskResponse)
def get_task_by_id(task_id: str) -> TaskResponse:
    task = task_service.get_task_by_id(task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return task


@router.patch("/{task_id}/status", response_model=TaskResponse)
def update_task_status(
    task_id: str,
    request: UpdateTaskStatusRequest,
) -> TaskResponse:
    task = task_service.update_task_status(task_id, request.status)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return task