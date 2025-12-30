from os import path as os_path

from src.domain.entity.FileInfo import FileInfo
from src.domain.entity.DuplicateMatch import DuplicateMatch
from src.domain.event.EventManagerInterface import EventManagerInterface
from src.domain.repository.SettingsRepositoryInterface import SettingsRepositoryInterface
from src.domain.repository.FileInfoRepositoryInterface import FileInfoRepositoryInterface
from src.domain.service.compare.CompareBinary import CompareBinary
from src.domain.service.compare.CompareFileName import CompareFileName


class ListDuplicate:
    def __init__(
        self,
        event_manager: EventManagerInterface,
        settings_repository: SettingsRepositoryInterface,
        file_info_repository: FileInfoRepositoryInterface,
        binary_comparator: CompareBinary,
        file_name_comparator: CompareFileName,
    ):
        self.event_manager = event_manager
        self.settings_repository = settings_repository
        self.file_info_repository = file_info_repository
        self.binary_comparator = binary_comparator
        self.file_name_comparator = file_name_comparator

    def list_duplicates(self):
        self.event_manager.trigger("status", "Fetching files")

        duplicate_matches = []

        all_files = self.file_info_repository.fetch_all_from_folder(
            self.settings_repository.fetch_one("remove_duplicates_folder")
        )

        self.event_manager.trigger("status", "Processing files")

        file: FileInfo
        for file in all_files:
            if not os_path.isfile(file.full_path):
                continue

            if self.settings_repository.fetch_one("binary_search") is True:
                duplicate_match = self.__list_files_by_identical_binary_content(all_files, file)
            else:
                duplicate_match = self.__list_files_by_identical_file_name(all_files, file)

            if duplicate_match is not None:
                duplicate_matches.append(duplicate_match)

        self.event_manager.trigger("status", "Done")

        return duplicate_matches

    def __list_files_by_identical_binary_content(
        self,
        all_files: list[FileInfo],
        duplicate_of: FileInfo,
    ) -> DuplicateMatch:
        file: FileInfo

        files = []

        for file in all_files:
            if not os_path.isfile(file.full_path):
                continue

            if self.binary_comparator.compare(file, duplicate_of) is True:
                files.append(file)

        if len(files) == 0:
            return None

        self.__remove_found_duplicates_from_all_files_list(all_files, files, duplicate_of)
        return DuplicateMatch(files, duplicate_of)

    def __list_files_by_identical_file_name(
        self,
        all_files: list[FileInfo],
        file_looked_up: FileInfo,
    ) -> DuplicateMatch:
        file: FileInfo
        for file in all_files:
            if not os_path.isfile(file.full_path):
                continue

            if self.file_name_comparator.compare(file, file_looked_up) is True:
                return DuplicateMatch(file_looked_up, file)

    def __remove_found_duplicates_from_all_files_list(
            self,
            all_files: list[FileInfo],
            files: list[FileInfo],
            duplicate_of: FileInfo):
        for file in files:
            del all_files[all_files.index(file)]

        del all_files[all_files.index(duplicate_of)]
