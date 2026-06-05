from aio_pika import connect_robust
from aio_pika.abc import AbstractRobustConnection

from src.frameworks_and_drivers.queue_implementations.settings import rabbitmq_settings


async def get_rabbitmq_connection() -> AbstractRobustConnection:
    return await connect_robust(rabbitmq_settings.url)
