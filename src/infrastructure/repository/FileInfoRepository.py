from os import path as os_path, walk as os_walk, remove as os_remove
from glob import glob

from src.domain.entity.FileInfo import FileInfo
from src.domain.repository.FileInfoRepositoryInterface import FileInfoRepositoryInterface
from src.infrastructure.repository.SettingsRepository import SettingsRepository
from src.application.service.EventManager import EventManager


class FileInfoRepository(FileInfoRepositoryInterface):
    def __init__(
        self,
        settingsRepository: SettingsRepository,
        eventManager: EventManager,
    ):
        self.settingsRepository = settingsRepository
        self.eventManager = eventManager

    def fetchAllFromFolder(
        self,
        folderPath: str,
        skipEmptyFiles: bool = True,
        skipLargeFiles: bool = True,
    ) -> list[FileInfo]:
        allFileFullPaths = [y for x in os_walk(folderPath) for y in glob(os_path.join(x[0], '*.*'))]

        allFiles = []

        for fileFullPath in allFileFullPaths:
            if not os_path.isfile(fileFullPath):
                continue

            if (
                os_path.getsize(fileFullPath) > self.settingsRepository.fetchOne("binaryComparisonLargeFilesThreshold")
                and self.settingsRepository.fetchOne("binarySearch") is True
                and self.settingsRepository.fetchOne("binarySearchLargeFiles") is False
                and skipLargeFiles
            ):
                self.eventManager.trigger("output", "Skipping large file " + fileFullPath)
            else:
                f = open(fileFullPath, 'rb')

                filePartialContents = f.read(128)

                if len(filePartialContents) == 0 and skipEmptyFiles:
                    self.eventManager.trigger("output", "Skipping empty File " + fileFullPath)
                else:
                    allFiles.append(
                        FileInfo(
                            fullPath=fileFullPath,
                            fileName=os_path.basename(fileFullPath),
                            size=os_path.getsize(fileFullPath),
                            partialContents=filePartialContents,
                        )
                    )
                f.close()

        return allFiles

    def fetchOne(self, fullPath: str, withFullContents: bool = False, readMode: str = "rb") -> FileInfo:
        fileOpened = open(fullPath, readMode)
        filePartialContents = fileOpened.read(128)

        if withFullContents:
            fileContents = fileOpened.read()
        fileOpened.close()

        return FileInfo(
            fullPath=fullPath,
            fileName=os_path.basename(fullPath),
            size=os_path.getsize(fullPath),
            partialContents=filePartialContents,
            contents=fileContents
        )

    def removeOne(self, filePath: str):
        os_remove(filePath)
        self.eventManager.trigger("output", "Removed file " + filePath)
