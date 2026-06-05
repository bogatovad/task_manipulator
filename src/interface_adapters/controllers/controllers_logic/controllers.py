from src.entities.task import TypeTask
from src.interface_adapters.dtos.task import TaskDto
from src.interface_adapters.dtos.usecases import UsecaseDto


class ProcessTaskController:
    def __init__(self, usecase: UsecaseDto):
        self.usecase: UsecaseDto = usecase

    async def run_task(self, task: TaskDto):
        if task.type_task == TypeTask.CPU:
            return await self.usecase.process_cpu_tasks_usecase.execute(task)
        if task.type_task == TypeTask.MEMORY:
            return await self.usecase.process_read_shared_memory_usecase.execute(task)
        if task.type_task == TypeTask.LLM:
            return await self.usecase.process_lll_tasks_usecase.execute(task)
        return None
