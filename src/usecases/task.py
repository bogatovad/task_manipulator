from src.entities.task import TaskStatus
from src.interface_adapters.dtos.task import TaskDto
from src.interface_adapters.repositories_interfaces.task import TaskStorageInterface
from src.usecases.base import BaseUseCase


class CreateTaskUseCase(BaseUseCase):
    def __init__(self, task_repository: TaskStorageInterface):
        self.task_repository = task_repository

    async def execute(self, task: TaskDto) -> TaskDto:
        await self.task_repository.create_task(task)
        return task


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
    def __init__(self, task_repository: TaskStorageInterface):
        self.task_repository = task_repository

    async def execute(self, task_id: int) -> bool:
        return await self.task_repository.delete_task(task_id)


class GetStatusTaskUseCase(BaseUseCase):
    def __init__(self, task_repository: TaskStorageInterface):
        self.task_repository = task_repository

    async def execute(self, task_id: int) -> TaskStatus:
        return await self.task_repository.get_task_status(task_id)
