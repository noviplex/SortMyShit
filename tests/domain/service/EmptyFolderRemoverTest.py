from unittest import TestCase
from unittest.mock import Mock, create_autospec
from pathlib import Path
from os import path as os_path, remove as os_remove, makedirs as os_makedirs, rmdir as os_rmdir

from src.domain.entity.FileInfo import FileInfo
from src.domain.event.LogActivityEvent import LogActivityEvent
from src.domain.event.RemoveEmptyFoldersEvent import RemoveEmptyFoldersEvent
from src.domain.service.EmptyFolderRemover import EmptyFolderRemover
from src.domain.repository.SettingsRepositoryInterface import SettingsRepositoryInterface

class EmptyFolderRemoverTest(TestCase):
    def setUp(self):
        rootFolder = str(Path().resolve()) + "/tests/domain/service/EmptyFolderRemoverTest"
        self.emptyFolderPath = rootFolder + "/TestEmptyFolder"
        self.notEmptyFolderPath = rootFolder + "/TestNotEmptyFolder"

        self.__clearFolders()

        os_makedirs(self.emptyFolderPath)
        os_makedirs(self.notEmptyFolderPath)

        self.fileInfo1 = self.__createFile(self.notEmptyFolderPath + "/filetest.txt", "TEST_FILE_CONTENT")

        settingsRepositoryMock = Mock(SettingsRepositoryInterface)
        settingsRepositoryMock.loadOne.side_effect = [rootFolder]

        self.emptyFolderRemover = EmptyFolderRemover(
            Mock(LogActivityEvent),
            Mock(RemoveEmptyFoldersEvent),
            settingsRepositoryMock,
        )

        return super().setUp()
    
    def tearDown(self):
        self.__clearFolders()

        return super().tearDown()

    def test_given_folders_when_empty_folders_are_present_then_only_empty_folders_removed(self):
        self.emptyFolderRemover.removeEmptyFolders()
        
        self.assertTrue(os_path.isdir(self.notEmptyFolderPath))
        self.assertFalse(os_path.isdir(self.emptyFolderPath))

    def __createFile(self, filePath, fileContents):
        file = open(filePath, "w")
        file.write(fileContents)
        file.close()

        return FileInfo(filePath, fileContents)
    
    def __clearFolders(self):
        if (os_path.isdir(self.emptyFolderPath)):
            os_rmdir(self.emptyFolderPath)
        if (os_path.isdir(self.notEmptyFolderPath)):
            os_remove(self.notEmptyFolderPath + "/filetest.txt")
            os_rmdir(self.notEmptyFolderPath)
