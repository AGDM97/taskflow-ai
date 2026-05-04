from app.schemas.task_schema import TaskResponse, TaskSummaryResponse


class TaskSummaryService:
    def summarize(self, task: TaskResponse) -> TaskSummaryResponse:
        description_text = (
            f" Description: {task.description}"
            if task.description
            else " No description was provided."
        )

        summary = (
            f"Task '{task.title}' is currently {task.status.value}. "
            f"Priority is {task.priority.value}."
            f"{description_text}"
        )

        return TaskSummaryResponse(
            task_id=task.id,
            summary=summary,
        )


task_summary_service = TaskSummaryService()
