from src.domain.event.EventManagerInterface import EventManagerInterface
from src.domain.entity.FileInfo import FileInfo
from src.domain.repository.FileInfoRepositoryInterface import FileInfoRepositoryInterface
from src.domain.repository.SettingsRepositoryInterface import SettingsRepositoryInterface


class CompareBinary:
    def __init__(
        self,
        event_manager: EventManagerInterface,
        file_info_repository: FileInfoRepositoryInterface,
        settings_repository: SettingsRepositoryInterface,
    ):
        self.event_manager = event_manager
        self.file_info_repository = file_info_repository
        self.settings_repository = settings_repository

    def compare(self, file1: FileInfo, file2: FileInfo):
        self.event_manager.trigger(
            "status",
            f"Comparing {file2.full_path} with {file1.full_path}"
        )

        if not self.__files_match_required_size(file1, file2):
            return False

        if (
            file2.full_path != file1.full_path
            and file2.partial_contents == file1.partial_contents
        ):
            file_info1 = self.file_info_repository.fetch_one(
                file1.full_path, with_full_contents=True
            )
            file_info2 = self.file_info_repository.fetch_one(
                file2.full_path, with_full_contents=True
            )

            if file_info1.contents == file_info2.contents:
                return True

        return False

    def __files_match_required_size(self, file: FileInfo, file_looked_up: FileInfo):
        return (
            self.__files_compared_are_not_too_large(file, file_looked_up)
            or self.settings_repository.fetch_one("binary_search_large_files") is True
        )

    def __files_compared_are_not_too_large(self, file: FileInfo, file_looked_up: FileInfo):
        file_size_threshold = self.settings_repository.fetch_one(
            "binary_comparison_large_files_threshold"
        )
        return (
            file_looked_up.size < file_size_threshold
            and file.size < file_size_threshold
        )
