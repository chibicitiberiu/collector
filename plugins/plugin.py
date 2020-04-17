from abc import ABC, abstractmethod
from typing import Tuple


class Plugin(ABC):
    models = []

    @abstractmethod
    def get_interval(self) -> int:
        pass

    @abstractmethod
    def execute(self) -> None:
        pass
