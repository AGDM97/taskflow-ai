from app.schemas.task_schema import TaskResponse, TaskSummaryResponse
from app.services.llm_client import llm_client


class TaskSummaryService:
    def summarize(self, task: TaskResponse) -> TaskSummaryResponse:
        summary = llm_client.generate_task_summary(
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
