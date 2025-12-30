class FileInfo:
    def __init__(
        self,
        full_path: str,
        file_name: str,
        size: int,
        partial_contents: str,
        contents: str = None
    ):
        self.full_path = full_path
        self.file_name = file_name
        self.size = size
        self.partial_contents = partial_contents
        self.contents = contents
