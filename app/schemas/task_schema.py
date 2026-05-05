from enum import Enum
from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"
    BLOCKED = "BLOCKED"


class TaskPriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class CreateTaskRequest(BaseModel):
    title: str = Field(..., min_length=3)
    description: str | None = None
    priority: TaskPriority = TaskPriority.MEDIUM


class UpdateTaskStatusRequest(BaseModel):
    status: TaskStatus


class TaskResponse(BaseModel):
    id: str
    title: str
    description: str | None
    status: TaskStatus
    priority: TaskPriority


class TaskSummaryResponse(BaseModel):
    task_id: str
    summary: str


class SuggestedSubtask(BaseModel):
    title: str = Field(..., min_length=3)
    description: str = Field(..., min_length=3)
    priority: TaskPriority


class TaskBreakdownResponse(BaseModel):
    task_id: str
    subtasks: list[SuggestedSubtask] = Field(..., min_length=3, max_length=7)
