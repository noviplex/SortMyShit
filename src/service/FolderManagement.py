from os import rmdir as os_rmdir, walk as os_walk

from src.event.LogActivityEvent import LogActivityEvent
from src.event.FolderDeletedEvent import FolderDeletedEvent

from src.service.SettingsService import SettingsService

from src.configuration.ServiceManager import ServiceManager

class FolderManagement:
    def __init__(self, serviceManager: ServiceManager = ServiceManager()):
        self.logActivityEvent = serviceManager.get("SettingsService") # type: SettingsService
        self.logActivityEvent = serviceManager.get("LogActivityEvent") # type: LogActivityEvent
        self.folderDeletedEvent = serviceManager.get("FolderDeletedEvent") # type: FolderDeletedEvent
        self.settingsService = serviceManager.get("SettingsService") # type: SettingsService

    def removeEmptyFolder(self):
        emptyFoldersCount = 0
        self.logActivityEvent.trigger("Begin empty folders removal")

        for root, dirs, files in os_walk(self.settingsService.getSetting("folderToProcess")): 
            if not len(dirs) and not len(files) and not root == self.settingsService.getSetting("folderToProcess"): 
                os_rmdir(root)
                emptyFoldersCount += 1

                deletedFolderText = "Deleted empty directory " + root
                self.folderDeletedEvent.trigger(deletedFolderText)
                self.logActivityEvent.trigger(deletedFolderText)

        self.folderDeletedEvent.trigger("Finished deleting empty directories. " + str(emptyFoldersCount) + " folder(s) found")
        self.logActivityEvent.trigger("Done")
                