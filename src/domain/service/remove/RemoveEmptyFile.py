from os import path as os_path

from src.domain.entity.FileInfo import FileInfo
from src.domain.event.EventManagerInterface import EventManagerInterface
from src.domain.repository.SettingsRepositoryInterface import SettingsRepositoryInterface
from src.domain.repository.FileInfoRepositoryInterface import FileInfoRepositoryInterface


class RemoveEmptyFile:
    def __init__(
        self,
        event_manager: EventManagerInterface,
        settings_repository: SettingsRepositoryInterface,
        file_info_repository: FileInfoRepositoryInterface,
    ):
        self.event_manager = event_manager
        self.settings_repository = settings_repository
        self.file_info_repository = file_info_repository

    def list_empty_files(self):
        self.event_manager.trigger("status", "Fetching files")

        empty_files = []

        all_files = self.file_info_repository.fetch_all_from_folder(
            self.settings_repository.fetch_one("remove_duplicates_folder"),
            skip_empty_files=False,
        )

        file: FileInfo
        for file in all_files:
            if not os_path.isfile(file.full_path):
                continue

            if len(file.partial_contents) == 0:
                empty_files.append(file)

        self.event_manager.trigger("status", "Done")

        return empty_files

    def remove_empty_files(self, empty_files: list[FileInfo]):
        self.event_manager.trigger("status", "Removing empty files")

        for file in empty_files:
            if not os_path.isfile(file.full_path):
                continue

            self.file_info_repository.remove_one(file.full_path)
            self.event_manager.trigger(
                "output",
                f"Removed empty file {file.full_path}"
            )

        self.event_manager.trigger("status", "Done")
