from src.interface_adapters.dtos.task import TaskDto


class TaskQueuePublisherInterface:
    def __init__(self, connection) -> None:
        self.connection = connection

    async def publish(self, task_id: TaskDto) -> None:
        pass
