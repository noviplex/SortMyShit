from unittest import TestCase
from unittest.mock import Mock

from src.domain.entity.FileInfo import FileInfo
from src.domain.service.compare.CompareFileName import CompareFileName
from src.domain.event.EventManagerInterface import EventManagerInterface


class FileNameComparatorTest(TestCase):
    def setUp(self):
        self.file1_path = "/tests/domain/service/CompareFileNameTest/testFile1.txt"
        self.file2_path = "/tests/domain/service/CompareFileNameTest/subfolder/testFile1.txt"

        self.file_name_comparator = CompareFileName(
            Mock(EventManagerInterface)
        )

        super().setUp()

    def test_given_two_different_file_names_in_different_folders_when_comparing_then_returns_true(self):
        self.assertTrue(
            self.file_name_comparator.compare(
                FileInfo(self.file1_path, "", 500, ""),
                FileInfo(self.file2_path, "", 500, ""),
            )
        )

    def test_given_twice_the_same_file_when_comparing_then_returns_false(self):
        self.assertFalse(
            self.file_name_comparator.compare(
                FileInfo(self.file1_path, "", 500, ""),
                FileInfo(self.file1_path, "", 500, ""),
            )
        )
