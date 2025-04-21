from unittest import TestCase
from unittest.mock import Mock
from pathlib import Path
from os import path as os_path, remove as os_remove

from src.domain.entity.FileInfo import FileInfo
from src.domain.event.EventManagerInterface import EventManagerInterface
from src.domain.service.BinaryComparator import BinaryComparator
from src.domain.service.DuplicateRemover import DuplicateRemover
from src.domain.service.FileNameComparator import FileNameComparator
from src.domain.repository.FileInfoRepositoryInterface import FileInfoRepositoryInterface


class DuplicateRemoverTest(TestCase):
    def setUp(self):
        self.binaryComparatorMock = Mock(BinaryComparator)
        self.fileInfoRepositoryMock = Mock(FileInfoRepositoryInterface)
        self.duplicateRemover = DuplicateRemover(
            self.binaryComparatorMock,
            Mock(FileNameComparator),
            Mock(EventManagerInterface),
            self.fileInfoRepositoryMock,
        )

        self.file1Path = str(Path().resolve()) + "/tests/domain/service/DuplicateRemoverTest/testFile1.txt"
        self.file2Path = str(Path().resolve()) + "/tests/domain/service/DuplicateRemoverTest/testFile2.txt"

        self.fileInfo1 = self.__createFile(self.file1Path, "TEST_FILE_CONTENT")
        self.fileInfo2 = self.__createFile(self.file2Path, "TEST_FILE_CONTENT")

        return super().setUp()

    def tearDown(self):
        if os_path.isfile(self.file1Path):
            os_remove(self.file1Path)
        os_remove(self.file2Path)

        return super().tearDown()

    def test_given_two_files_with_same_content_when_comparing_files_then_one_copy_is_deleted(self):
        self.binaryComparatorMock.compare.return_value = True

        self.duplicateRemover.removeFilesByIdenticalBinaryContent([self.fileInfo1, self.fileInfo2], self.fileInfo1)

        self.fileInfoRepositoryMock.removeOne.assert_called_once_with(self.file1Path)

    def test_given_two_files_with_different_content_when_using_file_that_does_not_exist_then_skip(self):
        self.duplicateRemover.removeFilesByIdenticalBinaryContent(
            [self.fileInfo1, self.fileInfo2],
            FileInfo("non_existing_file.txt", "non_existing_file.txt", 500, "", "")
        )

        self.fileInfoRepositoryMock.removeOne.assert_not_called()

    def test_given_two_files_with_different_content_when_comparing_files_that_are_above_size_threshold_then_both_files_are_kept(self):
        self.binaryComparatorMock.compare.return_value = False

        self.duplicateRemover.removeFilesByIdenticalBinaryContent([self.fileInfo1, self.fileInfo2], self.fileInfo1)

        self.fileInfoRepositoryMock.removeOne.assert_not_called()

    def __createFile(self, filePath, fileContents):
        file = open(filePath, "w")
        file.write(fileContents)
        file.close()

        return FileInfo(filePath, os_path.basename(filePath), 500, fileContents, fileContents)
