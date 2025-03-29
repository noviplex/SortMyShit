from os import path as os_path, remove as os_remove

from src.event.RemoveDuplicatesEvent import RemoveDuplicatesEvent
from src.event.LogActivityEvent import LogActivityEvent

from src.configuration.ServiceManager import ServiceManager

from src.service.SettingsService import SettingsService

class DuplicateSearcher:
    def __init__(self, serviceManager: ServiceManager = ServiceManager()):
        self.settingsService = serviceManager.get("SettingsService") # type: SettingsService
        self.logActivityEvent = serviceManager.get("LogActivityEvent") # type: LogActivityEvent
        self.removeDuplicatesEvent = serviceManager.get("RemoveDuplicatesEvent") # type: RemoveDuplicatesEvent

    def compareFileBinaries(self, allFiles, fileLookedUp):
        fileSizeThreshold = self.settingsService.getSetting("binaryComparisonLargeFilesThreshold")

        for file in allFiles:
            if not os_path.isfile(file["fileFullPath"]):
                continue
            else:
                self.logActivityEvent.trigger("Comparing " + fileLookedUp["fileFullPath"] + " with " + file["fileFullPath"])

            if (
                (
                    self.__filesComparedAreNotTooLarge(file, fileLookedUp, fileSizeThreshold)
                    or self.settingsService.getSetting("binarySearchLargeFiles") == True
                )
                and fileLookedUp["fileFullPath"] != file["fileFullPath"]
                and fileLookedUp["filePartialContent"] == file["filePartialContent"]
            ):
                fileOpened = open(file["fileFullPath"], 'rb')
                fileLookedUpOpened = open(fileLookedUp["fileFullPath"], 'rb')

                if (fileOpened.read() == fileLookedUpOpened.read()):
                    os_remove(file["fileFullPath"])
                    self.__notifyDuplicateFound(file, fileLookedUp)
                fileOpened.close()
                fileLookedUpOpened.close()

    def compareFileNames(self, allFiles, fileLookedUp):
        for file in allFiles:
            self.logActivityEvent.trigger("Comparing " + fileLookedUp["fileFullPath"] + " with " + file["fileFullPath"])
            
            if (
                os_path.basename(fileLookedUp["fileFullPath"]) == os_path.basename(file["fileFullPath"]) 
                and fileLookedUp["fileFullPath"] != file["fileFullPath"]
            ):
                os_remove(file["fileFullPath"])
                self.__notifyDuplicateFound(file, fileLookedUp)
                break

    def __notifyDuplicateFound(self, file, fileLookedUp):
        self.removeDuplicatesEvent.trigger("Removed " + file["fileFullPath"] + " duplicate of " + fileLookedUp["fileFullPath"])
        self.logActivityEvent.trigger("Removed " + file["fileFullPath"] + " duplicate of " + fileLookedUp["fileFullPath"])

    def __filesComparedAreNotTooLarge(self, file, fileLookedUp, fileSizeThreshold):
            return (os_path.getsize(fileLookedUp["fileFullPath"]) < fileSizeThreshold 
                and os_path.getsize(file["fileFullPath"]) < fileSizeThreshold)