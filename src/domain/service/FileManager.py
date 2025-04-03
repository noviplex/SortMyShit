from os import path as os_path, walk as os_walk, mkdir as os_mkdir, remove as os_remove
from glob import glob

from src.domain.entity.FileInfo import FileInfo
from src.domain.event.RemoveDuplicatesEvent import RemoveDuplicatesEvent
from src.domain.event.RemoveEmptyFilesEvent import RemoveEmptyFilesEvent
from src.domain.event.LogActivityEvent import LogActivityEvent
from src.domain.service.DuplicateRemover import DuplicateRemover
from src.domain.service.FileSorter import FileSorter
from src.domain.repository.SettingsRepositoryInterface import SettingsRepositoryInterface

class FileManager:
    def __init__(
            self, 
            settingsRepository: SettingsRepositoryInterface,
            duplicateRemover: DuplicateRemover,
            fileSorter: FileSorter,
            logActivityEvent: LogActivityEvent,
            removeEmptyFilesEvent: RemoveEmptyFilesEvent,
            removeDuplicatesEvent: RemoveDuplicatesEvent,
    ):
        self.duplicateRemover = duplicateRemover
        self.fileSorter = fileSorter
        self.logActivityEvent = logActivityEvent
        self.removeEmptyFilesEvent = removeEmptyFilesEvent
        self.removeDuplicatesEvent = removeDuplicatesEvent
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
                self.removeEmptyFilesEvent.trigger("Removed empty File " + file.fullPath)
                
        return allFiles


    def moveFilesToSortedFolder(self):
        destinationFolder = self.settingsRepository.loadOne("destinationFolder")

        self.logActivityEvent.trigger("Begin moving files to sorted folder")
            
        if os_path.isdir(destinationFolder) == False:
            self.logActivityEvent.trigger("Creating folder " + destinationFolder)
            os_mkdir(destinationFolder)

        for category in self.settingsRepository.appSettings.defaultTypeMapping:
            categoryDestinationFolder = destinationFolder + "/" + category

            if os_path.isdir(categoryDestinationFolder) == False:
                self.logActivityEvent.trigger("Creating subfolder " + categoryDestinationFolder)
                os_mkdir(categoryDestinationFolder)

            for extension in self.settingsRepository.appSettings.defaultTypeMapping[category]:
                filesFullPath = [y for x in os_walk(self.settingsRepository.loadOne("folderToProcess")) for y in glob(os_path.join(x[0], '*.' + extension))]

                if self.settingsRepository.loadOne("keepOriginalFiles") == True:
                    self.fileSorter.copyFile(filesFullPath, categoryDestinationFolder)
                else:
                    self.fileSorter.moveFile(filesFullPath, categoryDestinationFolder)
        self.logActivityEvent.trigger("Done")

    def removeDuplicatesInMovedFiles(self):
        self.logActivityEvent.trigger("Begin removing duplicates")
        self.logActivityEvent.trigger("Fetching files")

        # TODO : give the choice to select from which folder removing duplicates 
        allFiles = self.__fetchAllFiles(self.settingsRepository.loadOne("removeDuplicatesFolder"))

        self.logActivityEvent.trigger("Processing files")

        for file in allFiles:
            
            if not os_path.isfile(file.fullPath):
                continue

            if (self.settingsRepository.loadOne("binarySearch") == True):
                self.duplicateRemover.removeFilesByIdenticalBinaryContent(allFiles, file)
            else:
                self.duplicateRemover.removeFilesByIdenticalFileName(allFiles, file)

        self.logActivityEvent.trigger("Done")

    def __fetchAllFiles(
            self, 
            folder,
            skipEmptyFiles: bool = True, 
            skipLargeFiles: bool = True
    ) :
        allFileFullPaths = [y for x in os_walk(folder) for y in glob(os_path.join(x[0], '*.*'))]

        allFiles = []

        for fileFullPath in allFileFullPaths:
            if not os_path.isfile(fileFullPath):
                continue

            if (
                os_path.getsize(fileFullPath) > self.settingsRepository.loadOne("binaryComparisonLargeFilesThreshold")
                and self.settingsRepository.loadOne("binarySearch") == True 
                and self.settingsRepository.loadOne("binarySearchLargeFiles") == False
                and skipLargeFiles
            ):
                self.removeDuplicatesEvent.trigger("Skipping large file " + fileFullPath)
            else:
                f = open(fileFullPath, 'rb')

                fileContent = f.read(128)

                if len(fileContent) == 0 and skipEmptyFiles:
                    self.removeDuplicatesEvent.trigger("Empty File " + fileFullPath)
                else:
                    allFiles.append(FileInfo(fileFullPath, fileContent))
                f.close()

        return allFiles
