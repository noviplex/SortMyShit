from os import system as os_system

from src.domain.event.EventManagerInterface import EventManagerInterface


class FileSorter:
    def __init__(
        self,
        eventManager: EventManagerInterface,
    ):
        self.eventManager = eventManager

    def moveFile(self, filesFullPath: str, categoryDestinationFolder: str):
        self.__moveOrCopyFile("rm", filesFullPath, categoryDestinationFolder)

    def copyFile(self, filesFullPath: str, categoryDestinationFolder: str):
        self.__moveOrCopyFile("cp", filesFullPath, categoryDestinationFolder)

    def __moveOrCopyFile(self, command: str, filesFullPath: str, categoryDestinationFolder: str):
        action = "copied" if command == "cp" else "moved"
        for fileFullPath in filesFullPath:

            os_system(command + " \"" + fileFullPath + "\" " + categoryDestinationFolder)
            self.eventManager.trigger("output", fileFullPath + " " + action + " successfully, now into " + categoryDestinationFolder)
