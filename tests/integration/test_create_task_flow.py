import pytest

from src.entities.task import TaskStatus
from src.usecases.usecases_api.task import CreateTaskUseCase, GetStatusTaskUseCase
from tests.fakes.cache import FakeTaskStatusCache
from tests.fakes.queue import FakeTaskQueuePublisher
from tests.fakes.repository import sample_task_dto


@pytest.mark.asyncio
async def test_create_task_end_to_end_with_sqlalchemy(
    task_repository,
) -> None:
    queue = FakeTaskQueuePublisher()
    cache = FakeTaskStatusCache()
    create_usecase = CreateTaskUseCase(task_repository, queue, cache)
    status_usecase = GetStatusTaskUseCase(task_repository, cache)

    created = await create_usecase.execute(sample_task_dto())
    await task_repository.commit()

    assert created.task_id is not None
    assert len(queue.published) == 1
    assert queue.published[0].task_id == created.task_id

    status = await status_usecase.execute(created.task_id)
    assert status == TaskStatus.NEW

    db_task = await task_repository.get_task_by_id(created.task_id)
    assert db_task.name == "test-task"
