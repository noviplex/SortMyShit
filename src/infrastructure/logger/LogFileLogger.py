from datetime import datetime
from os import path as os_path, mkdir as os_mkdir

from src.application.service.EventManager import EventManager

from src.infrastructure.repository.SettingsRepository import SettingsRepository


class LogFileLogger:
    def __init__(
            self,
            eventManager: EventManager,
            settingsRepository: SettingsRepository,
    ):
        self.eventManager = eventManager
        self.settingsRepository = settingsRepository

    def activateLogging(self):
        self.eventManager.subscribe("status", self.logInFile)
        self.eventManager.subscribe("output", self.logInFile)

    def logInFile(self, logMessage):
        if not os_path.isdir(self.settingsRepository.runDir + "/log"):
            os_mkdir(self.settingsRepository.runDir + "/log")

        with open(self.settingsRepository.runDir + "/log/log.txt", "a") as file:
            file.write("[" + f"{datetime.now():%Y-%m-%d %H:%M:%S.%s}" + "] " + logMessage + "\n")
