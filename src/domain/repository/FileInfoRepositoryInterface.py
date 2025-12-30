from abc import ABC, abstractmethod

from src.domain.entity.FileInfo import FileInfo


class FileInfoRepositoryInterface(ABC):
    @abstractmethod
    def fetch_all_from_folder(self, folder_path: str) -> list[FileInfo]:
        pass

    @abstractmethod
    def fetch_one(
        self, full_path: str, with_full_contents: bool = False, read_mode: str = "rb"
    ) -> FileInfo:
        pass

    @abstractmethod
    def remove_one(self, file_path: str):
        pass
