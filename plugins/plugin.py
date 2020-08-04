from abc import ABC, abstractmethod
from typing import Tuple
import database


class Plugin(ABC):
    models = []

    @abstractmethod
    def get_interval(self) -> int:
        pass

    @abstractmethod
    def execute(self) -> None:
        pass

    def execute_wrapper(self) -> None:
        with database.DB.connection_context():
            self.execute()