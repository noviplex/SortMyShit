from os import path as os_path

from src.domain.event.EventManagerInterface import EventManagerInterface


class FileNameComparator:
    def __init__(
        self,
        eventManager: EventManagerInterface,
    ):
        self.eventManager = eventManager

    def compare(self, file1, file2):
        self.eventManager.trigger("status", "Comparing " + file2.fullPath + " with " + file1.fullPath)

        if (
            os_path.basename(file2.fullPath) == os_path.basename(file1.fullPath)
            and file2.fullPath != file1.fullPath
        ):
            return True

        return False
