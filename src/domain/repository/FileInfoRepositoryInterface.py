from abc import ABC, abstractmethod

from src.domain.entity.FileInfo import FileInfo


class FileInfoRepositoryInterface(ABC):
    @abstractmethod
    def fetchAllFromFolder(self, folderPath: str) -> list[FileInfo]:
        pass

    @abstractmethod
    def fetchOne(self, fullPath: str, withFullContents: bool = False, readMode: str = "rb") -> FileInfo:
        pass

    @abstractmethod
    def removeOne(self, filePath: str):
        pass
