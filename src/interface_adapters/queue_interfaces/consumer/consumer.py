from collections.abc import AsyncGenerator, Callable

from src.interface_adapters.controllers.controllers_logic.controllers import (
    ProcessTaskController,
)


class TaskQueueConsumerInterface:
    def __init__(
        self,
        url: str,
        queue_name: str,
        get_controller: Callable[[], AsyncGenerator[ProcessTaskController]],
    ) -> None:
        self.url = url
        self.queue_name = queue_name
        self.get_controller = get_controller

    def run(self):
        pass
