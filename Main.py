from os import path as os_path 
from sys import argv as sys_argv
from tkinter import Tk

from src.gui.SMSInterface import SMSInterface
from src.gui.view.SMSHomeView import SMSHomeView
from src.gui.view.SMSSettingsView import SMSSettingsView

from src.configuration.ServiceManager import ServiceManager
from src.configuration.ViewManager import ViewManager

from src.event.LogActivityEvent import LogActivityEvent
from src.event.DuplicateFoundEvent import DuplicateFoundEvent
from src.event.ChangeViewEvent import ChangeViewEvent
from src.event.FolderDeletedEvent import FolderDeletedEvent
from src.event.FileMovedEvent import FileMovedEvent

from src.entity.Settings import Settings

from src.service.FileLogger import FileLogger
from src.service.FileManagement import FileManagement
from src.service.FolderManagement import FolderManagement

class SortMyShit:
    def main(
        serviceManager: ServiceManager = ServiceManager(),
        viewManager: ViewManager = ViewManager()
    ):
        # At the moment, services need to be registered manually and in order of usage
        # @TODO: Implement service registration from a configuration file
        serviceManager.registerServices({
            "Settings": Settings,
            # Events
            "ChangeViewEvent": ChangeViewEvent,
            "DuplicateFoundEvent": DuplicateFoundEvent,
            "FileMovedEvent": FileMovedEvent,
            "FolderDeletedEvent": FolderDeletedEvent,
            "LogActivityEvent": LogActivityEvent,
            # Services
            "FileLogger": FileLogger,
            "FileManagement": FileManagement,
            "FolderManagement": FolderManagement,
        })

        serviceManager.get("FileLogger").activateLogging()
        serviceManager.get("Settings").runDir = os_path.dirname(os_path.abspath(sys_argv[0]))

        root = Tk()

        viewManager.registerViews({
            "home": SMSHomeView(root),
            "settings": SMSSettingsView(root)
        })

        SMSInterface(root)
        

if __name__ == "__main__":
    SortMyShit.main()