import asyncio
import json
import logging

from aio_pika import connect_robust, IncomingMessage
from aio_pika.abc import AbstractConnection

from src.frameworks_and_drivers.queue_implementations.settings import (
    RABBITMQ_QUEUE_NAME,
    RABBITMQ_URL,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# todo: подумать про интерфейс, возможно стоит создать абстрацию консюмера, так как крутить можно кафку\ребит\натс
class RabbitMQConsumer:
    def __init__(self, rabbitmq_url: str, queue_name: str):
        self.rabbitmq_url = rabbitmq_url
        self.queue_name = queue_name
        self.connection: AbstractConnection | None = None
        self.channel = None
        self.queue = None
        self.reconnect_delay = 1
        self.max_reconnect_delay = 30

    async def connect(self) -> None:
        try:
            self.connection = await connect_robust(self.rabbitmq_url)
            logger.info("Connected to RabbitMQ")

            self.channel = await self.connection.channel()
            await self.channel.set_qos(prefetch_count=1)

            self.queue = await self.channel.declare_queue(
                self.queue_name,
                durable=True,
                auto_delete=False,
            )
            self.reconnect_delay = 1
        except Exception as exc:
            logger.error(
                "Connection failed: %s. Retrying in %ss...",
                exc,
                self.reconnect_delay,
            )
            await asyncio.sleep(self.reconnect_delay)
            self.reconnect_delay = min(
                self.reconnect_delay * 2, self.max_reconnect_delay
            )
            raise

    async def process_message(self, message: IncomingMessage) -> None:
        async with message.process():
            payload = json.loads(message.body.decode())
            logger.info(f"Processing task {payload}")
            # todo: тут сделать обработку события

    async def start_consuming(self) -> None:
        async with self.queue.iterator() as queue_iter:
            async for message in queue_iter:
                await self.process_message(message)

    async def run(self) -> None:
        while True:
            try:
                await self.connect()
                await self.start_consuming()
            except Exception as exc:
                logger.error("Unexpected error: %s. Reconnecting...", exc)
            finally:
                if self.channel:
                    await self.channel.close()
                if self.connection:
                    await self.connection.close()
                await asyncio.sleep(self.reconnect_delay)
                self.reconnect_delay = min(
                    self.reconnect_delay * 2,
                    self.max_reconnect_delay,
                )


async def run_consumer() -> None:
    consumer = RabbitMQConsumer(
        rabbitmq_url=RABBITMQ_URL,
        queue_name=RABBITMQ_QUEUE_NAME,
    )
    await consumer.run()
