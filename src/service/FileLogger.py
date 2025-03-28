from datetime import datetime
from os import path as os_path, mkdir as os_mkdir

from src.event.LogActivityEvent import LogActivityEvent

from src.service.SettingsService import SettingsService

from src.configuration.ServiceManager import ServiceManager

class FileLogger:

    def __init__(self, serviceManager: ServiceManager = ServiceManager()):
        self.logActivityEvent = serviceManager.get("LogActivityEvent") # type: LogActivityEvent
        self.settingsService = serviceManager.get("SettingsService") # type: SettingsService

    def activateLogging(self):
        self.logActivityEvent.subscribe(self.logInFile)

    def logInFile(self, logMessage):
        if not os_path.isdir(self.settingsService.runDir + "/log"):
            os_mkdir(self.settingsService.runDir + "/log")

        with open(self.settingsService.runDir + "/log/log.txt", "a") as file:
            file.write("[" + f"{datetime.now():%Y-%m-%d %H:%M:%S.%s}" + "] " + logMessage + "\n")
