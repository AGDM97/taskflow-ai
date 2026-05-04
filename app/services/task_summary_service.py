from app.schemas.task_schema import TaskResponse, TaskSummaryResponse
from app.services.ollama_client import ollama_client


class TaskSummaryService:
    def summarize(self, task: TaskResponse) -> TaskSummaryResponse:
        summary = ollama_client.generate_task_summary(
            title=task.title,
            description=task.description,
            status=task.status.value,
            priority=task.priority.value,
        )

        return TaskSummaryResponse(
            task_id=task.id,
            summary=summary,
        )


task_summary_service = TaskSummaryService()
