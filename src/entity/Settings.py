from json import load as json_load, dumps as json_dumps

class Settings:
    runDir = None
    folderToProcess = "" # TODO: add field in settings interface to make it dynamic
    destinationFolder = "" # TODO: add field in settings interface to make it dynamic
    defaultTypeMapping = {
        "docs": ["pdf", "pdf_lbk", "doc", "docx", "xls", "xlsx", "ppt", "pptx", "txt", "odt", "ods", "odp"],
        "pics": ["jpg", "jpg_lbk", "jpeg", "jpeg_lbk", "png", "gif", "webp"],
        "compressed": ["zip", "rar", "tar", "gz", "7z", "xz", "bz2"],
        "audio": ["mp3", "wma", "wav", "flac", "ogg", "m4a", "m4a_lbk", "aac"],
        "video": ["m4v", "webm", "mp4", "avi", "mkv", "flv", "mov", "wmv"],
        "software": ["deb", "exe", "dmg", "pkg", "iso", "img", "apk", "rpm", "pat"],
        "configuration": ["json", "so", "ovpn"],
    }
    fontColor = "#BDB6D0"
    backgroundColor = "#46464C"
    settings = None,
    defaultSettings = {
        "binarySearch": True, 
        "binarySearchLargeFiles": False, 
        "keepOriginalFiles": True, 
        "logOutputInFile": True, 
        "askBeforeRemovingDuplicates": True,
        "askBeforeRemovingEmptyFolders": True,
        "binaryComparisonLargeFilesThreshold": 5000000
    }

    def getSettings(self):
        try:
            jsonSettingsFile = open(self.runDir + "/settings.json")
            self.settings = json_load(jsonSettingsFile)
            jsonSettingsFile.close()
        except:
            self.saveSettings(self.defaultSettings)
            self.settings = self.defaultSettings

        return self.settings
 
    def saveSettings(self, settings):
        jsonSettingsFile = open(self.runDir + "/settings.json", "w+")
        jsonSettingsFile.write(json_dumps(settings))
        jsonSettingsFile.close()

    def getSetting(self, name:str):
        settings = self.getSettings()
        return settings[name]

    def setSetting(self, name: str, value: str):
        settings = self.getSettings()
        settings[name] = value
        
        self.saveSettings(settings)


