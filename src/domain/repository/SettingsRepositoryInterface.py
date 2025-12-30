from abc import ABC, abstractmethod


class SettingsRepositoryInterface(ABC):
    @abstractmethod
    def fetch_all(self):
        pass

    @abstractmethod
    def fetch_one(self, name: str):
        pass

    @abstractmethod
    def save_all(self, settings):
        pass

    @abstractmethod
    def save_one(self, name: str, setting: str):
        pass
