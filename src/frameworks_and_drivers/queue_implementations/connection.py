from aio_pika import connect_robust
from aio_pika.abc import AbstractRobustConnection

from src.frameworks_and_drivers.queue_implementations.settings import rabbitmq_settings

rabbitmq_connection: AbstractRobustConnection | None = None


async def init_rabbitmq_connection() -> AbstractRobustConnection:
    global rabbitmq_connection
    if rabbitmq_connection is None or rabbitmq_connection.is_closed:
        rabbitmq_connection = await connect_robust(rabbitmq_settings.url)
    return rabbitmq_connection


async def close_rabbitmq_connection() -> None:
    global rabbitmq_connection
    if rabbitmq_connection is not None and not rabbitmq_connection.is_closed:
        await rabbitmq_connection.close()
    rabbitmq_connection = None


def get_rabbitmq_connection() -> AbstractRobustConnection:
    if rabbitmq_connection is None or rabbitmq_connection.is_closed:
        raise RuntimeError("RabbitMQ connection is not initialized")
    return rabbitmq_connection
