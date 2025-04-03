from src.domain.entity.FileInfo import FileInfo
from src.domain.event.LogActivityEvent import LogActivityEvent


class BinaryComparator:
    def __init__(
        self,
        logActivityEvent: LogActivityEvent,
    ):
        self.logActivityEvent = logActivityEvent

    def compare(self, file1: FileInfo, file2: FileInfo):
        self.logActivityEvent.trigger("Comparing " + file2.fullPath + " with " + file1.fullPath)

        if (
            file2.fullPath != file1.fullPath
            and file2.partialContents == file1.partialContents
        ):
            fileOpened = open(file1.fullPath, 'rb')
            file2Opened = open(file2.fullPath, 'rb')

            if (fileOpened.read() == file2Opened.read()):
                return True
            fileOpened.close()
            file2Opened.close()

        return False
