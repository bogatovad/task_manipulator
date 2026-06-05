from fastapi import FastAPI, Depends
from src.frameworks_and_drivers.http_web_fastapi.depends import (
    task_controller_dependency,
)
from src.interface_adapters.controllers.task import TaskController


app = FastAPI()


@app.get("/task")
async def get_task(
    task_controller: TaskController = Depends(task_controller_dependency),
):
    await task_controller.get_task()
    return {"Hello": "World"}


@app.get("/task")
async def get_tasks(
    task_controller: TaskController = Depends(task_controller_dependency),
):
    await task_controller.get_tasks()
    return {"Hello": "World"}


@app.post("/task")
async def create_task(
    task_controller: TaskController = Depends(task_controller_dependency),
):
    await task_controller.create_task()
    return {"Hello": "World"}
