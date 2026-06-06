from src.entities.task import TaskStatus
from src.interface_adapters.cache_interfaces.task_status import TaskStatusCacheInterface
from src.interface_adapters.dtos.task import TaskDto
from src.interface_adapters.queue_interfaces.publisher.publisher import (
    TaskQueuePublisherInterface,
)
from src.interface_adapters.repositories_interfaces.task import TaskStorageInterface
from src.usecases.base import BaseUseCase


class CreateTaskUseCase(BaseUseCase):
    def __init__(
        self,
        task_repository: TaskStorageInterface,
        queue: TaskQueuePublisherInterface,
        status_cache: TaskStatusCacheInterface | None = None,
    ):
        self.task_repository = task_repository
        self.queue = queue
        self.status_cache = status_cache

    async def execute(self, task: TaskDto) -> TaskDto:
        created_task = await self.task_repository.create_task(task)
        await self.queue.publish(created_task)
        if self.status_cache is not None:
            await self.status_cache.set_task_status(
                created_task.task_id, created_task.status
            )
        return created_task


class GetTasksUseCase(BaseUseCase):
    def __init__(self, task_repository: TaskStorageInterface):
        self.task_repository = task_repository

    async def execute(self) -> list[TaskDto]:
        return await self.task_repository.get_tasks()


class GetTaskUseCase(BaseUseCase):
    def __init__(self, task_repository: TaskStorageInterface):
        self.task_repository = task_repository

    async def execute(self, task_id: int) -> TaskDto:
        return await self.task_repository.get_task_by_id(task_id)


class DeleteTaskUseCase(BaseUseCase):
    def __init__(
        self,
        task_repository: TaskStorageInterface,
        status_cache: TaskStatusCacheInterface | None = None,
    ):
        self.task_repository = task_repository
        self.status_cache = status_cache

    async def execute(self, task_id: int) -> bool:
        result = await self.task_repository.delete_task(task_id)

        if self.status_cache is not None:
            await self.status_cache.set_task_status(task_id, TaskStatus.CANCELED)

        return result


class GetStatusTaskUseCase(BaseUseCase):
    def __init__(
        self,
        task_repository: TaskStorageInterface,
        status_cache: TaskStatusCacheInterface | None = None,
    ):
        self.task_repository = task_repository
        self.status_cache = status_cache

    async def execute(self, task_id: int) -> TaskStatus:
        if self.status_cache is not None:
            cached_status = await self.status_cache.get_task_status(task_id)

            if cached_status is not None:
                return cached_status

        status = await self.task_repository.get_task_status(task_id)

        if self.status_cache is not None:
            await self.status_cache.set_task_status(task_id, status)

        return status
