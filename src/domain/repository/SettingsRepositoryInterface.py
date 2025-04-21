from abc import ABC, abstractmethod


class SettingsRepositoryInterface(ABC):
    @abstractmethod
    def fetchAll(self):
        pass

    @abstractmethod
    def fetchOne(self, name: str):
        pass

    @abstractmethod
    def saveAll(self, settings):
        pass

    @abstractmethod
    def saveOne(self, name: str, setting: str):
        pass
