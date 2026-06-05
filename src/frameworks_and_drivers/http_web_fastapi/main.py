from fastapi import Depends, FastAPI

from src.entities.exceptions import TaskNotFoundError
from src.entities.task import TaskStatus
from src.frameworks_and_drivers.http_web_fastapi.depends import (
    task_controller_dependency,
)
from src.frameworks_and_drivers.http_web_fastapi.exception_handlers import (
    task_not_found_handler,
)
from src.interface_adapters.controllers.task import TaskController
from src.interface_adapters.dtos.task import TaskDto


app = FastAPI()
app.add_exception_handler(TaskNotFoundError, task_not_found_handler)


@app.get("/tasks/{task_id}", response_model=TaskDto)
async def get_task(
    task_id: int,
    task_controller: TaskController = Depends(task_controller_dependency),
) -> TaskDto:
    return await task_controller.get_task(task_id)


@app.get("/tasks", response_model=list[TaskDto])
async def get_tasks(
    task_controller: TaskController = Depends(task_controller_dependency),
) -> list[TaskDto]:
    return await task_controller.get_tasks()


@app.get("/tasks/{task_id}/status", response_model=TaskStatus)
async def get_task_status(
    task_id: int,
    task_controller: TaskController = Depends(task_controller_dependency),
) -> TaskStatus:
    return await task_controller.get_status_task(task_id)


@app.post("/tasks", response_model=TaskDto)
async def create_task(
    task: TaskDto,
    task_controller: TaskController = Depends(task_controller_dependency),
) -> TaskDto:
    return await task_controller.create_task(task)


@app.delete("/tasks/{task_id}")
async def delete_task(
    task_id: int,
    task_controller: TaskController = Depends(task_controller_dependency),
) -> dict[str, bool]:
    await task_controller.delete_task(task_id)
    return {"success": True}
