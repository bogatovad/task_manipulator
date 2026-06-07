from src.entities.task import TaskStatus
from src.interface_adapters.cache_interfaces.task_status import TaskStatusCacheInterface


class FakeTaskStatusCache(TaskStatusCacheInterface):
    def __init__(self) -> None:
        self._store: dict[int, TaskStatus] = {}

    async def get_task_status(self, task_id: int) -> TaskStatus | None:
        return self._store.get(task_id)

    async def set_task_status(self, task_id: int, status: TaskStatus) -> bool:
        self._store[task_id] = status
        return True
