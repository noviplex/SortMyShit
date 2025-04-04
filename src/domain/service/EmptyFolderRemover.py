from os import rmdir as os_rmdir, walk as os_walk

from src.domain.event.EventManagerInterface import EventManagerInterface
from src.domain.repository.SettingsRepositoryInterface import SettingsRepositoryInterface


class EmptyFolderRemover:
    def __init__(
            self,
            eventManager: EventManagerInterface,
            settingsRepository: SettingsRepositoryInterface
    ):
        self.eventManager = eventManager
        self.settingsRepository = settingsRepository

    def removeEmptyFolders(self):
        folderToProcess = self.settingsRepository.loadOne("folderToProcess")
        emptyFoldersCount = 0
        self.eventManager.trigger("status", "Begin empty folders removal")

        for root, dirs, files in os_walk(folderToProcess):
            if not len(dirs) and not len(files) and not root == folderToProcess:
                os_rmdir(root)
                emptyFoldersCount += 1

                self.eventManager.trigger(
                    "deletedEmptyFolder",
                    "Deleted empty directory " + root
                )

        self.eventManager.trigger(
            "status",
            "Finished deleting empty directories. " + str(emptyFoldersCount) + " folder(s) found"
        )

        self.eventManager.trigger("status", "Done")
