from abc import ABC, abstractmethod


class EventManagerInterface(ABC):
    @abstractmethod
    def subscribe(self, eventName: str, listener: callable):
        pass

    @abstractmethod
    def trigger(self, eventName, *args, **kwargs):
        pass
