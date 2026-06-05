from fastapi import Depends, FastAPI

from src.frameworks_and_drivers.http_web_fastapi.depends import (
    task_controller_dependency,
)
from src.interface_adapters.controllers.task import TaskController
from src.interface_adapters.dtos.task import TaskDto


app = FastAPI()


@app.get("/tasks/{task_id}")
async def get_task(
    task_controller: TaskController = Depends(task_controller_dependency),
):
    await task_controller.get_task()
    return {"Hello": "World"}


@app.get("/tasks")
async def get_tasks(
    task_controller: TaskController = Depends(task_controller_dependency),
):
    await task_controller.get_tasks()
    return {"Hello": "World"}


@app.get("/tasks/{task_id}/status")
async def get_task_status(
    task_controller: TaskController = Depends(task_controller_dependency),
):
    await task_controller.get_tasks()
    return {"Hello": "World"}


@app.post("/tasks", response_model=TaskDto)
async def create_task(
    task: TaskDto,
    task_controller: TaskController = Depends(task_controller_dependency),
) -> TaskDto:
    return await task_controller.create_task(task)


@app.delete("/tasks/{task_id}")
async def delete_task(
    task_controller: TaskController = Depends(task_controller_dependency),
):
    await task_controller.get_task()
    return {"Hello": "World"}
