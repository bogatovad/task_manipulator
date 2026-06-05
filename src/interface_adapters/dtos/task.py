from pydantic import BaseModel

from src.entities.task import TaskPriority, TaskStatus, TypeTask
from datetime import datetime


class TaskDto(BaseModel):
    task_id: int | None = None
    name: str
    description: str
    priority: TaskPriority
    type_task: TypeTask = TypeTask.CPU
    status: TaskStatus
    created_at: datetime | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    result: dict = {}
    info: dict = {}
