from dataclasses import dataclass

from src.usecases.usecases_api.task import (
    CreateTaskUseCase,
    GetTaskUseCase,
    GetTasksUseCase,
    DeleteTaskUseCase,
    GetStatusTaskUseCase,
)

from src.usecases.usecases_logic.task import (
    ProcessCpuTasksUseCase,
    ProcessLllTasksUseCase,
    ProcessReadSharedMemoryUseCase,
)


@dataclass
class UsecaseDto:
    create_task_usecase: CreateTaskUseCase | None = None
    get_tasks_usecase: GetTasksUseCase | None = None
    get_task_usecase: GetTaskUseCase | None = None
    delete_task_usecase: DeleteTaskUseCase | None = None
    get_status_usecase: GetStatusTaskUseCase | None = None
    process_cpu_tasks_usecase: ProcessCpuTasksUseCase | None = None
    process_lll_tasks_usecase: ProcessLllTasksUseCase | None = None
    process_read_shared_memory_usecase: ProcessReadSharedMemoryUseCase | None = None
