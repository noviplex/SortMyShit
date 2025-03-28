from json import load as json_load, dumps as json_dumps

from src.entity.Settings import Settings

class SettingsService:
    appSettings = Settings()
    runDir = None

    def getSettings(self):
        try:
            jsonUserSettingsFile = open(self.runDir + "/settings.json")
            userSettings = json_load(jsonUserSettingsFile)
            jsonUserSettingsFile.close()
            return userSettings 
        except:
            self.saveSettings(self.appSettings.defaultUserSettings)
            return self.appSettings.defaultUserSettings
 
    def saveSettings(self, userSettings):
        jsonUserSettingsFile = open(self.runDir + "/settings.json", "w+")
        jsonUserSettingsFile.write(json_dumps(userSettings))
        jsonUserSettingsFile.close()

    def getSetting(self, name:str):
        userSettings = self.getSettings()
        return userSettings[name]

    def setSetting(self, name: str, value: str):
        userSettings = self.getSettings()
        userSettings[name] = value
        
        self.saveSettings(userSettings)


