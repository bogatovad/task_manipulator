from src.interface_adapters.dtos.task import TaskDto


class TaskQueueInterface:
    async def publish(self, task_id: TaskDto) -> None:
        pass
