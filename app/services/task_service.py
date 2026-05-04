from uuid import uuid4

from app.schemas.task_schema import (
    CreateTaskRequest,
    TaskPriority,
    TaskResponse,
    TaskStatus,
)


class TaskService:
    def __init__(self):
        self._tasks: dict[str, TaskResponse] = {}

    def create_task(self, request: CreateTaskRequest) -> TaskResponse:
        task = TaskResponse(
            id=str(uuid4()),
            title=request.title,
            description=request.description,
            status=TaskStatus.TODO,
            priority=request.priority or TaskPriority.MEDIUM,
        )

        self._tasks[task.id] = task
        return task

    def list_tasks(self) -> list[TaskResponse]:
        return list(self._tasks.values())


task_service = TaskService()