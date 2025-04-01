from inspect import signature
from tkinter import Tk

from src.manager.ServiceManager import ServiceManager

from src.gui.view.SMSView import SMSView

class ViewManager:
    def __new__(viewManager):
        if not hasattr(viewManager, 'instance'):
            viewManager.instance = super(viewManager, viewManager).__new__(viewManager)
        return viewManager.instance

    def __init__(self):
        self.viewContainer = {}

    def setServiceManager(self, serviceManager: ServiceManager):
        self.serviceManager = serviceManager

    def get(self, viewName):
        return self.viewContainer[viewName]
    
    def registerView(self, mainContainer: Tk, viewName: str, view: SMSView):
        if viewName not in self.viewContainer:
            dependencies = signature(view).parameters

            viewDependencies = [mainContainer]
            for dependencyName in dependencies:
                if (dependencyName != "container"):
                    viewDependencies.append(self.serviceManager.get(dependencies[dependencyName].annotation.__name__))
            self.viewContainer[viewName] = view(*viewDependencies)

    def unregisterView(self, viewName):
        del self.viewContainer[viewName]

    def registerViews(self, mainContainer: Tk, views: dict[SMSView]):
        for viewName, view in views.items():
            self.registerView(mainContainer, viewName, view)