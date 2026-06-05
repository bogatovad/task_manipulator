from src.interface_adapters.dtos.task import TaskDto
from src.entities.task import TaskStatus


# todo: подумать от чего лучше стоит наследоваться. пока оставлю так.
class TaskStorageInterface:
    async def create_task(self, task: TaskDto) -> bool:
        pass

    async def get_tasks(self) -> list[TaskDto]:
        pass

    async def get_task_by_id(self, task_id: int) -> TaskDto:
        pass

    async def delete_task(self, task_id: int) -> bool:
        pass

    async def get_task_status(self, task_id: int) -> TaskStatus:
        pass
