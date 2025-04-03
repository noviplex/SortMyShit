from json import load as json_load, dumps as json_dumps

from src.domain.entity.Settings import Settings
from src.domain.repository.SettingsRepositoryInterface import SettingsRepositoryInterface


class SettingsRepository(SettingsRepositoryInterface):
    appSettings = Settings()
    runDir: str = None

    def loadAll(self):
        try:
            jsonUserSettingsFile = open(self.runDir + "/settings.json")
            userSettings = json_load(jsonUserSettingsFile)
            jsonUserSettingsFile.close()
            return userSettings
        except FileNotFoundError:
            self.save(self.appSettings.defaultUserSettings)
            return self.appSettings.defaultUserSettings

    def save(self, userSettings):
        jsonUserSettingsFile = open(self.runDir + "/settings.json", "w+")
        jsonUserSettingsFile.write(json_dumps(userSettings))
        jsonUserSettingsFile.close()

    def loadOne(self, name: str):
        userSettings = self.loadAll()
        return userSettings[name]

    def updateOne(self, name: str, value: str):
        userSettings = self.loadAll()
        userSettings[name] = value

        self.save(userSettings)
