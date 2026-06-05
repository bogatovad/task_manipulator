from sqlalchemy import Column, DateTime, Enum, String, BigInteger, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base
from src.entities.task import TaskPriority, TaskStatus, TypeTask
from datetime import datetime

Base = declarative_base()


class Task(Base):
    __tablename__ = "task"

    task_id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(255))
    description = Column(Text)
    priority = Column(Enum(TaskPriority))
    type_task = Column(Enum(TypeTask), default=TypeTask.CPU)
    status = Column(Enum(TaskStatus))
    created_at = Column(DateTime, default=datetime.utcnow)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    result = Column(JSONB, nullable=True, default=dict)
    info = Column(JSONB, nullable=True, default=dict)

    def __repr__(self):
        return f"<Task(task_id={self.task_id})>"
