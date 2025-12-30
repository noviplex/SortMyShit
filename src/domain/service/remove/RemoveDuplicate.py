from os import path as os_path

from src.domain.event.EventManagerInterface import EventManagerInterface
from src.domain.repository.FileInfoRepositoryInterface import FileInfoRepositoryInterface
from src.domain.entity.DuplicateMatch import DuplicateMatch


class RemoveDuplicate:
    def __init__(
            self,
            file_info_repository: FileInfoRepositoryInterface,
            event_manager: EventManagerInterface
    ):
        self.file_info_repository = file_info_repository
        self.event_manager = event_manager

    def remove_duplicates(self, duplicatesList: list[DuplicateMatch]):
        self.event_manager.trigger("status", "Removing duplicate files")

        for duplicate in duplicatesList:
            for file in duplicate.files:
                if not os_path.isfile(file.full_path):
                    continue

                self.file_info_repository.remove_one(file.full_path)
                self.event_manager.trigger(
                    "output",
                    f"Removed {file.full_path} duplicate of {duplicate.duplicate_of.full_path}"
                )
