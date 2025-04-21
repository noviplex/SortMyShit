from unittest import TestCase
from unittest.mock import Mock

from pathlib import Path

from src.domain.entity.FileInfo import FileInfo
from src.domain.event.EventManagerInterface import EventManagerInterface
from src.domain.repository.FileInfoRepositoryInterface import FileInfoRepositoryInterface
from src.domain.repository.SettingsRepositoryInterface import SettingsRepositoryInterface
from src.domain.service.BinaryComparator import BinaryComparator


class BinaryComparatorTest(TestCase):
    def setUp(self):
        self.file1Path = str(Path().resolve()) + "/tests/domain/service/BinaryComparatorTest/testFile1.txt"
        self.file2Path = str(Path().resolve()) + "/tests/domain/service/BinaryComparatorTest/testFile2.txt"
        self.file3Path = str(Path().resolve()) + "/tests/domain/service/BinaryComparatorTest/testFile3.txt"

        self.settingsRepositoryMock = Mock(SettingsRepositoryInterface)

        self.binaryComparator = BinaryComparator(
            Mock(EventManagerInterface),
            Mock(FileInfoRepositoryInterface),
            self.settingsRepositoryMock,
        )

        return super().setUp()

    def test_given_two_files_with_same_content_when_comparing_then_returns_true(self):
        file1Contents = self.__getFileContents(self.file1Path)
        file2Contents = self.__getFileContents(self.file2Path)

        self.settingsRepositoryMock.fetchOne.side_effect = [50000, True, 50000, True]

        self.assertTrue(self.binaryComparator.compare(
            FileInfo(self.file1Path, "", 500, file1Contents),
            FileInfo(self.file2Path, "", 500, file2Contents),
        ))

    def test_given_two_oversized_files_with_same_content_when_comparing_then_with_large_file_search_enabled_returns_true(self):
        file1Contents = self.__getFileContents(self.file1Path)
        file2Contents = self.__getFileContents(self.file2Path)

        self.settingsRepositoryMock.fetchOne.side_effect = [50000, True, 50000, True]

        self.assertTrue(self.binaryComparator.compare(
            FileInfo(self.file1Path, "", 55000, file1Contents),
            FileInfo(self.file2Path, "", 55000, file2Contents),
        ))

    def test_given_two_oversized_files_with_same_content_when_comparing_then_with_large_file_search_disabled_returns_false(self):
        file1Contents = self.__getFileContents(self.file1Path)
        file2Contents = self.__getFileContents(self.file2Path)

        self.settingsRepositoryMock.fetchOne.side_effect = [50000, False, 50000, False]

        self.assertFalse(self.binaryComparator.compare(
            FileInfo(self.file1Path, "", 55000, file1Contents),
            FileInfo(self.file2Path, "", 55000, file2Contents),
        ))

    def test_given_two_files_with_different_content_when_comparing_then_returns_false(self):
        file1Contents = self.__getFileContents(self.file1Path)
        file3Contents = self.__getFileContents(self.file3Path)

        self.settingsRepositoryMock.fetchOne.side_effect = [50000, True, 50000, True]

        self.assertFalse(self.binaryComparator.compare(
            FileInfo(self.file1Path, "", 500, file1Contents),
            FileInfo(self.file3Path, "", 500, file3Contents),
        ))

    def test_given_same_file_twice_when_comparing_then_returns_false(self):
        file1Contents = self.__getFileContents(self.file1Path)

        self.settingsRepositoryMock.fetchOne.side_effect = [50000, True, 50000, True]

        self.assertFalse(self.binaryComparator.compare(
            FileInfo(self.file1Path, "", 500, file1Contents),
            FileInfo(self.file1Path, "", 500, file1Contents),
        ))

    def __getFileContents(self, filePath: str):
        file = open(filePath)
        fileContents = file.read()
        file.close()

        return fileContents
