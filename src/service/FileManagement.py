from os import path as os_path, walk as os_walk, mkdir as os_mkdir, remove as os_remove, system as os_system
from glob import glob

from src.event.DuplicateFoundEvent import DuplicateFoundEvent
from src.event.LogActivityEvent import LogActivityEvent
from src.event.FileMovedEvent import FileMovedEvent

from src.configuration.ServiceManager import ServiceManager

from src.service.SettingsService import SettingsService

class FileManagement:
    def __init__(self, serviceManager: ServiceManager = ServiceManager()):
        self.settingsService = serviceManager.get("SettingsService") # type: SettingsService
        self.logActivityEvent = serviceManager.get("LogActivityEvent") # type: LogActivityEvent
        self.duplicateFoundEvent = serviceManager.get("DuplicateFoundEvent") # type: DuplicateFoundEvent
        self.fileMovedEvent = serviceManager.get("FileMovedEvent") # type: FileMovedEvent
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
                    self.__copyFile(filesFullPath, categoryDestinationFolder)
                else:
                    self.__moveFile(filesFullPath, categoryDestinationFolder)
        self.logActivityEvent.trigger("Done")

    def removeDuplicatesInMovedFiles(self):
        self.logActivityEvent.trigger("Begin removing duplicates")

        self.logActivityEvent.trigger("Fetching files")

        allFiles = self.__fetchAllFiles()

        self.logActivityEvent.trigger("Processing files")

        for fileCompared in allFiles:
            if not os_path.isfile(fileCompared["fileFullPath"]):
                continue

            if (self.settingsService.getSetting("binarySearch") == True):
                self.__compareFileBinaries(allFiles, fileCompared)
            else:
                self.__compareFileNames(allFiles, fileCompared)

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
                self.duplicateFoundEvent.trigger("Skipping large file " + fileFullPath)
            else:
                f = open(fileFullPath, 'rb')

                fileContent = f.read(128)

                if len(fileContent) == 0:
                    self.duplicateFoundEvent.trigger("Empty File " + fileFullPath)
                else:
                    allFiles.append({"fileFullPath": fileFullPath, "filePartialContent": fileContent})
                f.close()

        return allFiles
    

    def __compareFileBinaries(self, allFiles, fileCompared):
        fileSizeThreshold = self.settingsService.getSetting("binaryComparisonLargeFilesThreshold")

        for fileToCompare in allFiles:
            if not os_path.isfile(fileToCompare["fileFullPath"]):
                continue
            else:
                self.logActivityEvent.trigger("Comparing " + fileCompared["fileFullPath"] + " with " + fileToCompare["fileFullPath"])

            if (
                (
                    (
                        os_path.getsize(fileCompared["fileFullPath"]) < fileSizeThreshold
                        and os_path.getsize(fileToCompare["fileFullPath"]) < fileSizeThreshold
                    )
                    or self.settingsService.getSetting("binarySearchLargeFiles") == True
                )
                and fileCompared["fileFullPath"] != fileToCompare["fileFullPath"]
                and fileCompared["filePartialContent"] == fileToCompare["filePartialContent"]
            ):

                fileFetchedOpened = open(fileToCompare["fileFullPath"], 'rb')
                fileOpened = open(fileCompared["fileFullPath"], 'rb')

                if (fileFetchedOpened.read() == fileOpened.read()):
                    os_remove(fileToCompare["fileFullPath"])
                    self.__notifyDuplicateFound(fileToCompare, fileCompared)
                fileFetchedOpened.close()
                fileOpened.close()

    def __compareFileNames(self, allFiles, fileCompared):
        for fileToCompare in allFiles:
            self.logActivityEvent.trigger("Comparing " + fileCompared["fileFullPath"] + " with " + fileToCompare["fileFullPath"])
            
            if (
                os_path.basename(fileCompared["fileFullPath"]) == os_path.basename(fileToCompare["fileFullPath"]) 
                and fileCompared["fileFullPath"] != fileToCompare["fileFullPath"]
            ):
                os_remove(fileToCompare["fileFullPath"])
                self.__notifyDuplicateFound(fileToCompare, fileCompared)
                break

    def __notifyDuplicateFound(self, fileToCompare, fileCompared):
        self.duplicateFoundEvent.trigger("Removed " + fileToCompare["fileFullPath"] + " duplicate of " + fileCompared["fileFullPath"])
        self.logActivityEvent.trigger("Removed " + fileToCompare["fileFullPath"] + " duplicate of " + fileCompared["fileFullPath"])

    def __moveFile(self, filesFullPath: str, categoryDestinationFolder: str):                    
        self.__moveOrCopyFile("rm", filesFullPath, categoryDestinationFolder)
        
    def __copyFile(self, filesFullPath: str, categoryDestinationFolder: str):                    
        self.__moveOrCopyFile("cp", filesFullPath, categoryDestinationFolder)

    def __moveOrCopyFile(self, command: str, filesFullPath: str, categoryDestinationFolder: str):
        action = "copied" if command == "cp" else "moved"
        for fileFullPath in filesFullPath:
            
            os_system(command + " \"" + fileFullPath + "\" " + categoryDestinationFolder)
            self.fileMovedEvent.trigger(fileFullPath + " " + action + " successfully, now into " + categoryDestinationFolder)
            self.logActivityEvent.trigger(fileFullPath + " " + action + " successfully, now into " + categoryDestinationFolder)