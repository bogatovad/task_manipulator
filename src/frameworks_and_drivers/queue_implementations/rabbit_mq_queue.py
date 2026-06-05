from src.interface_adapters.dtos.task import TaskDto
from src.interface_adapters.queue_interfaces.queue import TaskQueueInterface


class TaskRabbitMqQueue(TaskQueueInterface):
    async def publish(self, task: TaskDto) -> None:
        print(f"publishing task {task}")
