import pytest
from httpx import AsyncClient

from src.entities.task import TaskStatus
from tests.fakes.repository import sample_task_dto


@pytest.mark.asyncio
async def test_create_task(api_client: AsyncClient, queue) -> None:
    payload = sample_task_dto().model_dump(mode="json")

    response = await api_client.post("/tasks", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert body["task_id"] == 1
    assert body["name"] == "test-task"
    assert body["status"] == TaskStatus.NEW
    assert len(queue.published) == 1
    assert queue.published[0].task_id == 1


@pytest.mark.asyncio
async def test_get_task(api_client: AsyncClient, task_controller) -> None:
    created = await task_controller.create_task(sample_task_dto())

    response = await api_client.get(f"/tasks/{created.task_id}")

    assert response.status_code == 200
    assert response.json()["task_id"] == created.task_id
    assert response.json()["name"] == created.name


@pytest.mark.asyncio
async def test_get_task_not_found(api_client: AsyncClient) -> None:
    response = await api_client.get("/tasks/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Task 999 not found"


@pytest.mark.asyncio
async def test_get_tasks_pagination(api_client: AsyncClient, task_controller) -> None:
    for index in range(3):
        await task_controller.create_task(
            sample_task_dto(name=f"task-{index}", status=TaskStatus.NEW)
        )

    response = await api_client.get("/tasks", params={"page": 1, "page_size": 2})

    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 3
    assert body["page"] == 1
    assert body["page_size"] == 2
    assert len(body["items"]) == 2


@pytest.mark.asyncio
async def test_get_tasks_filter_by_status(
    api_client: AsyncClient, task_controller
) -> None:
    await task_controller.create_task(sample_task_dto(name="new-task"))
    completed = await task_controller.create_task(
        sample_task_dto(name="completed-task", status=TaskStatus.COMPLETED)
    )

    response = await api_client.get(
        "/tasks",
        params={"status": TaskStatus.COMPLETED.value},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 1
    assert body["items"][0]["task_id"] == completed.task_id


@pytest.mark.asyncio
async def test_get_task_status_from_cache(
    api_client: AsyncClient, task_controller, cache
) -> None:
    created = await task_controller.create_task(sample_task_dto())
    await cache.set_task_status(created.task_id, TaskStatus.IN_PROGRESS)

    response = await api_client.get(f"/tasks/{created.task_id}/status")

    assert response.status_code == 200
    assert response.json() == TaskStatus.IN_PROGRESS.value


@pytest.mark.asyncio
async def test_get_task_status_not_found(api_client: AsyncClient) -> None:
    response = await api_client.get("/tasks/404/status")

    assert response.status_code == 404
    assert response.json()["detail"] == "Task 404 not found"


@pytest.mark.asyncio
async def test_delete_task(api_client: AsyncClient, task_controller, cache) -> None:
    created = await task_controller.create_task(sample_task_dto())

    response = await api_client.delete(f"/tasks/{created.task_id}")

    assert response.status_code == 200
    assert response.json() == {"success": True}
    assert await cache.get_task_status(created.task_id) == TaskStatus.CANCELED


@pytest.mark.asyncio
async def test_delete_task_not_found(api_client: AsyncClient) -> None:
    response = await api_client.delete("/tasks/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Task 999 not found"


@pytest.mark.asyncio
async def test_create_task_validation_error(api_client: AsyncClient) -> None:
    response = await api_client.post(
        "/tasks",
        json={
            "name": "broken",
            "description": "missing required fields",
        },
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_tasks_invalid_page_size(api_client: AsyncClient) -> None:
    response = await api_client.get("/tasks", params={"page_size": 101})

    assert response.status_code == 422
