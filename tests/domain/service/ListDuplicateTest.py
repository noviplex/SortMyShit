from unittest import TestCase
from unittest.mock import Mock
from pathlib import Path
from os import path as os_path, remove as os_remove

from src.domain.entity.FileInfo import FileInfo
from src.domain.event.EventManagerInterface import EventManagerInterface
from src.domain.service.compare.CompareBinary import CompareBinary
from src.domain.service.list.ListDuplicate import ListDuplicate
from src.domain.service.compare.CompareFileName import CompareFileName
from src.domain.repository.FileInfoRepositoryInterface import FileInfoRepositoryInterface
from src.domain.repository.SettingsRepositoryInterface import SettingsRepositoryInterface
from src.domain.entity.DuplicateMatch import DuplicateMatch


class ListDuplicateTest(TestCase):
    def setUp(self):
        self.binary_comparator_mock = Mock(CompareBinary)
        self.file_info_repository_mock = Mock(FileInfoRepositoryInterface)
        self.settings_repository_mock = Mock(SettingsRepositoryInterface)

        self.list_duplicate = ListDuplicate(
            Mock(EventManagerInterface),
            self.settings_repository_mock,
            self.file_info_repository_mock,
            self.binary_comparator_mock,
            Mock(CompareFileName),
        )

        base_path = Path().resolve() / "tests/domain/service/DuplicateTest"
        self.file1_path = str(base_path / "testFile1.txt")
        self.file2_path = str(base_path / "testFile2.txt")
        self.file3_path = str(base_path / "testFile3.txt")

        self.file_info1 = self._create_file(self.file1_path, "TEST_FILE_CONTENT")
        self.file_info2 = self._create_file(self.file2_path, "TEST_FILE_CONTENT")
        self.file_info3 = self._create_file(self.file3_path, "TEST_FILE_CONTENT")

        super().setUp()

    def tearDown(self):
        if os_path.isfile(self.file1_path):
            os_remove(self.file1_path)
        if os_path.isfile(self.file2_path):
            os_remove(self.file2_path)
        if os_path.isfile(self.file3_path):
            os_remove(self.file3_path)

        super().tearDown()

    def test_given_two_files_with_same_content_when_comparing_files_then_a_duplicate_match_is_returned(self):
        self.settings_repository_mock.fetch_one.return_value = True
        self.binary_comparator_mock.compare.side_effect = False, True, True, False
        self.file_info_repository_mock.fetch_all_from_folder.return_value = [self.file_info1, self.file_info2, self.file_info3]

        duplicates = self.list_duplicate.list_duplicates()

        self.assertEqual(duplicates[0].files, [self.file_info2, self.file_info3])
        self.assertEqual(duplicates[0].duplicate_of, self.file_info1)

    def _create_file(self, file_path, file_contents):
        with open(file_path, "w") as file:
            file.write(file_contents)
        return FileInfo(
            file_path,
            os_path.basename(file_path),
            500,
            file_contents,
            file_contents,
        )
