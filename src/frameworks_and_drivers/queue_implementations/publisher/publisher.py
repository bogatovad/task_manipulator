import aio_pika

from src.frameworks_and_drivers.queue_implementations.topology import setup_topology
from src.interface_adapters.dtos.task import TaskDto
from src.interface_adapters.queue_interfaces.publisher.publisher import (
    TaskQueuePublisherInterface,
)


class TaskRabbitMqQueue(TaskQueuePublisherInterface):
    async def publish(self, task: TaskDto) -> None:
        channel = await self.connection.channel()
        exchange = await setup_topology(channel)
        await exchange.publish(
            aio_pika.Message(
                body=task.model_dump_json().encode(),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
            ),
            routing_key=task.priority.value,
        )
        await channel.close()
