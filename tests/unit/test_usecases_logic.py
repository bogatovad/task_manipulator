from unittest.mock import AsyncMock

import pytest

from src.entities.task import TaskStatus, TypeTask
from src.usecases.usecases_logic.task import (
    ProcessCpuTasksUseCase,
    ProcessLllTasksUseCase,
    ProcessReadSharedMemoryUseCase,
)
from tests.fakes.cache import FakeTaskStatusCache
from tests.fakes.llm import FakeLlmGateway
from tests.fakes.repository import InMemoryTaskRepository, sample_task_dto


@pytest.mark.asyncio
async def test_process_llm_task_success(mocker) -> None:
    mocker.patch("src.usecases.usecases_logic.task.sleep", new_callable=AsyncMock)
    repository = InMemoryTaskRepository()
    cache = FakeTaskStatusCache()
    gateway = FakeLlmGateway(response={"answer": "done"})
    usecase = ProcessLllTasksUseCase(repository, gateway, cache)
    task = await repository.create_task(sample_task_dto(type_task=TypeTask.LLM))

    result = await usecase.execute(task)

    assert result is True
    assert gateway.calls == [task.description]
    stored = await repository.get_task_by_id(task.task_id)
    assert stored.status == TaskStatus.COMPLETED
    assert stored.result["result"] == {"answer": "done"}
    assert await cache.get_task_status(task.task_id) == TaskStatus.COMPLETED


@pytest.mark.asyncio
async def test_process_llm_task_failure(mocker) -> None:
    mocker.patch("src.usecases.usecases_logic.task.sleep", new_callable=AsyncMock)
    repository = InMemoryTaskRepository()
    cache = FakeTaskStatusCache()
    gateway = FakeLlmGateway(error=RuntimeError("llm down"))
    usecase = ProcessLllTasksUseCase(repository, gateway, cache)
    task = await repository.create_task(sample_task_dto(type_task=TypeTask.LLM))

    result = await usecase.execute(task)

    assert result is True
    stored = await repository.get_task_by_id(task.task_id)
    assert stored.status == TaskStatus.FAILED
    assert stored.info["error"] is True
    assert await cache.get_task_status(task.task_id) == TaskStatus.FAILED


@pytest.mark.asyncio
async def test_process_llm_task_caches_in_progress(mocker) -> None:
    mocker.patch("src.usecases.usecases_logic.task.sleep", new_callable=AsyncMock)
    repository = InMemoryTaskRepository()
    cache = FakeTaskStatusCache()
    set_calls: list[TaskStatus] = []

    original_set = cache.set_task_status

    async def track_set(task_id: int, status: TaskStatus) -> bool:
        set_calls.append(status)
        return await original_set(task_id, status)

    cache.set_task_status = track_set  # type: ignore[method-assign]
    gateway = FakeLlmGateway()
    usecase = ProcessLllTasksUseCase(repository, gateway, cache)
    task = await repository.create_task(sample_task_dto(type_task=TypeTask.LLM))

    await usecase.execute(task)

    assert TaskStatus.IN_PROGRESS in set_calls
    assert TaskStatus.COMPLETED in set_calls


@pytest.mark.asyncio
async def test_process_cpu_task(mocker) -> None:
    mocker.patch("src.usecases.usecases_logic.task.sleep", new_callable=AsyncMock)
    repository = InMemoryTaskRepository()
    cache = FakeTaskStatusCache()
    usecase = ProcessCpuTasksUseCase(repository, cache)
    task = await repository.create_task(sample_task_dto(type_task=TypeTask.CPU))

    result = await usecase.execute(task)

    assert result is True
    stored = await repository.get_task_by_id(task.task_id)
    assert stored.status == TaskStatus.COMPLETED
    assert stored.result["type_task"] == "ProcessCpuTasksUseCase"
    assert await cache.get_task_status(task.task_id) == TaskStatus.COMPLETED


@pytest.mark.asyncio
async def test_process_memory_task(mocker) -> None:
    mocker.patch("src.usecases.usecases_logic.task.sleep", new_callable=AsyncMock)
    repository = InMemoryTaskRepository()
    cache = FakeTaskStatusCache()
    usecase = ProcessReadSharedMemoryUseCase(repository, cache)
    task = await repository.create_task(sample_task_dto(type_task=TypeTask.MEMORY))

    result = await usecase.execute(task)

    assert result is True
    stored = await repository.get_task_by_id(task.task_id)
    assert stored.status == TaskStatus.COMPLETED
    assert stored.result["type_task"] == "ProcessReadSharedMemoryUseCase"
