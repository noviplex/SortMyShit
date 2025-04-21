from os import path as os_path

from src.domain.event.EventManagerInterface import EventManagerInterface
from src.domain.repository.SettingsRepositoryInterface import SettingsRepositoryInterface
from src.domain.repository.FileInfoRepositoryInterface import FileInfoRepositoryInterface
from src.domain.entity.FileInfo import FileInfo


class EmptyFileRemover:
    def __init__(
            self,
            eventManager: EventManagerInterface,
            settingsRepository: SettingsRepositoryInterface,
            fileInfoRepository: FileInfoRepositoryInterface,
    ):
        self.eventManager = eventManager
        self.settingsRepository = settingsRepository
        self.fileInfoRepository = fileInfoRepository

    def removeEmptyFiles(self):
        # TODO add setting to pick folder from which removing empty files
        allFiles = self.fileInfoRepository.fetchAllFromFolder(
            self.settingsRepository.fetchOne("removeDuplicatesFolder"),
            skipEmptyFiles=False
        )

        file: FileInfo
        for file in allFiles:
            if not os_path.isfile(file.fullPath):
                continue

            if len(file.partialContents) == 0:
                self.fileInfoRepository.removeOne(file.fullPath)
                self.eventManager.trigger("output", "Removed empty File " + file.fullPath)

        return allFiles
