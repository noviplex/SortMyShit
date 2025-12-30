import os
from glob import glob

from src.domain.event.EventManagerInterface import EventManagerInterface
from src.domain.repository.SettingsRepositoryInterface import SettingsRepositoryInterface


class SortFile:
    def __init__(
        self,
        event_manager: EventManagerInterface,
        settings_repository: SettingsRepositoryInterface,
    ):
        self.event_manager = event_manager
        self.settings_repository = settings_repository

    def move_files_to_sorted_folder(self):
        destination_folder = self.settings_repository.fetch_one("destination_folder")

        self.event_manager.trigger("status", "Begin moving files to sorted folder")

        if not os.path.isdir(destination_folder):
            self.event_manager.trigger("status", f"Creating folder {destination_folder}")
            os.mkdir(destination_folder)

        for category in self.settings_repository.app_settings.default_type_mapping:
            category_destination_folder = os.path.join(destination_folder, category)

            if not os.path.isdir(category_destination_folder):
                self.event_manager.trigger("status", f"Creating subfolder {category_destination_folder}")
                os.mkdir(category_destination_folder)

            for extension in self.settings_repository.app_settings.default_type_mapping[category]:
                files_full_path = [
                    y
                    for x in os.walk(self.settings_repository.fetch_one("folder_to_process"))
                    for y in glob(os.path.join(x[0], f"*.{extension}"))
                ]

                if self.settings_repository.fetch_one("keep_original_files"):
                    self._copy_file(files_full_path, category_destination_folder)
                else:
                    self._move_file(files_full_path, category_destination_folder)
        self.event_manager.trigger("status", "Done")

    def _move_file(self, files_full_path: list, category_destination_folder: str):
        self._move_or_copy_file("mv", files_full_path, category_destination_folder)

    def _copy_file(self, files_full_path: list, category_destination_folder: str):
        self._move_or_copy_file("cp", files_full_path, category_destination_folder)

    def _move_or_copy_file(self, command: str, files_full_path: list, category_destination_folder: str):
        action = "copied" if command == "cp" else "moved"
        for file_full_path in files_full_path:
            os.system(f'{command} "{file_full_path}" "{category_destination_folder}"')
            self.event_manager.trigger(
                "output",
                f'{file_full_path} {action} successfully, now into {category_destination_folder}',
            )
