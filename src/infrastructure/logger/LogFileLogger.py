from datetime import datetime
from os import path as os_path, mkdir as os_mkdir

from src.application.service.EventManager import EventManager
from src.infrastructure.repository.SettingsRepository import SettingsRepository


class LogFileLogger:
    def __init__(
        self,
        event_manager: EventManager,
        settings_repository: SettingsRepository,
    ):
        self.event_manager = event_manager
        self.settings_repository = settings_repository

    def activate_logging(self):
        self.event_manager.subscribe("status", self.log_in_file)
        self.event_manager.subscribe("output", self.log_in_file)

    def log_in_file(self, log_message):
        log_dir = os_path.join(self.settings_repository.runDir, "log")
        log_file = os_path.join(log_dir, "log.txt")

        if not os_path.isdir(log_dir):
            os_mkdir(log_dir)

        with open(log_file, "a") as file:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            file.write(f"[{timestamp}] {log_message}\n")
