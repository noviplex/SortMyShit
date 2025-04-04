from src.domain.event.EventManagerInterface import EventManagerInterface
from src.domain.entity.FileInfo import FileInfo


class BinaryComparator:
    def __init__(
        self,
        eventManager: EventManagerInterface,
    ):
        self.eventManager = eventManager

    def compare(self, file1: FileInfo, file2: FileInfo):
        self.eventManager.trigger("status", "Comparing " + file2.fullPath + " with " + file1.fullPath)

        if (
            file2.fullPath != file1.fullPath
            and file2.partialContents == file1.partialContents
        ):
            file1Content = self.__getFileContent(file1.fullPath)
            file2Content = self.__getFileContent(file2.fullPath)

            if (file1Content == file2Content):
                return True

        return False

    def __getFileContent(self, filePath: str):
        fileOpened = open(filePath, 'rb')
        fileContent = fileOpened.read()
        fileOpened.close()

        return fileContent
