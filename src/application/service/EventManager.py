from src.domain.event.EventManagerInterface import EventManagerInterface


class EventManager(EventManagerInterface):
    def __init__(self):
        self.listeners = {}

    def subscribe(self, eventName: str, listener: callable):
        if eventName not in self.listeners:
            self.listeners[eventName] = []
        self.listeners[eventName].append(listener)

    def trigger(self, eventName, *args, **kwargs):
        for listener in self.listeners[eventName]:
            listener(*args, **kwargs)
