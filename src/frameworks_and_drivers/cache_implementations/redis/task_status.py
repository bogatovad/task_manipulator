from redis.asyncio.client import Redis

from src.entities.task import TaskStatus
from src.frameworks_and_drivers.cache_implementations.redis.settings import (
    redis_settings,
)
from src.interface_adapters.cache_interfaces.task_status import TaskStatusCacheInterface


class TaskStatusRedisCache(TaskStatusCacheInterface):
    def __init__(self, client: Redis) -> None:
        self.client = client
        self.ttl_seconds = redis_settings.status_ttl_seconds

    @staticmethod
    def _key(task_id: int) -> str:
        return f"task:status:{task_id}"

    async def get_task_status(self, task_id: int) -> TaskStatus | None:
        status = await self.client.get(self._key(task_id))

        if status is None:
            return None

        return TaskStatus(status)

    async def set_task_status(self, task_id: int, status: TaskStatus) -> None:
        await self.client.set(
            self._key(task_id),
            status.value,
            ex=self.ttl_seconds,
        )
