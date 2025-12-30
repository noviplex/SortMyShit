from src.domain.repository.TmpStorageRepositoryInterface import TmpStorageRepositoryInterface


class TmpStorageRepository(TmpStorageRepositoryInterface):
    tmp_storage = {}

    def save_one(self, name: str, data):
        self.tmp_storage[name] = data

    def fetch_one(self, name: str):
        return self.tmp_storage[name]

    def remove_one(self, name: str):
        del self.tmp_storage[name]
