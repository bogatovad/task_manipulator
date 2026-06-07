import pytest

from src.entities.exceptions import TaskNotFoundError
from src.entities.task import TaskPriority, TaskStatus, TypeTask
from src.frameworks_and_drivers.repositories_implementations.aync_sqlalchemy.task import (
    TaskSqlAlchemyRepository,
)
from tests.fakes.repository import sample_task_dto


@pytest.mark.asyncio
async def test_repository_create_and_get(
    task_repository: TaskSqlAlchemyRepository,
) -> None:
    created = await task_repository.create_task(sample_task_dto())
    await task_repository.commit()

    fetched = await task_repository.get_task_by_id(created.task_id)

    assert fetched.task_id == created.task_id
    assert fetched.name == "test-task"
    assert fetched.status == TaskStatus.NEW


@pytest.mark.asyncio
async def test_repository_get_tasks_with_pagination(
    task_repository: TaskSqlAlchemyRepository,
) -> None:
    for index in range(4):
        await task_repository.create_task(sample_task_dto(name=f"task-{index}"))
    await task_repository.commit()

    page = await task_repository.get_tasks(page=1, page_size=2)

    assert page.total == 4
    assert len(page.items) == 2


@pytest.mark.asyncio
async def test_repository_get_tasks_filter_by_status(
    task_repository: TaskSqlAlchemyRepository,
) -> None:
    await task_repository.create_task(sample_task_dto(name="new"))
    await task_repository.create_task(
        sample_task_dto(name="done", status=TaskStatus.COMPLETED)
    )
    await task_repository.commit()

    page = await task_repository.get_tasks(
        page=1, page_size=10, status=TaskStatus.COMPLETED
    )

    assert page.total == 1
    assert page.items[0].status == TaskStatus.COMPLETED


@pytest.mark.asyncio
async def test_repository_delete_marks_canceled(
    task_repository: TaskSqlAlchemyRepository,
) -> None:
    created = await task_repository.create_task(sample_task_dto())
    await task_repository.commit()

    await task_repository.delete_task(created.task_id)
    await task_repository.commit()

    status = await task_repository.get_task_status(created.task_id)
    assert status == TaskStatus.CANCELED


@pytest.mark.asyncio
async def test_repository_update_task_lifecycle(
    task_repository: TaskSqlAlchemyRepository,
) -> None:
    created = await task_repository.create_task(
        sample_task_dto(type_task=TypeTask.LLM, priority=TaskPriority.HIGH)
    )
    await task_repository.commit()

    start_status = await task_repository.update_task_start(created.task_id)
    await task_repository.commit()
    assert start_status == TaskStatus.IN_PROGRESS

    end_status = await task_repository.update_task_end(
        created.task_id,
        result_task={"result": {"ok": True}},
        error_info={},
    )
    await task_repository.commit()

    assert end_status == TaskStatus.COMPLETED
    task = await task_repository.get_task_by_id(created.task_id)
    assert task.result == {"result": {"ok": True}}
    assert task.start_date is not None
    assert task.end_date is not None


@pytest.mark.asyncio
async def test_repository_update_task_end_with_error(
    task_repository: TaskSqlAlchemyRepository,
) -> None:
    created = await task_repository.create_task(sample_task_dto())
    await task_repository.commit()

    status = await task_repository.update_task_end(
        created.task_id,
        result_task={"result": None},
        error_info={"error": True, "exception": "boom"},
    )
    await task_repository.commit()

    assert status == TaskStatus.FAILED


@pytest.mark.asyncio
async def test_repository_get_task_not_found(
    task_repository: TaskSqlAlchemyRepository,
) -> None:
    with pytest.raises(TaskNotFoundError, match="Task 123 not found"):
        await task_repository.get_task_by_id(123)
