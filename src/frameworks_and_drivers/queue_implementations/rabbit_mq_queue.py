import aio_pika
from aio_pika.abc import AbstractRobustConnection

from src.frameworks_and_drivers.queue_implementations.settings import (
    RABBITMQ_QUEUE_NAME,
)
from src.interface_adapters.dtos.task import TaskDto
from src.interface_adapters.queue_interfaces.queue import TaskQueueInterface


class TaskRabbitMqQueue(TaskQueueInterface):
    def __init__(self, connection: AbstractRobustConnection) -> None:
        self.connection = connection

    async def publish(self, task: TaskDto) -> None:
        # todo: сейчас на каждый http осздается свой channel!
        channel = await self.connection.channel()
        await channel.declare_queue(RABBITMQ_QUEUE_NAME, durable=True)
        await channel.default_exchange.publish(
            aio_pika.Message(
                body=task.model_dump_json().encode(),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
            ),
            routing_key=RABBITMQ_QUEUE_NAME,
        )
        await channel.close()
