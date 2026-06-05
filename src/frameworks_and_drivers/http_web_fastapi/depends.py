from collections.abc import AsyncGenerator

from src.frameworks_and_drivers.queue_implementations.connection import (
    get_rabbitmq_connection,
)
from src.frameworks_and_drivers.queue_implementations.publisher.publisher import (
    TaskRabbitMqQueue,
)
from src.frameworks_and_drivers.repositories_implementations.aync_sqlalchemy.database import (
    get_db_async_context_manager,
)
from src.frameworks_and_drivers.repositories_implementations.aync_sqlalchemy.task import (
    TaskSqlAlchemyRepository,
)
from src.interface_adapters.controllers.task import TaskController
from src.interface_adapters.dtos.usecases import UsecaseDto
from src.usecases.task import (
    CreateTaskUseCase,
    GetTaskUseCase,
    GetStatusTaskUseCase,
    GetTasksUseCase,
    DeleteTaskUseCase,
)


async def task_controller_dependency() -> AsyncGenerator[TaskController]:
    rabbitmq_connection = await get_rabbitmq_connection()

    # todo: тут нужно вызвать rabbitmq_connection.close(). подумать где именно.
    async with get_db_async_context_manager() as session:
        task_sql_alchemy_repository = TaskSqlAlchemyRepository(session=session)
        queue = TaskRabbitMqQueue(connection=rabbitmq_connection)

        create_task_usecase = CreateTaskUseCase(
            task_repository=task_sql_alchemy_repository,
            queue=queue,
        )
        get_task_usecase = GetTaskUseCase(task_repository=task_sql_alchemy_repository)
        get_status_task_usecase = GetStatusTaskUseCase(
            task_repository=task_sql_alchemy_repository
        )
        get_tasks_usecase = GetTasksUseCase(task_repository=task_sql_alchemy_repository)
        delete_task_usecase = DeleteTaskUseCase(
            task_repository=task_sql_alchemy_repository
        )
        usecase_dto = UsecaseDto(
            create_task_usecase=create_task_usecase,
            get_task_usecase=get_task_usecase,
            get_status_usecase=get_status_task_usecase,
            delete_task_usecase=delete_task_usecase,
            get_tasks_usecase=get_tasks_usecase,
        )

        task_controller = TaskController(
            usecase=usecase_dto,
        )
        yield task_controller
