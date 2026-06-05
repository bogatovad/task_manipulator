from enum import StrEnum
from datetime import datetime


class TaskPriority(StrEnum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class TaskStatus(StrEnum):
    NEW = "NEW"
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELED = "CANCELED"


class TypeTask(StrEnum):
    CPU = "CPU"
    MEMORY = "MEMORY"
    LLM = "LLM"


class Task:
    name: str
    description: str
    priority: TaskPriority
    status: str
    created_at: datetime
    start_date: datetime
    end_date: datetime
    result: dict
    info: dict
