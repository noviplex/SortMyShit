from abc import ABC, abstractmethod
from typing import Callable


class EventManagerInterface(ABC):
    @abstractmethod
    def subscribe(self, event_name: str, listener: Callable):
        pass

    @abstractmethod
    def trigger(self, event_name: str, *args, **kwargs):
        pass
