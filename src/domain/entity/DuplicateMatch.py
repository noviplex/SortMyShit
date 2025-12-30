from src.domain.entity.FileInfo import FileInfo


class DuplicateMatch:
    def __init__(self, files: list[FileInfo], duplicate_of: FileInfo):
        self.files = files
        self.duplicate_of = duplicate_of
