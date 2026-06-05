from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.entities.exceptions import TaskNotFoundError
from src.entities.task import TaskStatus
from src.frameworks_and_drivers.repositories_implementations.aync_sqlalchemy.models import (
    Task as TaskModel,
)
from src.interface_adapters.dtos.task import TaskDto
from src.interface_adapters.repositories_interfaces.task import TaskStorageInterface


class TaskSqlAlchemyRepository(TaskStorageInterface):
    def __init__(self, session: AsyncSession):
        self.session = session

    @staticmethod
    def _to_dto(db_task: TaskModel) -> TaskDto:
        return TaskDto(
            task_id=db_task.task_id,
            name=db_task.name,
            description=db_task.description,
            priority=db_task.priority,
            type_task=db_task.type_task,
            status=db_task.status,
            created_at=db_task.created_at,
            start_date=db_task.start_date,
            end_date=db_task.end_date,
            result=db_task.result or {},
            info=db_task.info or {},
        )

    async def create_task(self, task: TaskDto) -> TaskDto:
        db_task = TaskModel(**task.model_dump(exclude={"task_id"}))
        self.session.add(db_task)
        await self.session.flush()
        await self.session.refresh(db_task)
        return self._to_dto(db_task)

    async def get_tasks(self) -> list[TaskDto]:
        result = await self.session.execute(select(TaskModel))
        return [self._to_dto(db_task) for db_task in result.scalars().all()]

    async def get_task_by_id(self, task_id: int) -> TaskDto:
        result = await self.session.execute(
            select(TaskModel).where(TaskModel.task_id == task_id)
        )
        db_task = result.scalar_one_or_none()

        if db_task is None:
            raise TaskNotFoundError(f"Task {task_id} not found")

        return self._to_dto(db_task)

    async def delete_task(self, task_id: int) -> bool:
        result = await self.session.execute(
            select(TaskModel).where(TaskModel.task_id == task_id)
        )
        db_task = result.scalar_one_or_none()

        if db_task is None:
            raise TaskNotFoundError(f"Task {task_id} not found")

        db_task.status = TaskStatus.CANCELED
        await self.session.flush()
        return True

    async def get_task_status(self, task_id: int) -> TaskStatus:
        result = await self.session.execute(
            select(TaskModel.status).where(TaskModel.task_id == task_id)
        )
        status = result.scalar_one_or_none()

        if status is None:
            raise TaskNotFoundError(f"Task {task_id} not found")

        return status
