from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from unittest.mock import AsyncMock

import pytest
from httpx import ASGITransport, AsyncClient

from src.frameworks_and_drivers.http_web_fastapi.depends import (
    task_controller_dependency,
)
from src.frameworks_and_drivers.http_web_fastapi.exception_handlers import (
    task_not_found_handler,
)
from src.entities.exceptions import TaskNotFoundError
from src.interface_adapters.controllers.controllers_api.controllers import (
    TaskController,
)
from src.interface_adapters.dtos.usecases import UsecaseDto
from src.usecases.usecases_api.task import (
    CreateTaskUseCase,
    DeleteTaskUseCase,
    GetStatusTaskUseCase,
    GetTaskUseCase,
    GetTasksUseCase,
)
from tests.fakes.cache import FakeTaskStatusCache
from tests.fakes.queue import FakeTaskQueuePublisher
from tests.fakes.repository import InMemoryTaskRepository


def build_task_controller(
    repository: InMemoryTaskRepository | None = None,
    queue: FakeTaskQueuePublisher | None = None,
    cache: FakeTaskStatusCache | None = None,
) -> TaskController:
    repository = repository or InMemoryTaskRepository()
    queue = queue or FakeTaskQueuePublisher()
    cache = cache if cache is not None else FakeTaskStatusCache()
    usecases = UsecaseDto(
        create_task_usecase=CreateTaskUseCase(repository, queue, cache),
        get_tasks_usecase=GetTasksUseCase(repository),
        get_task_usecase=GetTaskUseCase(repository),
        delete_task_usecase=DeleteTaskUseCase(repository, cache),
        get_status_usecase=GetStatusTaskUseCase(repository, cache),
    )
    return TaskController(usecases)


@pytest.fixture
def repository() -> InMemoryTaskRepository:
    return InMemoryTaskRepository()


@pytest.fixture
def queue() -> FakeTaskQueuePublisher:
    return FakeTaskQueuePublisher()


@pytest.fixture
def cache() -> FakeTaskStatusCache:
    return FakeTaskStatusCache()


@pytest.fixture
def task_controller(
    repository: InMemoryTaskRepository,
    queue: FakeTaskQueuePublisher,
    cache: FakeTaskStatusCache,
) -> TaskController:
    return build_task_controller(repository, queue, cache)


@pytest.fixture
async def api_client(task_controller: TaskController) -> AsyncIterator[AsyncClient]:
    from fastapi import Depends, FastAPI, Query

    from src.entities.task import TaskStatus
    from src.interface_adapters.dtos.task import TaskDto, TasksPageDto

    @asynccontextmanager
    async def empty_lifespan(_app: FastAPI):
        yield

    test_app = FastAPI(lifespan=empty_lifespan)
    test_app.add_exception_handler(TaskNotFoundError, task_not_found_handler)

    async def override_controller() -> AsyncIterator[TaskController]:
        yield task_controller

    test_app.dependency_overrides[task_controller_dependency] = override_controller

    @test_app.get("/tasks/{task_id}", response_model=TaskDto)
    async def get_task(
        task_id: int,
        controller: TaskController = Depends(task_controller_dependency),
    ) -> TaskDto:
        return await controller.get_task(task_id)

    @test_app.get("/tasks", response_model=TasksPageDto)
    async def get_tasks(
        page: int = Query(default=1, ge=1),
        page_size: int = Query(default=20, ge=1, le=100),
        status: TaskStatus | None = None,
        controller: TaskController = Depends(task_controller_dependency),
    ) -> TasksPageDto:
        return await controller.get_tasks(page=page, page_size=page_size, status=status)

    @test_app.get("/tasks/{task_id}/status", response_model=TaskStatus)
    async def get_task_status(
        task_id: int,
        controller: TaskController = Depends(task_controller_dependency),
    ) -> TaskStatus:
        return await controller.get_status_task(task_id)

    @test_app.post("/tasks", response_model=TaskDto)
    async def create_task(
        task: TaskDto,
        controller: TaskController = Depends(task_controller_dependency),
    ) -> TaskDto:
        return await controller.create_task(task)

    @test_app.delete("/tasks/{task_id}")
    async def delete_task(
        task_id: int,
        controller: TaskController = Depends(task_controller_dependency),
    ) -> dict[str, bool]:
        await controller.delete_task(task_id)
        return {"success": True}

    transport = ASGITransport(app=test_app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.fixture
def mock_rabbitmq(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "src.frameworks_and_drivers.queue_implementations.connection.init_rabbitmq_connection",
        AsyncMock(return_value=AsyncMock()),
    )
    monkeypatch.setattr(
        "src.frameworks_and_drivers.queue_implementations.connection.close_rabbitmq_connection",
        AsyncMock(),
    )


@pytest.fixture
def mock_redis(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "src.frameworks_and_drivers.cache_implementations.redis.connection.init_redis_connection",
        AsyncMock(return_value=AsyncMock()),
    )
    monkeypatch.setattr(
        "src.frameworks_and_drivers.cache_implementations.redis.connection.close_redis_connection",
        AsyncMock(),
    )
