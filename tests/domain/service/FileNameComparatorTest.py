from unittest import TestCase
from unittest.mock import Mock

from src.domain.entity.FileInfo import FileInfo
from src.domain.service.FileNameComparator import FileNameComparator
from src.domain.event.EventManagerInterface import EventManagerInterface


class FileNameComparatorTest(TestCase):
    def setUp(self):
        self.file1Path = "/tests/domain/service/FileNameComparatorTest/testFile1.txt"
        self.file2Path = "/tests/domain/service/FileNameComparatorTest/subfolder/testFile1.txt"

        self.binaryComparator = FileNameComparator(
            Mock(EventManagerInterface)
        )

        return super().setUp()

    def test_given_two_different_fileNames_in_different_folders_when_comparing_then_returns_true(self):
        self.assertTrue(self.binaryComparator.compare(
            FileInfo(self.file1Path, ""),
            FileInfo(self.file2Path, ""),
        ))

    def test_given_twice_the_same_file_when_comparing_then_returns_false(self):
        self.assertFalse(self.binaryComparator.compare(
            FileInfo(self.file1Path, ""),
            FileInfo(self.file1Path, ""),
        ))
