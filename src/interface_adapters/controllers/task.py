from src.entities.task import TaskStatus
from src.interface_adapters.dtos.task import TaskDto
from src.interface_adapters.dtos.usecases import UsecaseDto


class TaskController:
    def __init__(self, usecase: UsecaseDto):
        self.usecase: UsecaseDto = usecase

    async def create_task(self, task: TaskDto) -> TaskDto:
        return await self.usecase.create_task_usecase.execute(task)

    async def delete_task(self, task_id: int) -> bool:
        return await self.usecase.delete_task_usecase.execute(task_id)

    async def get_task(self, task_id: int) -> TaskDto:
        return await self.usecase.get_task_usecase.execute(task_id)

    async def get_tasks(self) -> list[TaskDto]:
        return await self.usecase.get_tasks_usecase.execute()

    async def get_status_task(self, task_id: int) -> TaskStatus:
        return await self.usecase.get_status_usecase.execute(task_id)
