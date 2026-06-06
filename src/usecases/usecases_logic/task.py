from asyncio import sleep

from src.interface_adapters.dtos.task import TaskDto
from src.interface_adapters.repositories_interfaces.task import TaskStorageInterface
from src.usecases.base import BaseUseCase
from src.entities.task import TaskStatus


class ProcessLllTasksUseCase(BaseUseCase):
    def __init__(self, task_repository: TaskStorageInterface):
        self.task_repository = task_repository

    async def execute(self, task: TaskDto) -> bool:
        # todo: вот тут нужно 1) проставить время начала выполнения задачи
        # todo 2) обновить статус задачи в кэше
        await self.task_repository.update_task_status(
            task_id=task.task_id, status=TaskStatus.IN_PROGRESS
        )
        print("ProcessLllTasksUseCase")
        await sleep(5)
        await self.task_repository.update_task_status(
            task_id=task.task_id, status=TaskStatus.COMPLETED
        )
        return True


class ProcessCpuTasksUseCase(BaseUseCase):
    def __init__(self, task_repository: TaskStorageInterface):
        self.task_repository = task_repository

    async def execute(self, task: TaskDto) -> bool:
        print("ProcessCpuTasksUseCase")
        return True


class ProcessReadSharedMemoryUseCase(BaseUseCase):
    def __init__(self, task_repository: TaskStorageInterface):
        self.task_repository = task_repository

    async def execute(self, task: TaskDto) -> bool:
        print("ProcessReadSharedMemoryUseCase")
        return True
