from inspect import signature
from tkinter import Tk

from pysman.ServiceManager import ServiceManager

from src.application.view.SMSView import SMSView


class ViewManager:
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(ViewManager, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.view_container = {}

    def set_service_manager(self, service_manager: ServiceManager):
        self.service_manager = service_manager

    def get(self, view_name):
        return self.view_container[view_name]

    def register_view(self, main_container: Tk, view_name: str, view: SMSView):
        if view_name not in self.view_container:
            dependencies = signature(view).parameters

            view_dependencies = [main_container]
            for dependency_name in dependencies:
                if dependency_name != "container":
                    annotation = dependencies[dependency_name].annotation
                    view_dependencies.append(self.service_manager.get_service(annotation.__name__))
            self.view_container[view_name] = view(*view_dependencies)

    def unregister_view(self, view_name):
        del self.view_container[view_name]

    def register_views(self, main_container: Tk, views: dict[str, SMSView]):
        for view_name, view in views.items():
            self.register_view(main_container, view_name, view)
