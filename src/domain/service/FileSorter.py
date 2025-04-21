from os import system as os_system, path as os_path, walk as os_walk, mkdir as os_mkdir
from glob import glob

from src.domain.event.EventManagerInterface import EventManagerInterface
from src.domain.repository.SettingsRepositoryInterface import SettingsRepositoryInterface


class FileSorter:
    def __init__(
        self,
        eventManager: EventManagerInterface,
        settingsRepository: SettingsRepositoryInterface,
    ):
        self.eventManager = eventManager
        self.settingsRepository = settingsRepository

    def moveFilesToSortedFolder(self):
        destinationFolder = self.settingsRepository.fetchOne("destinationFolder")

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
                filesFullPath = [y for x in os_walk(self.settingsRepository.fetchOne("folderToProcess")) for y in glob(os_path.join(x[0], '*.' + extension))]

                if self.settingsRepository.fetchOne("keepOriginalFiles") is True:
                    self.__copyFile(filesFullPath, categoryDestinationFolder)
                else:
                    self.__moveFile(filesFullPath, categoryDestinationFolder)
        self.eventManager.trigger("status", "Done")

    def __moveFile(self, filesFullPath: str, categoryDestinationFolder: str):
        self.__moveOrCopyFile("rm", filesFullPath, categoryDestinationFolder)

    def __copyFile(self, filesFullPath: str, categoryDestinationFolder: str):
        self.__moveOrCopyFile("cp", filesFullPath, categoryDestinationFolder)

    def __moveOrCopyFile(self, command: str, filesFullPath: str, categoryDestinationFolder: str):
        action = "copied" if command == "cp" else "moved"
        for fileFullPath in filesFullPath:

            os_system(command + " \"" + fileFullPath + "\" " + categoryDestinationFolder)
            self.eventManager.trigger("output", fileFullPath + " " + action + " successfully, now into " + categoryDestinationFolder)
