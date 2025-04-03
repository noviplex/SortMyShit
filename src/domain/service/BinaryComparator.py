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
            file1Content = self.__getFileContent(file1.fullPath)
            file2Content = self.__getFileContent(file2.fullPath)

            if (file1Content == file2Content):
                return True

        return False

    def __getFileContent(self, filePath):
        fileOpened = open(filePath, 'rb')
        fileContent = fileOpened.read()
        fileOpened.close()

        return fileContent
