from fastapi import APIRouter, status

from app.schemas.task_schema import CreateTaskRequest, TaskResponse
from app.services.task_service import task_service

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(request: CreateTaskRequest) -> TaskResponse:
    return task_service.create_task(request)


@router.get("", response_model=list[TaskResponse])
def list_tasks() -> list[TaskResponse]:
    return task_service.list_tasks()
