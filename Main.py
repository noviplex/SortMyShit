from os import path as os_path 
from sys import argv as sys_argv
from tkinter import Tk

from src.gui.SMSInterface import SMSInterface
from src.gui.SMSNavBar import SMSNavBar
from src.gui.view.SMSHomeView import SMSHomeView
from src.gui.view.SMSSettingsView import SMSSettingsView

from src.manager.ServiceManager import ServiceManager
from src.manager.ViewManager import ViewManager

from src.event.LogActivityEvent import LogActivityEvent
from src.event.RemoveDuplicatesEvent import RemoveDuplicatesEvent
from src.event.ChangeViewEvent import ChangeViewEvent
from src.event.RemoveEmptyFilesEvent import RemoveEmptyFilesEvent
from src.event.RemoveEmptyFoldersEvent import RemoveEmptyFoldersEvent
from src.event.SortFilesEvent import SortFilesEvent

from src.service.DuplicateSearcher import DuplicateSearcher
from src.service.FileLogger import FileLogger
from src.service.FileManager import FileManager
from src.service.FileSorter import FileSorter
from src.service.FolderManager import FolderManager
from src.service.SettingsService import SettingsService

class SortMyShit:
    def main():
        serviceManager = ServiceManager()
        viewManager = ViewManager()
        viewManager.setServiceManager(serviceManager)

        services = [
            SettingsService,
            ChangeViewEvent,
            RemoveDuplicatesEvent,
            SortFilesEvent,
            RemoveEmptyFilesEvent,
            RemoveEmptyFoldersEvent,
            LogActivityEvent,
            FileLogger,
            DuplicateSearcher,
            FileSorter,
            FileManager,
            FolderManager,
        ]

        serviceManager.registerServices(services)
        serviceManager.get("SettingsService").runDir = os_path.dirname(os_path.abspath(sys_argv[0]))
        serviceManager.get("FileLogger").activateLogging()

        root = Tk()

        viewManager.registerViews(root, {
            "navBar": SMSNavBar,
            "home": SMSHomeView,
            "settings": SMSSettingsView
        })

        SMSInterface(
            root,
            serviceManager.get("SettingsService"),
            serviceManager.get("ChangeViewEvent"),
            viewManager
        )


        

if __name__ == "__main__":
    SortMyShit.main()