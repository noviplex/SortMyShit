from datetime import datetime
from os import path as os_path, mkdir as os_mkdir

from src.event.LogActivityEvent import LogActivityEvent

from src.service.SettingsService import SettingsService

class FileLogger:

    def __init__(
            self, 
            logactivityEvent: LogActivityEvent,
            settingsService: SettingsService
    ):
        self.logActivityEvent = logactivityEvent
        self.settingsService = settingsService

    def activateLogging(self):
        self.logActivityEvent.subscribe(self.logInFile)

    def logInFile(self, logMessage):
        if not os_path.isdir(self.settingsService.runDir + "/log"):
            os_mkdir(self.settingsService.runDir + "/log")

        with open(self.settingsService.runDir + "/log/log.txt", "a") as file:
            file.write("[" + f"{datetime.now():%Y-%m-%d %H:%M:%S.%s}" + "] " + logMessage + "\n")