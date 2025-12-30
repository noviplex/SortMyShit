from abc import ABC, abstractmethod


class TmpStorageRepositoryInterface(ABC):
    @abstractmethod
    def fetch_one(self, name: str):
        pass

    @abstractmethod
    def remove_one(self, name: str):
        pass
