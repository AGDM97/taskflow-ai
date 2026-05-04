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

    def get_task_by_id(self, task_id: str) -> TaskResponse | None:
        return self._tasks.get(task_id)

    def update_task_status(
        self,
        task_id: str,
        new_status: TaskStatus,
    ) -> TaskResponse | None:
        task = self._tasks.get(task_id)

        if task is None:
            return None

        updated_task = task.model_copy(update={"status": new_status})
        self._tasks[task_id] = updated_task

        return updated_task


task_service = TaskService()