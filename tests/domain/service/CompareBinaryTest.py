from unittest import TestCase
from unittest.mock import Mock
from pathlib import Path

from src.domain.entity.FileInfo import FileInfo
from src.domain.event.EventManagerInterface import EventManagerInterface
from src.domain.repository.FileInfoRepositoryInterface import FileInfoRepositoryInterface
from src.domain.repository.SettingsRepositoryInterface import SettingsRepositoryInterface
from src.domain.service.compare.CompareBinary import CompareBinary


class BinaryComparatorTest(TestCase):
    def setUp(self):
        base_path = Path().resolve() / "tests/domain/service/CompareBinaryTest"
        self.file1_path = str(base_path / "testFile1.txt")
        self.file2_path = str(base_path / "testFile2.txt")
        self.file3_path = str(base_path / "testFile3.txt")

        self.settings_repository_mock = Mock(SettingsRepositoryInterface)

        self.binary_comparator = CompareBinary(
            Mock(EventManagerInterface),
            Mock(FileInfoRepositoryInterface),
            self.settings_repository_mock,
        )

        super().setUp()

    def test_given_two_files_with_same_content_when_comparing_then_returns_true(self):
        file1_contents = self._get_file_contents(self.file1_path)
        file2_contents = self._get_file_contents(self.file2_path)

        self.settings_repository_mock.fetch_one.side_effect = [50000, True, 50000, True]

        self.assertTrue(self.binary_comparator.compare(
            FileInfo(self.file1_path, "", 500, file1_contents),
            FileInfo(self.file2_path, "", 500, file2_contents),
        ))

    def test_given_two_oversized_files_with_same_content_when_comparing_then_with_large_file_search_enabled_returns_true(self):
        file1_contents = self._get_file_contents(self.file1_path)
        file2_contents = self._get_file_contents(self.file2_path)

        self.settings_repository_mock.fetch_one.side_effect = [50000, True, 50000, True]

        self.assertTrue(self.binary_comparator.compare(
            FileInfo(self.file1_path, "", 55000, file1_contents),
            FileInfo(self.file2_path, "", 55000, file2_contents),
        ))

    def test_given_two_oversized_files_with_same_content_when_comparing_then_with_large_file_search_disabled_returns_false(self):
        file1_contents = self._get_file_contents(self.file1_path)
        file2_contents = self._get_file_contents(self.file2_path)

        self.settings_repository_mock.fetch_one.side_effect = [50000, False, 50000, False]

        self.assertFalse(self.binary_comparator.compare(
            FileInfo(self.file1_path, "", 55000, file1_contents),
            FileInfo(self.file2_path, "", 55000, file2_contents),
        ))

    def test_given_two_files_with_different_content_when_comparing_then_returns_false(self):
        file1_contents = self._get_file_contents(self.file1_path)
        file3_contents = self._get_file_contents(self.file3_path)

        self.settings_repository_mock.fetch_one.side_effect = [50000, True, 50000, True]

        self.assertFalse(self.binary_comparator.compare(
            FileInfo(self.file1_path, "", 500, file1_contents),
            FileInfo(self.file3_path, "", 500, file3_contents),
        ))

    def test_given_same_file_twice_when_comparing_then_returns_false(self):
        file1_contents = self._get_file_contents(self.file1_path)

        self.settings_repository_mock.fetch_one.side_effect = [50000, True, 50000, True]

        self.assertFalse(self.binary_comparator.compare(
            FileInfo(self.file1_path, "", 500, file1_contents),
            FileInfo(self.file1_path, "", 500, file1_contents),
        ))

    def _get_file_contents(self, file_path: str):
        with open(file_path) as file:
            return file.read()
