from os import rmdir as os_rmdir, walk as os_walk

from src.entity.Settings import Settings

from src.event.LogActivityEvent import LogActivityEvent
from src.event.FolderDeletedEvent import FolderDeletedEvent

from src.configuration.ServiceManager import ServiceManager

class FolderManagement:
    def __init__(self, serviceManager: ServiceManager = ServiceManager()):
        self.settings = serviceManager.get("Settings") # type: Settings
        self.logActivityEvent = serviceManager.get("LogActivityEvent") # type: LogActivityEvent
        self.folderDeletedEvent = serviceManager.get("FolderDeletedEvent") # type: FolderDeletedEvent

    def removeEmptyFolder(self):
        emptyFoldersCount = 0
        self.logActivityEvent.trigger("Begin empty folders removal")

        for root, dirs, files in os_walk(self.settings.folderToProcess): 
            if not len(dirs) and not len(files) and not root == self.settings.folderToProcess: 
                os_rmdir(root)
                emptyFoldersCount += 1

                deletedFolderText = "Deleted empty directory " + root
                self.folderDeletedEvent.trigger(deletedFolderText)
                self.logActivityEvent.trigger(deletedFolderText)

        self.folderDeletedEvent.trigger("Finished deleting empty directories. " + str(emptyFoldersCount) + " folder(s) found")
        self.logActivityEvent.trigger("Done")
                