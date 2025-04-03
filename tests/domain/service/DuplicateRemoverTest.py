from unittest import TestCase
from unittest.mock import Mock, create_autospec
from pathlib import Path
from os import path as os_path, remove as os_remove

from src.domain.entity.FileInfo import FileInfo
from src.domain.event.RemoveDuplicatesEvent import RemoveDuplicatesEvent
from src.domain.event.LogActivityEvent import LogActivityEvent
from src.domain.service.BinaryComparator import BinaryComparator
from src.domain.service.DuplicateRemover import DuplicateRemover
from src.domain.service.FileNameComparator import FileNameComparator
from src.domain.repository.SettingsRepositoryInterface import SettingsRepositoryInterface

class DuplicateRemoverTest(TestCase):
    def setUp(self):
        self.binaryComparatorMock = Mock(BinaryComparator)
        self.settingsRepositoryMock = Mock(SettingsRepositoryInterface)
        
        self.duplicateRemover = DuplicateRemover(
            Mock(LogActivityEvent),
            Mock(RemoveDuplicatesEvent),
            self.binaryComparatorMock,
            Mock(FileNameComparator),
            self.settingsRepositoryMock
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
        self.binaryComparatorMock.compare.side_effect = [True]
        self.settingsRepositoryMock.loadOne.side_effect = [50000, True]

        self.duplicateRemover.removeFilesByIdenticalBinaryContent([self.fileInfo1, self.fileInfo2], self.fileInfo1)

        self.assertFalse((os_path.isfile(self.file1Path)))
        self.assertTrue((os_path.isfile(self.file2Path)))

    def test_given_two_files_with_different_content_when_comparing_files_then_both_files_are_kept(self):
        self.binaryComparatorMock.compare.side_effect = [False, False]
        self.settingsRepositoryMock.loadOne.side_effect = [50000, True, 50000, True]

        self.duplicateRemover.removeFilesByIdenticalBinaryContent([self.fileInfo1, self.fileInfo2], self.fileInfo1)

        self.assertTrue((os_path.isfile(self.file1Path)))
        self.assertTrue((os_path.isfile(self.file2Path)))

    def test_given_two_files_with_different_content_when_comparing_files_that_are_above_size_threshold_then_both_files_are_kept(self):
        self.binaryComparatorMock.compare.side_effect = [True, True]
        self.settingsRepositoryMock.loadOne.side_effect = [1, False, 1, False]

        self.duplicateRemover.removeFilesByIdenticalBinaryContent([self.fileInfo1, self.fileInfo2], self.fileInfo1)

        self.assertTrue((os_path.isfile(self.file1Path)))
        self.assertTrue((os_path.isfile(self.file2Path)))

    def __createFile(self, filePath, fileContents):
        file = open(filePath, "w")
        file.write(fileContents)
        file.close()

        return FileInfo(filePath, fileContents)