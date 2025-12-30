from src.domain.event.EventManagerInterface import EventManagerInterface
from src.domain.entity.FileInfo import FileInfo


class CompareFileName:
    def __init__(
        self,
        event_manager: EventManagerInterface,
    ):
        self.event_manager = event_manager

    def compare(self, file1: FileInfo, file2: FileInfo) -> bool:
        self.event_manager.trigger(
            "status",
            f"Comparing {file2.full_path} with {file1.full_path}"
        )

        if file2.file_name == file1.file_name and file2.full_path != file1.full_path:
            return True

        return False
