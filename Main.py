from os import path as os_path 
from sys import argv as sys_argv
from tkinter import Tk

from src.gui.SMSInterface import SMSInterface
from src.gui.view.SMSHomeView import SMSHomeView
from src.gui.view.SMSSettingsView import SMSSettingsView

from src.configuration.ServiceManager import ServiceManager
from src.configuration.ViewManager import ViewManager

from src.event.LogActivityEvent import LogActivityEvent
from src.event.RemoveDuplicatesEvent import RemoveDuplicatesEvent
from src.event.ChangeViewEvent import ChangeViewEvent
from src.event.DeleteEmptyFoldersEvent import DeleteEmptyFoldersEvent
from src.event.SortFilesEvent import SortFilesEvent

from src.service.DuplicateSearcher import DuplicateSearcher
from src.service.FileLogger import FileLogger
from src.service.FileManager import FileManager
from src.service.FileSorter import FileSorter
from src.service.FolderManager import FolderManager
from src.service.SettingsService import SettingsService

class SortMyShit:
    def main(
        serviceManager: ServiceManager = ServiceManager(),
        viewManager: ViewManager = ViewManager()
    ):
        # At the moment, services need to be registered manually and in order of usage
        # @TODO: Implement service registration from a configuration file
        serviceManager.registerService("SettingsService", SettingsService)
        serviceManager.get("SettingsService").runDir = os_path.dirname(os_path.abspath(sys_argv[0]))
        
        serviceManager.registerServices({
            "ChangeViewEvent": ChangeViewEvent,
            "RemoveDuplicatesEvent": RemoveDuplicatesEvent,
            "SortFilesEvent": SortFilesEvent,
            "DeleteEmptyFoldersEvent": DeleteEmptyFoldersEvent,
            "LogActivityEvent": LogActivityEvent,
            "FileLogger": FileLogger,
            "DuplicateSearcher": DuplicateSearcher,
            "FileSorter": FileSorter,
            "FileManager": FileManager,
            "FolderManager": FolderManager,
        })

        serviceManager.get("FileLogger").activateLogging()

        root = Tk()

        viewManager.registerViews({
            "home": SMSHomeView(root),
            "settings": SMSSettingsView(root)
        })

        SMSInterface(root)
        

if __name__ == "__main__":
    SortMyShit.main()