from os import system as os_system

from src.event.LogActivityEvent import LogActivityEvent
from src.event.SortFilesEvent import SortFilesEvent

from src.configuration.ServiceManager import ServiceManager

class FileSorter:
    def __init__(self, serviceManager: ServiceManager = ServiceManager()):
        self.sortFilesEvent = serviceManager.get("SortFilesEvent") # type: SortFilesEvent
        self.logActivityEvent = serviceManager.get("LogActivityEvent") # type: LogActivityEvent

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