from os import path as os_path, remove as os_remove

from src.domain.event.RemoveDuplicatesEvent import RemoveDuplicatesEvent
from src.domain.event.LogActivityEvent import LogActivityEvent

from src.domain.repository.SettingsRepositoryInterface import SettingsRepositoryInterface

class DuplicateSearcher:
    def __init__(
            self, 
            settingsRepository: SettingsRepositoryInterface,
            logActivityEvent: LogActivityEvent,
            removeDuplicatesEvent: RemoveDuplicatesEvent
    ):
        self.settingsRepository = settingsRepository
        self.logActivityEvent = logActivityEvent
        self.removeDuplicatesEvent = removeDuplicatesEvent

    def compareFileBinaries(self, allFiles, fileLookedUp):
        fileSizeThreshold = self.settingsRepository.loadOne("binaryComparisonLargeFilesThreshold")

        for file in allFiles:
            if not os_path.isfile(file["fileFullPath"]):
                continue
            else:
                self.logActivityEvent.trigger("Comparing " + fileLookedUp["fileFullPath"] + " with " + file["fileFullPath"])

            if (
                (
                    self.__filesComparedAreNotTooLarge(file, fileLookedUp, fileSizeThreshold)
                    or self.settingsRepository.loadOne("binarySearchLargeFiles") == True
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