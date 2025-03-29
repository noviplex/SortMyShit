from os import path as os_path, walk as os_walk, mkdir as os_mkdir, remove as os_remove, system as os_system
from glob import glob

from src.event.RemoveDuplicatesEvent import RemoveDuplicatesEvent
from src.event.LogActivityEvent import LogActivityEvent

from src.configuration.ServiceManager import ServiceManager

from src.service.SettingsService import SettingsService
from src.service.DuplicateSearcher import DuplicateSearcher
from src.service.FileSorter import FileSorter

class FileManager:
    def __init__(self, serviceManager: ServiceManager = ServiceManager()):
        self.settingsService = serviceManager.get("SettingsService") # type: SettingsService
        self.duplicateSearcher = serviceManager.get("DuplicateSearcher") # type: DuplicateSearcher
        self.fileSorter = serviceManager.get("FileSorter") # type: FileSorter
        self.logActivityEvent = serviceManager.get("LogActivityEvent") # type: LogActivityEvent
        self.removeDuplicatesEvent = serviceManager.get("RemoveDuplicatesEvent") # type: RemoveDuplicatesEvent
        self.destinationFolder = self.settingsService.getSetting("destinationFolder")

    def moveFilesToSortedFolder(self):
        self.logActivityEvent.trigger("Begin moving files to sorted folder")
            
        if os_path.isdir(self.destinationFolder) == False:
            self.logActivityEvent.trigger("Creating folder " + self.destinationFolder)
            os_mkdir(self.destinationFolder)

        for category in self.settingsService.appSettings.defaultTypeMapping:
            categoryDestinationFolder = self.destinationFolder + "/" + category

            if os_path.isdir(categoryDestinationFolder) == False:
                self.logActivityEvent.trigger("Creating subfolder " + categoryDestinationFolder)
                os_mkdir(categoryDestinationFolder)

            for extension in self.settingsService.appSettings.defaultTypeMapping[category]:
                filesFullPath = [y for x in os_walk(self.settingsService.getSetting("folderToProcess")) for y in glob(os_path.join(x[0], '*.' + extension))]

                if self.settingsService.getSetting("keepOriginalFiles") == True:
                    self.fileSorter.copyFile(filesFullPath, categoryDestinationFolder)
                else:
                    self.fileSorter.moveFile(filesFullPath, categoryDestinationFolder)
        self.logActivityEvent.trigger("Done")

    def removeDuplicatesInMovedFiles(self):
        self.logActivityEvent.trigger("Begin removing duplicates")

        self.logActivityEvent.trigger("Fetching files")

        allFiles = self.__fetchAllFiles()

        self.logActivityEvent.trigger("Processing files")

        for file in allFiles:
            
            if not os_path.isfile(file["fileFullPath"]):
                continue

            if (self.settingsService.getSetting("binarySearch") == True):
                self.duplicateSearcher.compareFileBinaries(allFiles, file)
            else:
                self.duplicateSearcher.compareFileNames(allFiles, file)

        self.logActivityEvent.trigger("Done")

    def __fetchAllFiles(self):
        allFileFullPaths = [y for x in os_walk(self.settingsService.getSetting("removeDuplicatesFolder")) for y in glob(os_path.join(x[0], '*.*'))]
        allFileFullPaths.sort()

        allFiles = []

        for fileFullPath in allFileFullPaths:
            if not os_path.isfile(fileFullPath):
                continue

            if (
                os_path.getsize(fileFullPath) > self.settingsService.getSetting("binaryComparisonLargeFilesThreshold")
                and self.settingsService.getSetting("binarySearch") == True 
                and self.settingsService.getSetting("binarySearchLargeFiles") == False
            ):
                self.removeDuplicatesEvent.trigger("Skipping large file " + fileFullPath)
            else:
                f = open(fileFullPath, 'rb')

                fileContent = f.read(128)

                if len(fileContent) == 0:
                    self.removeDuplicatesEvent.trigger("Empty File " + fileFullPath)
                else:
                    allFiles.append({"fileFullPath": fileFullPath, "filePartialContent": fileContent})
                f.close()

        return allFiles
