from abc import ABC, abstractmethod
from typing import Tuple


class Plugin(ABC):
    models = []

    @abstractmethod
    def execute(self) -> None:
        pass
