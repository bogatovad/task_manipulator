from abc import abstractmethod
from typing import Any


class BaseUseCase:
    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    async def execute(self, *args, **kwargs) -> Any:
        raise NotImplementedError("Subclasses should implement this method")
