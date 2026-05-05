from pydantic import ValidationError

from app.schemas.task_schema import (
    SuggestedSubtask,
    TaskBreakdownResponse,
    TaskResponse,
)
from app.services.llm_client import llm_client


class InvalidLLMOutputError(Exception):
    pass


class TaskBreakdownService:
    def breakdown(self, task: TaskResponse) -> TaskBreakdownResponse:
        raw_subtasks = llm_client.generate_task_breakdown(
            title=task.title,
            description=task.description,
            status=task.status.value,
            priority=task.priority.value,
        )

        try:
            subtasks = [SuggestedSubtask.model_validate(item) for item in raw_subtasks]
            return TaskBreakdownResponse(
                task_id=task.id,
                subtasks=subtasks,
            )
        except ValidationError as error:
            raise InvalidLLMOutputError("Invalid LLM output") from error


task_breakdown_service = TaskBreakdownService()
