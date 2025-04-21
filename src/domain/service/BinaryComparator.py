from src.domain.event.EventManagerInterface import EventManagerInterface
from src.domain.entity.FileInfo import FileInfo
from src.domain.repository.FileInfoRepositoryInterface import FileInfoRepositoryInterface
from src.domain.repository.SettingsRepositoryInterface import SettingsRepositoryInterface


class BinaryComparator:
    def __init__(
        self,
        eventManager: EventManagerInterface,
        fileInfoRepository: FileInfoRepositoryInterface,
        settingsRepository: SettingsRepositoryInterface,
    ):
        self.eventManager = eventManager
        self.fileInfoRepository = fileInfoRepository
        self.settingsRepository = settingsRepository

    def compare(self, file1: FileInfo, file2: FileInfo):
        self.eventManager.trigger("status", "Comparing " + file2.fullPath + " with " + file1.fullPath)

        if self.__filesMatchRequiredSize(file1, file2) is False:
            return False

        if (
            file2.fullPath != file1.fullPath
            and file2.partialContents == file1.partialContents
        ):
            fileInfo1 = self.fileInfoRepository.fetchOne(file1.fullPath, withFullContents=True)
            fileInfo2 = self.fileInfoRepository.fetchOne(file2.fullPath, withFullContents=True)

            if (fileInfo1.contents == fileInfo2.contents):
                return True

        return False

    def __filesMatchRequiredSize(self, file: FileInfo, fileLookedUp: FileInfo):
        return (
            self.__filesComparedAreNotTooLarge(file, fileLookedUp)
            or self.settingsRepository.fetchOne("binarySearchLargeFiles") is True
        )

    def __filesComparedAreNotTooLarge(self, file: FileInfo, fileLookedUp: FileInfo):
        fileSizeThreshold = self.settingsRepository.fetchOne("binaryComparisonLargeFilesThreshold")

        return (fileLookedUp.size < fileSizeThreshold and file.size < fileSizeThreshold)
