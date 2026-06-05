import asyncio
import json
import logging

from aio_pika import connect_robust, IncomingMessage
from aio_pika.abc import AbstractConnection

from src.frameworks_and_drivers.queue_implementations.settings import rabbitmq_settings
from src.interface_adapters.queue_interfaces.consumer.consumer import (
    TaskQueueConsumerInterface,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TaskRabbitMqConsumer(TaskQueueConsumerInterface):
    def __init__(self, url: str, queue_name: str) -> None:
        super().__init__(url, queue_name)
        self.connection: AbstractConnection | None = None
        self.channel = None
        self.queue = None
        self.reconnect_delay = 1

    async def _connect(self) -> None:
        try:
            self.connection = await connect_robust(self.url)
            logger.info("Connected to RabbitMQ")
            self.channel = await self.connection.channel()
            await self.channel.set_qos(prefetch_count=1)
            self.queue = await self.channel.declare_queue(
                self.queue_name,
                durable=True,
                auto_delete=False,
            )
        except Exception as exc:
            logger.error(
                "Connection failed: %s. Retrying in %ss...",
                exc,
                self.reconnect_delay,
            )
            await asyncio.sleep(self.reconnect_delay)
            raise

    @staticmethod
    async def _process_message(message: IncomingMessage) -> None:
        async with message.process():
            payload = json.loads(message.body.decode())
            logger.info(f"Processing task {payload}")

    async def _start_consuming(self) -> None:
        async with self.queue.iterator() as queue_iter:
            async for message in queue_iter:
                await self._process_message(message)

    async def run(self) -> None:
        while True:
            try:
                await self._connect()
                await self._start_consuming()
            except Exception as exc:
                logger.error("Unexpected error: %s. Reconnecting...", exc)
            finally:
                if self.channel:
                    await self.channel.close()
                if self.connection:
                    await self.connection.close()
                await asyncio.sleep(self.reconnect_delay)


async def run_consumer() -> None:
    consumer = TaskRabbitMqConsumer(
        url=rabbitmq_settings.url,
        queue_name=rabbitmq_settings.queue_name,
    )
    await consumer.run()


if __name__ == "__main__":
    asyncio.run(run_consumer())
