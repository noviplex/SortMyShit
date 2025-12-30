from os import path as os_path, walk as os_walk, remove as os_remove
from glob import glob

from src.domain.entity.FileInfo import FileInfo
from src.domain.repository.FileInfoRepositoryInterface import FileInfoRepositoryInterface
from src.infrastructure.repository.SettingsRepository import SettingsRepository
from src.application.service.EventManager import EventManager


class FileInfoRepository(FileInfoRepositoryInterface):
    def __init__(
        self,
        settings_repository: SettingsRepository,
        event_manager: EventManager,
    ):
        self.settings_repository = settings_repository
        self.event_manager = event_manager

    def fetch_all_from_folder(
        self,
        folder_path: str,
        skip_empty_files: bool = True,
        skip_large_files: bool = True,
    ) -> list[FileInfo]:
        all_file_full_paths = [
            y for x in os_walk(folder_path) for y in glob(os_path.join(x[0], "*.*"))
        ]

        all_files = []

        for file_full_path in all_file_full_paths:
            if not os_path.isfile(file_full_path):
                continue

            if (
                os_path.getsize(file_full_path)
                > self.settings_repository.fetch_one("binary_comparison_large_files_threshold")
                and self.settings_repository.fetch_one("binary_search") is True
                and self.settings_repository.fetch_one("binary_search_large_files") is False
                and skip_large_files
            ):
                self.event_manager.trigger("output", "Skipping large file " + file_full_path)
            else:
                with open(file_full_path, "rb") as f:
                    file_partial_contents = f.read(128)

                    if len(file_partial_contents) == 0 and skip_empty_files:
                        self.event_manager.trigger("output", "Skipping empty File " + file_full_path)
                    else:
                        all_files.append(
                            FileInfo(
                                full_path=file_full_path,
                                file_name=os_path.basename(file_full_path),
                                size=os_path.getsize(file_full_path),
                                partial_contents=file_partial_contents,
                            )
                        )

        return all_files

    def fetch_one(
        self, full_path: str, with_full_contents: bool = False, read_mode: str = "rb"
    ) -> FileInfo:
        file_contents = None
        with open(full_path, read_mode) as file_opened:
            file_partial_contents = file_opened.read(128)
            if with_full_contents:
                file_contents = file_opened.read()

        return FileInfo(
            full_path=full_path,
            file_name=os_path.basename(full_path),
            size=os_path.getsize(full_path),
            partial_contents=file_partial_contents,
            contents=file_contents,
        )

    def remove_one(self, file_path: str):
        os_remove(file_path)
        self.event_manager.trigger("output", "Removed file " + file_path)
