from src.domain.event.EventManagerInterface import EventManagerInterface
from src.domain.entity.FileInfo import FileInfo


class FileNameComparator:
    def __init__(
        self,
        eventManager: EventManagerInterface,
    ):
        self.eventManager = eventManager

    def compare(self, file1: FileInfo, file2: FileInfo):
        self.eventManager.trigger("status", "Comparing " + file2.fullPath + " with " + file1.fullPath)

        if (file2.fileName == file1.fileName and file2.fullPath != file1.fullPath):
            return True

        return False
