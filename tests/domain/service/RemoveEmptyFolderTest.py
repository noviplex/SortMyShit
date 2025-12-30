from unittest import TestCase
from unittest.mock import Mock
from pathlib import Path
from os import path as os_path, remove as os_remove, makedirs as os_makedirs, rmdir as os_rmdir

from src.domain.entity.FileInfo import FileInfo
from src.domain.service.remove.RemoveEmptyFolder import RemoveEmptyFolder
from src.domain.repository.SettingsRepositoryInterface import SettingsRepositoryInterface
from src.domain.event.EventManagerInterface import EventManagerInterface


class RemoveEmptyFolderTest(TestCase):
    def setUp(self):
        root_folder = (
            str(Path().resolve()) + "/tests/domain/service/RemoveEmptyFolderTest"
        )
        self.empty_folder_path = root_folder + "/TestEmptyFolder"
        self.not_empty_folder_path = root_folder + "/TestNotEmptyFolder"

        self._clear_folders()

        os_makedirs(self.empty_folder_path)
        os_makedirs(self.not_empty_folder_path)

        self.file_info1 = self._create_file(
            self.not_empty_folder_path + "/filetest.txt", "TEST_FILE_CONTENT"
        )

        settings_repository_mock = Mock(SettingsRepositoryInterface)
        settings_repository_mock.fetch_one.side_effect = [root_folder]

        self.empty_folder_remover = RemoveEmptyFolder(
            Mock(EventManagerInterface),
            settings_repository_mock,
        )

        super().setUp()

    def tearDown(self):
        self._clear_folders()
        super().tearDown()

    def test_given_folders_when_empty_folders_are_present_then_only_empty_folders_removed(self):
        empty_folders = self.empty_folder_remover.list_empty_folders()
        self.empty_folder_remover.remove_empty_folders(empty_folders)

        self.assertTrue(os_path.isdir(self.not_empty_folder_path))
        self.assertFalse(os_path.isdir(self.empty_folder_path))

    def _create_file(self, file_path, file_contents):
        with open(file_path, "w") as file:
            file.write(file_contents)
        return FileInfo(file_path, "", 500, file_contents)

    def _clear_folders(self):
        if os_path.isdir(self.empty_folder_path):
            os_rmdir(self.empty_folder_path)
        if os_path.isdir(self.not_empty_folder_path):
            file_path = self.not_empty_folder_path + "/filetest.txt"
            if os_path.isfile(file_path):
                os_remove(file_path)
            os_rmdir(self.not_empty_folder_path)
