from src.interface_adapters.dtos.task import TaskDto
from src.interface_adapters.repositories_interfaces.task import TaskStorageInterface
from src.usecases.base import BaseUseCase


class ProcessLllTasksUseCase(BaseUseCase):
    def __init__(self, task_repository: TaskStorageInterface):
        self.task_repository = task_repository

    async def execute(self, task: TaskDto) -> bool:
        print("ProcessLllTasksUseCase")
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
