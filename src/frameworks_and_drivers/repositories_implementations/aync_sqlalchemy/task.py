from sqlalchemy.ext.asyncio import AsyncSession

from src.frameworks_and_drivers.repositories_implementations.aync_sqlalchemy.models import (
    Task as TaskModel,
)
from src.interface_adapters.dtos.task import TaskDto
from src.interface_adapters.repositories_interfaces.task import TaskStorageInterface


class TaskSqlAlchemyRepository(TaskStorageInterface):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_task(self, task: TaskDto) -> bool:
        db_task = TaskModel(**task.model_dump())
        self.session.add(db_task)
        await self.session.flush()
        return True
