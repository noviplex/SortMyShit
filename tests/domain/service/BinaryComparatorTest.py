from unittest import TestCase
from unittest.mock import Mock

from pathlib import Path

from src.domain.entity.FileInfo import FileInfo
from src.domain.event.LogActivityEvent import LogActivityEvent
from src.domain.service.BinaryComparator import BinaryComparator


class BinaryComparatorTest(TestCase):
    def setUp(self):
        self.file1Path = str(Path().resolve()) + "/tests/domain/service/BinaryComparatorTest/testFile1.txt"
        self.file2Path = str(Path().resolve()) + "/tests/domain/service/BinaryComparatorTest/testFile2.txt"
        self.file3Path = str(Path().resolve()) + "/tests/domain/service/BinaryComparatorTest/testFile3.txt"

        self.binaryComparator = BinaryComparator(
            Mock(LogActivityEvent)
        )

        return super().setUp()

    def test_given_two_files_with_same_content_when_comparing_then_returns_true(self):
        file1 = open(self.file1Path)
        file2 = open(self.file2Path)

        file1Contents = file1.read()
        file2Contents = file2.read()

        file1.close()
        file2.close()

        self.assertTrue(self.binaryComparator.compare(
            FileInfo(self.file1Path, file1Contents),
            FileInfo(self.file2Path, file2Contents),
        ))

    def test_given_two_files_with_different_content_when_comparing_then_returns_false(self):
        file1 = open(self.file1Path)
        file3 = open(self.file3Path)

        file1Contents = file1.read()
        file3Contents = file3.read()

        file1.close()
        file3.close()

        self.assertFalse(self.binaryComparator.compare(
            FileInfo(self.file1Path, file1Contents),
            FileInfo(self.file3Path, file3Contents),
        ))

    def test_given_same_file_twice_when_comparing_then_returns_false(self):
        file1 = open(self.file1Path)
        file1Contents = file1.read()
        file1.close()

        self.assertFalse(self.binaryComparator.compare(
            FileInfo(self.file1Path, file1Contents),
            FileInfo(self.file1Path, file1Contents),
        ))
