from datetime import UTC, datetime

from src.entities.exceptions import TaskNotFoundError
from src.entities.task import TaskPriority, TaskStatus, TypeTask
from src.interface_adapters.dtos.task import TaskDto, TasksPageDto
from src.interface_adapters.repositories_interfaces.task import TaskStorageInterface


class InMemoryTaskRepository(TaskStorageInterface):
    def __init__(self) -> None:
        self._tasks: dict[int, TaskDto] = {}
        self._next_id = 0

    async def create_task(self, task: TaskDto) -> TaskDto:
        self._next_id += 1
        created = task.model_copy(
            update={
                "task_id": self._next_id,
                "created_at": datetime.now(UTC),
            }
        )
        self._tasks[self._next_id] = created
        return created

    async def get_tasks(
        self,
        page: int,
        page_size: int,
        status: TaskStatus | None = None,
    ) -> TasksPageDto:
        items = list(self._tasks.values())
        if status is not None:
            items = [task for task in items if task.status == status]
        items.sort(
            key=lambda task: (
                task.created_at or datetime.min.replace(tzinfo=UTC),
                task.task_id or 0,
            ),
            reverse=True,
        )
        total = len(items)
        start = (page - 1) * page_size
        end = start + page_size
        return TasksPageDto(
            items=items[start:end],
            total=total,
            page=page,
            page_size=page_size,
        )

    async def get_task_by_id(self, task_id: int) -> TaskDto:
        task = self._tasks.get(task_id)
        if task is None:
            raise TaskNotFoundError(f"Task {task_id} not found")
        return task

    async def delete_task(self, task_id: int) -> bool:
        task = self._tasks.get(task_id)
        if task is None:
            raise TaskNotFoundError(f"Task {task_id} not found")
        self._tasks[task_id] = task.model_copy(update={"status": TaskStatus.CANCELED})
        return True

    async def get_task_status(self, task_id: int) -> TaskStatus:
        task = self._tasks.get(task_id)
        if task is None:
            raise TaskNotFoundError(f"Task {task_id} not found")
        return task.status

    async def update_task_start(self, task_id: int) -> TaskStatus:
        task = self._tasks.get(task_id)
        if task is None:
            raise TaskNotFoundError(f"Task {task_id} not found")
        self._tasks[task_id] = task.model_copy(
            update={
                "status": TaskStatus.IN_PROGRESS,
                "start_date": datetime.now(UTC),
            }
        )
        return TaskStatus.IN_PROGRESS

    async def update_task_end(
        self, task_id: int, result_task: dict, error_info: dict
    ) -> TaskStatus:
        task = self._tasks.get(task_id)
        if task is None:
            raise TaskNotFoundError(f"Task {task_id} not found")
        status = TaskStatus.FAILED if error_info != {} else TaskStatus.COMPLETED
        self._tasks[task_id] = task.model_copy(
            update={
                "status": status,
                "end_date": datetime.now(UTC),
                "result": result_task,
                "info": error_info,
            }
        )
        return status

    async def commit(self) -> bool:
        return True


def sample_task_dto(**overrides) -> TaskDto:
    data = {
        "name": "test-task",
        "description": "test description",
        "priority": TaskPriority.MEDIUM,
        "type_task": TypeTask.LLM,
        "status": TaskStatus.NEW,
    }
    data.update(overrides)
    return TaskDto(**data)
