from os import path as os_path, walk as os_walk, mkdir as os_mkdir, remove as os_remove
from glob import glob

from src.domain.entity.FileInfo import FileInfo
from src.domain.event.EventManagerInterface import EventManagerInterface
from src.domain.service.DuplicateRemover import DuplicateRemover
from src.domain.service.FileSorter import FileSorter
from src.domain.repository.SettingsRepositoryInterface import SettingsRepositoryInterface


class FileManager:
    def __init__(
            self,
            eventManager: EventManagerInterface,
            duplicateRemover: DuplicateRemover,
            fileSorter: FileSorter,
            settingsRepository: SettingsRepositoryInterface,
    ):
        self.eventManager = eventManager
        self.duplicateRemover = duplicateRemover
        self.fileSorter = fileSorter
        self.settingsRepository = settingsRepository

    def removeEmptyFiles(self):
        # TODO add param to pick folder from which removing empty files
        allFiles = self.__fetchAllFiles(self.settingsRepository.loadOne("removeDuplicatesFolder"), skipEmptyFiles=False)

        for file in allFiles:
            if not os_path.isfile(file.fullPath):
                continue

            f = open(file.fullPath, 'rb')
            fileContent = f.read(128)

            if len(fileContent) == 0:
                os_remove(file.fullPath)
                self.eventManager.trigger("output", "Removed empty File " + file.fullPath)

        return allFiles

    def moveFilesToSortedFolder(self):
        destinationFolder = self.settingsRepository.loadOne("destinationFolder")

        self.eventManager.trigger("status", "Begin moving files to sorted folder")

        if os_path.isdir(destinationFolder) is False:
            self.eventManager.trigger("status", "Creating folder " + destinationFolder)
            os_mkdir(destinationFolder)

        for category in self.settingsRepository.appSettings.defaultTypeMapping:
            categoryDestinationFolder = destinationFolder + "/" + category

            if os_path.isdir(categoryDestinationFolder) is False:
                self.eventManager.trigger("status", "Creating subfolder " + categoryDestinationFolder)
                os_mkdir(categoryDestinationFolder)

            for extension in self.settingsRepository.appSettings.defaultTypeMapping[category]:
                filesFullPath = [y for x in os_walk(self.settingsRepository.loadOne("folderToProcess")) for y in glob(os_path.join(x[0], '*.' + extension))]

                if self.settingsRepository.loadOne("keepOriginalFiles") is True:
                    self.fileSorter.copyFile(filesFullPath, categoryDestinationFolder)
                else:
                    self.fileSorter.moveFile(filesFullPath, categoryDestinationFolder)
        self.eventManager.trigger("status", "Done")

    def removeDuplicatesInMovedFiles(self):
        self.eventManager.trigger("status", "Fetching files")

        # TODO : give the choice to select from which folder removing duplicates
        allFiles = self.__fetchAllFiles(self.settingsRepository.loadOne("removeDuplicatesFolder"))

        self.eventManager.trigger("status", "Processing files")

        for file in allFiles:

            if not os_path.isfile(file.fullPath):
                continue

            if (self.settingsRepository.loadOne("binarySearch") is True):
                self.duplicateRemover.removeFilesByIdenticalBinaryContent(allFiles, file)
            else:
                self.duplicateRemover.removeFilesByIdenticalFileName(allFiles, file)

        self.eventManager.trigger("status", "Done")

    def __fetchAllFiles(
            self,
            folder,
            skipEmptyFiles: bool = True,
            skipLargeFiles: bool = True,
    ):
        allFileFullPaths = [y for x in os_walk(folder) for y in glob(os_path.join(x[0], '*.*'))]

        allFiles = []

        for fileFullPath in allFileFullPaths:
            if not os_path.isfile(fileFullPath):
                continue

            if (
                os_path.getsize(fileFullPath) > self.settingsRepository.loadOne("binaryComparisonLargeFilesThreshold")
                and self.settingsRepository.loadOne("binarySearch") is True
                and self.settingsRepository.loadOne("binarySearchLargeFiles") is False
                and skipLargeFiles
            ):
                self.eventManager.trigger("output", "Skipping large file " + fileFullPath)
            else:
                f = open(fileFullPath, 'rb')

                fileContent = f.read(128)

                if len(fileContent) == 0 and skipEmptyFiles:
                    self.eventManager.trigger("output", "Skipping empty File " + fileFullPath)
                else:
                    allFiles.append(FileInfo(fileFullPath, fileContent))
                f.close()

        return allFiles
