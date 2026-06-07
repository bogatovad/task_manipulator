from src.interface_adapters.dtos.task import TaskDto
from src.interface_adapters.queue_interfaces.publisher.publisher import (
    TaskQueuePublisherInterface,
)


class FakeTaskQueuePublisher(TaskQueuePublisherInterface):
    def __init__(self) -> None:
        self.published: list[TaskDto] = []

    async def publish(self, task: TaskDto) -> bool:
        self.published.append(task)
        return True
