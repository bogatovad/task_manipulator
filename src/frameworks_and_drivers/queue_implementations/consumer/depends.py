from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from src.frameworks_and_drivers.repositories_implementations.aync_sqlalchemy.database import (
    get_db_async_context_manager,
)
from src.frameworks_and_drivers.repositories_implementations.aync_sqlalchemy.task import (
    TaskSqlAlchemyRepository,
)
from src.interface_adapters.controllers.controllers_logic.controllers import (
    ProcessTaskController,
)
from src.interface_adapters.dtos.usecases import UsecaseDto
from src.usecases.usecases_logic.task import (
    ProcessCpuTasksUseCase,
    ProcessLllTasksUseCase,
    ProcessReadSharedMemoryUseCase,
)


def create_process_task_controller(session: AsyncSession) -> ProcessTaskController:
    repo = TaskSqlAlchemyRepository(session=session)
    return ProcessTaskController(
        UsecaseDto(
            process_read_shared_memory_usecase=ProcessReadSharedMemoryUseCase(repo),
            process_cpu_tasks_usecase=ProcessCpuTasksUseCase(repo),
            process_lll_tasks_usecase=ProcessLllTasksUseCase(repo),
        )
    )


async def task_controller_dependency() -> AsyncGenerator[ProcessTaskController]:
    async with get_db_async_context_manager() as session:
        yield create_process_task_controller(session)
