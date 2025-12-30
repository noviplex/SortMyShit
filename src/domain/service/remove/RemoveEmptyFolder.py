from os import rmdir as os_rmdir, walk as os_walk

from src.domain.event.EventManagerInterface import EventManagerInterface
from src.domain.repository.SettingsRepositoryInterface import SettingsRepositoryInterface


class RemoveEmptyFolder:
    def __init__(
        self,
        event_manager: EventManagerInterface,
        settings_repository: SettingsRepositoryInterface
    ):
        self.event_manager = event_manager
        self.settings_repository = settings_repository

    def list_empty_folders(self) -> list[str]:
        folder_to_process = self.settings_repository.fetch_one("folder_to_process")
        empty_folders = []
        self.event_manager.trigger("status", "Begin empty folders listing")

        for root, dirs, files in os_walk(folder_to_process):
            if not dirs and not files and root != folder_to_process:
                empty_folders.append(root)
                self.event_manager.trigger(
                    "foundEmptyFolder",
                    f"Found empty directory {root}"
                )

        self.event_manager.trigger(
            "status",
            f"Finished listing empty directories. {len(empty_folders)} folder(s) found"
        )

        self.event_manager.trigger("status", "Done")
        return empty_folders

    def remove_empty_folders(self, empty_folders: list[str]) -> None:
        for empty_folder in empty_folders:
            os_rmdir(empty_folder)

            self.event_manager.trigger(
                "deletedEmptyFolder",
                f"Deleted empty directory {empty_folder}"
            )

        self.event_manager.trigger(
            "status",
            "Finished deleting empty directories."
        )

        self.event_manager.trigger("status", "Done")
