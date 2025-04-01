from os import system as os_system

from src.domain.event.LogActivityEvent import LogActivityEvent
from src.domain.event.SortFilesEvent import SortFilesEvent

class FileSorter:
    def __init__(self, sortFilesEvent: SortFilesEvent, logActivityEvent: LogActivityEvent):
        self.sortFilesEvent = sortFilesEvent
        self.logActivityEvent = logActivityEvent

    def moveFile(self, filesFullPath: str, categoryDestinationFolder: str):                    
        self.__moveOrCopyFile("rm", filesFullPath, categoryDestinationFolder)
        
    def copyFile(self, filesFullPath: str, categoryDestinationFolder: str):                    
        self.__moveOrCopyFile("cp", filesFullPath, categoryDestinationFolder)

    def __moveOrCopyFile(self, command: str, filesFullPath: str, categoryDestinationFolder: str):
        action = "copied" if command == "cp" else "moved"
        for fileFullPath in filesFullPath:
            
            os_system(command + " \"" + fileFullPath + "\" " + categoryDestinationFolder)
            self.sortFilesEvent.trigger(fileFullPath + " " + action + " successfully, now into " + categoryDestinationFolder)
            self.logActivityEvent.trigger(fileFullPath + " " + action + " successfully, now into " + categoryDestinationFolder)