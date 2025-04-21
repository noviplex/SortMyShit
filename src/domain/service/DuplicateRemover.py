from os import path as os_path

from src.domain.entity.FileInfo import FileInfo
from src.domain.event.EventManagerInterface import EventManagerInterface
from src.domain.service.BinaryComparator import BinaryComparator
from src.domain.service.FileNameComparator import FileNameComparator
from src.domain.repository.FileInfoRepositoryInterface import FileInfoRepositoryInterface


class DuplicateRemover:
    def __init__(
            self,
            binaryComparator: BinaryComparator,
            fileNameComparator: FileNameComparator,
            eventManager: EventManagerInterface,
            fileInfoRepository: FileInfoRepositoryInterface,
    ):
        self.binaryComparator = binaryComparator
        self.fileNameComparator = fileNameComparator
        self.eventManager = eventManager
        self.fileInfoRepository = fileInfoRepository

    def removeFilesByIdenticalBinaryContent(
        self,
        allFiles: list[FileInfo],
        fileLookedUp: FileInfo,
    ):
        for file in allFiles:
            if not os_path.isfile(file.fullPath):
                continue

            if self.binaryComparator.compare(file, fileLookedUp) is True:
                self.__removeFile(file, fileLookedUp)
                break

    def removeFilesByIdenticalFileName(
        self,
        allFiles: list[FileInfo],
        fileLookedUp: FileInfo,
    ):
        for file in allFiles:
            if not os_path.isfile(file.fullPath):
                continue

            if self.fileNameComparator.compare(file, fileLookedUp) is True:
                self.__removeFile(file, fileLookedUp)
                break

    def __removeFile(self, file: FileInfo, fileLookedUp: FileInfo):
        self.fileInfoRepository.removeOne(file.fullPath)
        self.eventManager.trigger(
            "output",
            "Removed " + file.fullPath + " duplicate of " + fileLookedUp.fullPath
        )
