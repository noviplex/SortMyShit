from os import rmdir as os_rmdir, walk as os_walk

from src.domain.event.LogActivityEvent import LogActivityEvent
from src.domain.event.RemoveEmptyFoldersEvent import RemoveEmptyFoldersEvent
from src.domain.repository.SettingsRepositoryInterface import SettingsRepositoryInterface


class EmptyFolderRemover:
    def __init__(
            self,
            logActivityEvent: LogActivityEvent,
            removeEmptyFoldersEvent: RemoveEmptyFoldersEvent,
            settingsRepository: SettingsRepositoryInterface
    ):
        self.logActivityEvent = logActivityEvent
        self.removeEmptyFoldersEvent = removeEmptyFoldersEvent
        self.settingsRepository = settingsRepository

    def removeEmptyFolders(self):
        folderToProcess = self.settingsRepository.loadOne("folderToProcess")
        emptyFoldersCount = 0
        self.logActivityEvent.trigger("Begin empty folders removal")

        for root, dirs, files in os_walk(folderToProcess):
            if not len(dirs) and not len(files) and not root == folderToProcess:
                os_rmdir(root)
                emptyFoldersCount += 1

                deletedFolderText = "Deleted empty directory " + root
                self.removeEmptyFoldersEvent.trigger(deletedFolderText)
                self.logActivityEvent.trigger(deletedFolderText)

        self.removeEmptyFoldersEvent.trigger("Finished deleting empty directories. " + str(emptyFoldersCount) + " folder(s) found")
        self.logActivityEvent.trigger("Done")
