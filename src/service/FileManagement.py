from os import path as os_path, walk as os_walk, mkdir as os_mkdir, system as os_system
from glob import glob

from src.entity.Settings import Settings

from src.event.DuplicateFoundEvent import DuplicateFoundEvent
from src.event.LogActivityEvent import LogActivityEvent
from src.event.FileMovedEvent import FileMovedEvent

from src.configuration.ServiceManager import ServiceManager

class FileManagement:
    def __init__(self, serviceManager: ServiceManager = ServiceManager()):
        self.settings = serviceManager.get("Settings") # type: Settings
        self.logActivityEvent = serviceManager.get("LogActivityEvent") # type: LogActivityEvent
        self.duplicateFoundEvent = serviceManager.get("DuplicateFoundEvent") # type: DuplicateFoundEvent
        self.fileMovedEvent = serviceManager.get("FileMovedEvent") # type: FileMovedEvent
        
    def moveFilesToSortedFolder(self):
        self.logActivityEvent.trigger("Begin moving files to sorted folder")
            
        if os_path.isdir(self.settings.destinationFolder) == False:
            self.logActivityEvent.trigger("Creating folder " + self.settings.destinationFolder)
            os_mkdir(self.settings.destinationFolder)

        for category in self.settings.defaultTypeMapping:
            destinationFolder = self.settings.destinationFolder + "/" + category

            if os_path.isdir(destinationFolder) == False:
                self.logActivityEvent.trigger("Creating subfolder " + destinationFolder)
                os_mkdir(destinationFolder)

            for extension in self.settings.defaultTypeMapping[category]:
                filesFullPath = [y for x in os_walk(self.settings.folderToProcess) for y in glob(os_path.join(x[0], '*.' + extension))]

                if self.settings.getSetting("keepOriginalFiles") == True:
                    self.__copyFile(filesFullPath, destinationFolder)
                else:
                    self.__moveFile(filesFullPath, destinationFolder)

    def removeDuplicatesInMovedFiles(self):
        self.logActivityEvent.trigger("Begin removing duplicates")

        self.logActivityEvent.trigger("Fetching files")

        allFiles = self.__fetchAllFiles()

        self.logActivityEvent.trigger("Processing files")

        for fileCompared in allFiles:
            if not os_path.isfile(fileCompared["fileFullPath"]):
                continue

            for fileToCompare in allFiles:
                if (self.settings.getSetting("binarySearch") == True):
                    self.__compareFileBinaries(fileToCompare, fileCompared)
                else:
                    self.__compareFileNames(fileToCompare, fileCompared)

        self.logActivityEvent.trigger("Done")

    def __fetchAllFiles(self):
        allFileFullPaths = [y for x in os_walk(self.settings.destinationFolder) for y in glob(os_path.join(x[0], '*.*'))]
        allFileFullPaths.sort()

        allFiles = []

        for fileFullPath in allFileFullPaths:
            if not os_path.isfile(fileFullPath):
                continue

            if (
                os_path.getsize(fileFullPath) > self.settings.getSetting("binaryComparisonLargeFilesThreshold")
                and self.settings.getSetting("binarySearch") == True 
                and self.settings.getSetting("binarySearchLargeFiles") == False
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
    

    def __compareFileBinaries(self, fileToCompare, fileCompared):
        self.logActivityEvent.trigger("Comparing " + fileCompared["fileFullPath"] + " with " + fileToCompare["fileFullPath"])

        if (
            (
                (
                    os_path.getsize(fileCompared["fileFullPath"]) < self.settings.getSetting("binaryComparisonLargeFilesThreshold")
                    and os_path.getsize(fileToCompare["fileFullPath"]) < self.settings.getSetting("binaryComparisonLargeFilesThreshold")
                )
                or self.settings.getSetting("binarySearchLargeFiles") == True
            ) 
            and fileCompared["fileFullPath"] != fileToCompare["fileFullPath"]
            and fileCompared["filePartialContent"] == fileToCompare["filePartialContent"]
        ):
            fileFetchedOpened = open(fileToCompare["fileFullPath"], 'rb')
            fileOpened = open(fileCompared["fileFullPath"], 'rb')

            if (fileFetchedOpened.read() == fileOpened.read()):
                # TODO: add file deletion
                self.__notifyDuplicateFound(fileToCompare, fileCompared)

            fileFetchedOpened.close()
            fileOpened.close()

    def __compareFileNames(self, fileToCompare, fileCompared):
        self.logActivityEvent.trigger("Comparing " + fileCompared["fileFullPath"] + " with " + fileToCompare["fileFullPath"])

        if (
            os_path.basename(fileCompared["fileFullPath"]) == os_path.basename(fileToCompare["fileFullPath"]) 
            and fileCompared["fileFullPath"] != fileToCompare["fileFullPath"]
        ):
            # TODO: add file deletion
            self.__notifyDuplicateFound(fileToCompare, fileCompared)

    def __notifyDuplicateFound(self, fileToCompare, fileCompared):
        self.duplicateFoundEvent.trigger(fileCompared["fileFullPath"] + " duplicate of " + fileToCompare["fileFullPath"])
        self.logActivityEvent.trigger(fileCompared["fileFullPath"] + " duplicate of " + fileToCompare["fileFullPath"])

    def __moveFile(self, filesFullPath: str, destinationFolder: str):                    
        self.__moveOrCopyFile("rm", filesFullPath, destinationFolder)
        
    def __copyFile(self, filesFullPath: str, destinationFolder: str):                    
        self.__moveOrCopyFile("cp", filesFullPath, destinationFolder)

    def __moveOrCopyFile(self, command: str, filesFullPath: str, destinationFolder: str):
        action = "copied" if command == "cp" else "moved"
        for fileFullPath in filesFullPath:
            
            os_system(command + " \"" + fileFullPath + "\" " + destinationFolder)
            self.fileMovedEvent.trigger(fileFullPath + " " + action + " successfully, now into " + destinationFolder)
            self.logActivityEvent.trigger(fileFullPath + " " + action + " successfully, now into " + destinationFolder)
