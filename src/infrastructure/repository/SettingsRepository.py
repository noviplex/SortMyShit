from json import load as json_load, dumps as json_dumps

from src.domain.entity.Settings import Settings
from src.domain.repository.SettingsRepositoryInterface import SettingsRepositoryInterface


class SettingsRepository(SettingsRepositoryInterface):
    appSettings = Settings()
    runDir: str = None

    def fetchAll(self):
        try:
            jsonUserSettingsFile = open(self.runDir + "/settings.json")
            userSettings = json_load(jsonUserSettingsFile)
            jsonUserSettingsFile.close()
            return userSettings
        except FileNotFoundError:
            self.saveAll(self.appSettings.defaultUserSettings)
            return self.appSettings.defaultUserSettings

    def fetchOne(self, name: str):
        userSettings = self.fetchAll()
        return userSettings[name]

    def saveAll(self, userSettings):
        jsonUserSettingsFile = open(self.runDir + "/settings.json", "w+")
        jsonUserSettingsFile.write(json_dumps(userSettings))
        jsonUserSettingsFile.close()

    def saveOne(self, name: str, value: str):
        userSettings = self.fetchAll()
        userSettings[name] = value

        self.saveAll(userSettings)
