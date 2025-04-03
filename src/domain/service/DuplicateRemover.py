from os import path as os_path, remove as os_remove

from src.domain.entity.FileInfo import FileInfo
from src.domain.event.RemoveDuplicatesEvent import RemoveDuplicatesEvent
from src.domain.event.LogActivityEvent import LogActivityEvent
from src.domain.service.BinaryComparator import BinaryComparator
from src.domain.service.FileNameComparator import FileNameComparator
from src.domain.repository.SettingsRepositoryInterface import SettingsRepositoryInterface

class DuplicateRemover:
    def __init__(
            self, 
            logActivityEvent: LogActivityEvent,
            removeDuplicatesEvent: RemoveDuplicatesEvent,
            binaryComparator: BinaryComparator,
            fileNameComparator: FileNameComparator,
            settingsRepository: SettingsRepositoryInterface,
    ):
        self.logActivityEvent = logActivityEvent
        self.removeDuplicatesEvent = removeDuplicatesEvent
        self.binaryComparator = binaryComparator
        self.fileNameComparator = fileNameComparator
        self.settingsRepository = settingsRepository

    def removeFilesByIdenticalBinaryContent(self, allFiles: list[FileInfo], fileLookedUp: FileInfo):
        for file in allFiles:
            if not os_path.isfile(file.fullPath):
                continue

            if self.__filesMatchRequiredSize(file, fileLookedUp) == True:
                if self.binaryComparator.compare(file, fileLookedUp) == True:
                    self.__removeFile(file, fileLookedUp)
                    break

    def removeFilesByIdenticalFileName(self, allFiles: list[FileInfo], fileLookedUp: FileInfo):
        for file in allFiles:
            if self.fileNameComparator.compare(file, fileLookedUp) == True:
                self.__removeFile(file, fileLookedUp)
                break

    def __notifyDuplicateFound(self, file: FileInfo, fileLookedUp: FileInfo):
        self.removeDuplicatesEvent.trigger("Removed " + file.fullPath + " duplicate of " + fileLookedUp.fullPath)
        self.logActivityEvent.trigger("Removed " + file.fullPath + " duplicate of " + fileLookedUp.fullPath)

    def __filesMatchRequiredSize(self, file: FileInfo, fileLookedUp: FileInfo):
            return (
                self.__filesComparedAreNotTooLarge(file, fileLookedUp)
                or self.settingsRepository.loadOne("binarySearchLargeFiles") == True
            )

    def __filesComparedAreNotTooLarge(self, file: FileInfo, fileLookedUp: FileInfo):
            fileSizeThreshold = self.settingsRepository.loadOne("binaryComparisonLargeFilesThreshold")

            return (
                os_path.getsize(fileLookedUp.fullPath) < fileSizeThreshold 
                and os_path.getsize(file.fullPath) < fileSizeThreshold
            )

    def __removeFile(self, file, fileLookedUp):
        os_remove(file.fullPath)
        self.__notifyDuplicateFound(file, fileLookedUp)
