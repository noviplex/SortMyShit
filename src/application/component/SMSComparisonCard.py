from tkinter import Frame

from src.application.component.SMSLabel import SMSLabel
from src.domain.entity.FileInfo import FileInfo
from src.domain.entity.DuplicateMatch import DuplicateMatch


class SMSComparisonCard(Frame):
    def __init__(
        self,
        master,
        duplicate_match: DuplicateMatch,
        bg: str,
        fg: str,
        border_color: str,
    ):
        super().__init__(
            master,
            background=bg,
        )
        self.fg = fg
        self.bg = bg
        self.border_color = border_color

        SMSLabel(
            self,
            text="Kept File",
            bg=self.bg,
            fg=self.fg,
            font=("Arial", 14),
        ).grid(padx=10, pady=10, row=0, column=0, sticky='w')

        SMSLabel(
            self,
            text="Duplicates",
            bg=self.bg,
            fg=self.fg,
            font=("Arial", 14),
        ).grid(padx=10, pady=10, row=0, column=1, sticky='w')

        self.__create_comparison_card(duplicate_match.duplicate_of).grid(padx=10, pady=5, row=1, column=0)
        row: int = 1
        for file in duplicate_match.files:
            self.__create_comparison_card(file).grid(padx=10, pady=5, row=row, column=1)
            row += 1

    def __create_comparison_card(self, file: FileInfo):
        text_container = Frame(self, width=570, height=40, background=self.border_color)
        text_container.grid_propagate(0)
        text_container.grid(row=0, column=0, padx=10, pady=10, sticky='w')

        SMSLabel(
            text_container,
            text=file.file_name,
            bg=self.border_color,
            fg=self.fg,
            font=("Arial", 12),
        ).grid(row=0, column=0, sticky='w')

        return text_container
