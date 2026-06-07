import pytest

from src.entities.task import TaskStatus
from src.usecases.usecases_api.task import (
    CreateTaskUseCase,
    DeleteTaskUseCase,
    GetStatusTaskUseCase,
    GetTaskUseCase,
    GetTasksUseCase,
)
from tests.fakes.cache import FakeTaskStatusCache
from tests.fakes.queue import FakeTaskQueuePublisher
from tests.fakes.repository import InMemoryTaskRepository, sample_task_dto


@pytest.mark.asyncio
async def test_create_task_usecase_publishes_and_caches() -> None:
    repository = InMemoryTaskRepository()
    queue = FakeTaskQueuePublisher()
    cache = FakeTaskStatusCache()
    usecase = CreateTaskUseCase(repository, queue, cache)

    created = await usecase.execute(sample_task_dto())

    assert created.task_id == 1
    assert len(queue.published) == 1
    assert await cache.get_task_status(1) == TaskStatus.NEW


@pytest.mark.asyncio
async def test_create_task_usecase_without_cache() -> None:
    repository = InMemoryTaskRepository()
    queue = FakeTaskQueuePublisher()
    usecase = CreateTaskUseCase(repository, queue, status_cache=None)

    created = await usecase.execute(sample_task_dto())

    assert created.task_id == 1
    assert len(queue.published) == 1


@pytest.mark.asyncio
async def test_get_tasks_usecase_returns_page() -> None:
    repository = InMemoryTaskRepository()
    usecase = GetTasksUseCase(repository)
    for index in range(5):
        await repository.create_task(sample_task_dto(name=f"task-{index}"))

    page = await usecase.execute(page=2, page_size=2)

    assert page.total == 5
    assert page.page == 2
    assert page.page_size == 2
    assert len(page.items) == 2


@pytest.mark.asyncio
async def test_get_task_usecase() -> None:
    repository = InMemoryTaskRepository()
    usecase = GetTaskUseCase(repository)
    created = await repository.create_task(sample_task_dto())

    task = await usecase.execute(created.task_id)

    assert task.task_id == created.task_id


@pytest.mark.asyncio
async def test_delete_task_usecase_updates_cache() -> None:
    repository = InMemoryTaskRepository()
    cache = FakeTaskStatusCache()
    usecase = DeleteTaskUseCase(repository, cache)
    created = await repository.create_task(sample_task_dto())

    result = await usecase.execute(created.task_id)

    assert result is True
    assert await cache.get_task_status(created.task_id) == TaskStatus.CANCELED


@pytest.mark.asyncio
async def test_get_status_usecase_reads_cache_first() -> None:
    repository = InMemoryTaskRepository()
    cache = FakeTaskStatusCache()
    usecase = GetStatusTaskUseCase(repository, cache)
    created = await repository.create_task(sample_task_dto())
    await cache.set_task_status(created.task_id, TaskStatus.IN_PROGRESS)

    status = await usecase.execute(created.task_id)

    assert status == TaskStatus.IN_PROGRESS


@pytest.mark.asyncio
async def test_get_status_usecase_populates_cache_on_miss() -> None:
    repository = InMemoryTaskRepository()
    cache = FakeTaskStatusCache()
    usecase = GetStatusTaskUseCase(repository, cache)
    created = await repository.create_task(sample_task_dto(status=TaskStatus.PENDING))

    status = await usecase.execute(created.task_id)

    assert status == TaskStatus.PENDING
    assert await cache.get_task_status(created.task_id) == TaskStatus.PENDING
