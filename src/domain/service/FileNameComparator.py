from os import path as os_path

from src.domain.event.LogActivityEvent import LogActivityEvent

class FileNameComparator:
    def __init__(
        self,
        logActivityEvent: LogActivityEvent,
    ):
        self.logActivityEvent = logActivityEvent

    def compare(self, file1, file2):
        self.logActivityEvent.trigger("Comparing " + file2.fullPath + " with " + file1.fullPath)
                
        if (
            os_path.basename(file2.fullPath) == os_path.basename(file1.fullPath) 
            and file2.fullPath != file1.fullPath
        ):
            return True
        
        return False