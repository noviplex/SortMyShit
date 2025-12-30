from os import path as os_path, getcwd as os_getcwd
from sys import argv as sys_argv
from tkinter import Tk, PhotoImage

from src.application.service.SMSRenderer import SMSRenderer
from src.application.view.ConsoleView import ConsoleView
from src.application.view.SettingsView import SettingsView
from src.application.view.RemoveDuplicatesView import RemoveDuplicatesView
from src.application.view.RemoveEmptyFilesView import RemoveEmptyFilesView
from src.application.view.RemoveEmptyFoldersView import RemoveEmptyFoldersView
from src.application.view.SortFilesView import SortFilesView
from src.application.service.EventManager import EventManager

from src.domain.service.compare.CompareBinary import CompareBinary
from src.domain.service.compare.CompareFileName import CompareFileName
from src.domain.service.list.ListDuplicate import ListDuplicate
from src.domain.service.remove.RemoveDuplicate import RemoveDuplicate
from src.domain.service.remove.RemoveEmptyFolder import RemoveEmptyFolder
from src.domain.service.remove.RemoveEmptyFile import RemoveEmptyFile
from src.domain.service.sort.SortFile import SortFile

from src.infrastructure.logger.LogFileLogger import LogFileLogger
from src.infrastructure.repository.SettingsRepository import SettingsRepository
from src.infrastructure.repository.FileInfoRepository import FileInfoRepository
from src.infrastructure.repository.TmpStorageRepository import TmpStorageRepository

from pysman.ServiceManager import ServiceManager
from src.manager.ViewManager import ViewManager


class SortMyShit:
    def main():
        serviceManager = ServiceManager()
        viewManager = ViewManager()
        viewManager.set_service_manager(serviceManager)

        services = [
            EventManager,
            SettingsRepository,
            FileInfoRepository,
            TmpStorageRepository,
            LogFileLogger,
            CompareFileName,
            CompareBinary,
            SortFile,
            ListDuplicate,
            RemoveEmptyFolder,
            RemoveEmptyFile,
            RemoveDuplicate,
            SMSRenderer,
        ]

        serviceManager.register_aliases({
            "SettingsRepositoryInterface": SettingsRepository,
            "FileInfoRepositoryInterface": FileInfoRepository,
            "TmpStorageRepositoryInterface": TmpStorageRepository,
            "EventManagerInterface": EventManager,
        })
        serviceManager.register_services(services)
        serviceManager.get_service("SettingsRepository").runDir = os_path.dirname(os_path.abspath(sys_argv[0]))
        serviceManager.get_service("LogFileLogger").activate_logging()

        root = Tk()
        root.iconphoto(False, PhotoImage(file=os_getcwd() + '/src/application/assets/icon.png'))

        viewManager.register_views(root, {
            "settings": SettingsView,
            "remove_duplicates": RemoveDuplicatesView,
            "remove_empty_files": RemoveEmptyFilesView,
            "remove_empty_folders": RemoveEmptyFoldersView,
            "sort_files": SortFilesView,
            "console": ConsoleView,
        })

        serviceManager.get_service("SMSRenderer").render(
            root,
            viewManager
        )

        root.mainloop()


if __name__ == "__main__":
    SortMyShit.main()
