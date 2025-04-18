from os import path as os_path
from sys import argv as sys_argv
from tkinter import Tk

from src.application.service.SMSRenderer import SMSRenderer
from src.application.view.SMSHomeView import SMSHomeView
from src.application.view.SMSSettingsView import SMSSettingsView
from src.application.service.EventManager import EventManager

from src.domain.service.DuplicateRemover import DuplicateRemover
from src.domain.service.FileManager import FileManager
from src.domain.service.FileSorter import FileSorter
from src.domain.service.EmptyFolderRemover import EmptyFolderRemover
from src.domain.service.BinaryComparator import BinaryComparator
from src.domain.service.FileNameComparator import FileNameComparator

from src.infrastructure.logger.LogFileLogger import LogFileLogger
from src.infrastructure.repository.SettingsRepository import SettingsRepository

from src.manager.ServiceManager import ServiceManager
from src.manager.ViewManager import ViewManager


class SortMyShit:
    def main():
        serviceManager = ServiceManager()
        viewManager = ViewManager()
        viewManager.setServiceManager(serviceManager)

        services = [
            EventManager,
            LogFileLogger,
            BinaryComparator,
            FileNameComparator,
            DuplicateRemover,
            FileSorter,
            FileManager,
            EmptyFolderRemover,
            SMSRenderer,
        ]

        serviceManager.registerAliases({
            "SettingsRepositoryInterface": SettingsRepository,
            "EventManagerInterface": EventManager,
        })
        serviceManager.registerServices(services)
        serviceManager.get("SettingsRepository").runDir = os_path.dirname(os_path.abspath(sys_argv[0]))
        serviceManager.get("LogFileLogger").activateLogging()

        root = Tk()

        viewManager.registerViews(root, {
            "home": SMSHomeView,
            "settings": SMSSettingsView
        })

        serviceManager.get("SMSRenderer").render(
            root,
            viewManager
        )

        root.mainloop()


if __name__ == "__main__":
    SortMyShit.main()
