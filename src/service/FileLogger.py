from datetime import datetime
from os import path as os_path, mkdir as os_mkdir

from src.event.LogActivityEvent import LogActivityEvent

from src.entity.Settings import Settings

from src.configuration.ServiceManager import ServiceManager

class FileLogger:

    def __init__(self, serviceManager: ServiceManager = ServiceManager()):
        self.logActivityEvent = serviceManager.get("LogActivityEvent") # type: LogActivityEvent
        self.settings = serviceManager.get("Settings") # type: Settings

    def activateLogging(self):
        self.logActivityEvent.subscribe(self.logInFile)

    def logInFile(self, logMessage):
        if not os_path.isdir(self.settings.runDir + "/log"):
            os_mkdir(self.settings.runDir + "/log")

        with open(self.settings.runDir + "/log/log.txt", "a") as file:
            file.write("[" + f"{datetime.now():%Y-%m-%d %H:%M:%S.%s}" + "] " + logMessage + "\n")
