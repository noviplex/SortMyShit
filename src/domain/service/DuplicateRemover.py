from os import path as os_path, remove as os_remove

from src.domain.entity.FileInfo import FileInfo
from src.domain.event.EventManagerInterface import EventManagerInterface
from src.domain.service.BinaryComparator import BinaryComparator
from src.domain.service.FileNameComparator import FileNameComparator
from src.domain.repository.SettingsRepositoryInterface import SettingsRepositoryInterface


class DuplicateRemover:
    def __init__(
            self,
            binaryComparator: BinaryComparator,
            fileNameComparator: FileNameComparator,
            settingsRepository: SettingsRepositoryInterface,
            eventManager: EventManagerInterface,
    ):
        self.binaryComparator = binaryComparator
        self.fileNameComparator = fileNameComparator
        self.settingsRepository = settingsRepository
        self.eventManager = eventManager

    def removeFilesByIdenticalBinaryContent(
        self,
        allFiles: list[FileInfo],
        fileLookedUp: FileInfo,
    ):
        for file in allFiles:
            if not os_path.isfile(file.fullPath):
                continue

            if self.__filesMatchRequiredSize(file, fileLookedUp) is True:
                if self.binaryComparator.compare(file, fileLookedUp) is True:
                    self.__removeFile(file, fileLookedUp)
                    break

    def removeFilesByIdenticalFileName(
        self,
        allFiles: list[FileInfo],
        fileLookedUp: FileInfo,
    ):
        for file in allFiles:
            if self.fileNameComparator.compare(file, fileLookedUp) is True:
                self.__removeFile(file, fileLookedUp)
                break

    def __notifyDuplicateFound(self, file: FileInfo, fileLookedUp: FileInfo):
        self.eventManager.trigger(
            "output",
            "Removed " + file.fullPath + " duplicate of " + fileLookedUp.fullPath
        )

    def __filesMatchRequiredSize(self, file: FileInfo, fileLookedUp: FileInfo):
        return (
            self.__filesComparedAreNotTooLarge(file, fileLookedUp)
            or self.settingsRepository.loadOne("binarySearchLargeFiles") is True
        )

    def __filesComparedAreNotTooLarge(self, file: FileInfo, fileLookedUp: FileInfo):
        fileSizeThreshold = self.settingsRepository.loadOne("binaryComparisonLargeFilesThreshold")

        return (
            os_path.getsize(fileLookedUp.fullPath) < fileSizeThreshold
            and os_path.getsize(file.fullPath) < fileSizeThreshold
        )

    def __removeFile(self, file: FileInfo, fileLookedUp: FileInfo):
        os_remove(file.fullPath)
        self.__notifyDuplicateFound(file, fileLookedUp)
