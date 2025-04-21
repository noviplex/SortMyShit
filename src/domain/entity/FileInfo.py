class FileInfo:
    def __init__(
        self,
        fullPath: str,
        fileName: str,
        size: int,
        partialContents: str,
        contents: str = None
    ):
        self.fullPath = fullPath
        self.fileName = fileName
        self.size = size
        self.partialContents = partialContents
        self.contents = contents
