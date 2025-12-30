from tkinter import Toplevel

from src.application.component.SMSImageDisplay import SMSImageDisplay


class SMSImagePreviewModal(Toplevel):
    def __init__(self, master, bg, file_name: str, full_path: str):
        super().__init__(master)
        self.title(file_name)
        SMSImageDisplay(self, full_path, 600, 600).pack(padx=30, pady=20)
        self.grab_set()
