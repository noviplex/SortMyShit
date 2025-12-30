from unittest import TestCase
from unittest.mock import Mock
from pathlib import Path
from os import path as os_path, remove as os_remove

from src.domain.entity.FileInfo import FileInfo
from src.domain.event.EventManagerInterface import EventManagerInterface
from src.domain.service.remove.RemoveDuplicate import RemoveDuplicate
from src.domain.repository.FileInfoRepositoryInterface import FileInfoRepositoryInterface
from src.domain.entity.DuplicateMatch import DuplicateMatch


class RemoveDuplicateTest(TestCase):
    def setUp(self):
        self.file_info_repository_mock = Mock(FileInfoRepositoryInterface)
        self.remove_duplicate = RemoveDuplicate(
            self.file_info_repository_mock,
            Mock(EventManagerInterface),
        )

        base_path = Path().resolve() / "tests/domain/service/DuplicateTest"
        self.file1_path = str(base_path / "testFile1.txt")
        self.file2_path = str(base_path / "testFile2.txt")

        self.file_info1 = self._create_file(self.file1_path, "TEST_FILE_CONTENT")
        self.file_info2 = self._create_file(self.file2_path, "TEST_FILE_CONTENT")

        super().setUp()

    def tearDown(self):
        if os_path.isfile(self.file1_path):
            os_remove(self.file1_path)
        if os_path.isfile(self.file2_path):
            os_remove(self.file2_path)

        super().tearDown()

    def test_given_two_files_with_same_content_when_comparing_files_then_one_copy_is_deleted(self):
        self.remove_duplicate.remove_duplicates(
            [DuplicateMatch([self.file_info1], self.file_info2)]
        )

        self.file_info_repository_mock.remove_one.assert_called_once_with(self.file1_path)

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
