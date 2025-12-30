from src.domain.event.EventManagerInterface import EventManagerInterface


class EventManager(EventManagerInterface):
    def __init__(self):
        self.listeners = {}

    def subscribe(self, event_name: str, listener: callable):
        if event_name not in self.listeners:
            self.listeners[event_name] = []
        self.listeners[event_name].append(listener)

    def trigger(self, event_name, *args, **kwargs):
        for listener in self.listeners.get(event_name, []):
            listener(*args, **kwargs)
