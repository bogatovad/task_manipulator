from fastapi import Request
from fastapi.responses import JSONResponse

from src.entities.exceptions import TaskNotFoundError


async def task_not_found_handler(
    request: Request,
    exc: TaskNotFoundError,
) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)},
    )
