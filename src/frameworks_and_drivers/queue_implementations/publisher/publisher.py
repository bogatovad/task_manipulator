import aio_pika

from src.frameworks_and_drivers.queue_implementations.settings import rabbitmq_settings
from src.interface_adapters.dtos.task import TaskDto
from src.interface_adapters.queue_interfaces.publisher.publisher import (
    TaskQueuePublisherInterface,
)


class TaskRabbitMqQueue(TaskQueuePublisherInterface):
    async def publish(self, task: TaskDto) -> None:
        # todo: сейчас на каждый http cоздается свой channel!
        channel = await self.connection.channel()
        await channel.declare_queue(rabbitmq_settings.queue_name, durable=True)
        await channel.default_exchange.publish(
            aio_pika.Message(
                body=task.model_dump_json().encode(),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
            ),
            routing_key=rabbitmq_settings.queue_name,
        )
        await channel.close()
