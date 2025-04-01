from abc import ABC, abstractmethod

class SettingsRepositoryInterface(ABC):
    @abstractmethod
    def loadAll(self):
        pass

    @abstractmethod
    def save(self, settings):
        pass

    @abstractmethod
    def loadOne(self, name: str):
        pass

    @abstractmethod
    def updateOne(self, name: str, setting: str):
        pass