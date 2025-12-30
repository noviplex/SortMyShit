from json import load as json_load, dumps as json_dumps

from src.domain.entity.Settings import Settings
from src.domain.repository.SettingsRepositoryInterface import SettingsRepositoryInterface


class SettingsRepository(SettingsRepositoryInterface):
    app_settings = Settings()
    runDir: str = None

    def fetch_all(self):
        try:
            with open(self.runDir + "/settings.json") as json_user_settings_file:
                user_settings = json_load(json_user_settings_file)
            return user_settings
        except FileNotFoundError:
            self.save_all(self.app_settings.default_user_settings)
            return self.app_settings.default_user_settings

    def fetch_one(self, name: str):
        user_settings = self.fetch_all()
        return user_settings[name]

    def save_all(self, user_settings):
        with open(self.runDir + "/settings.json", "w") as json_user_settings_file:
            json_user_settings_file.write(json_dumps(user_settings))

    def save_one(self, name: str, value: str):
        user_settings = self.fetch_all()
        user_settings[name] = value
        self.save_all(user_settings)
