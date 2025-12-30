from tkinter import Tk, constants as tk_constants

from src.application.component.SMSTextBox import SMSTextBox
from src.application.component.SMSLabel import SMSLabel
from src.application.service.EventManager import EventManager
from src.application.view.SMSView import SMSView

from src.domain.service.sort.SortFile import SortFile
from src.domain.service.list.ListDuplicate import ListDuplicate
from src.domain.service.remove.RemoveEmptyFolder import RemoveEmptyFolder
from src.domain.service.remove.RemoveEmptyFile import RemoveEmptyFile

from src.infrastructure.repository.SettingsRepository import SettingsRepository


class ConsoleView(SMSView):
    def __init__(
        self,
        container: Tk,
        settings_repository: SettingsRepository,
        list_duplicates: ListDuplicate,
        empty_folder_remover: RemoveEmptyFolder,
        empty_file_remover: RemoveEmptyFile,
        file_sorter: SortFile,
        event_manager: EventManager
    ):
        self.settings_repository = settings_repository
        self.list_duplicates = list_duplicates
        self.empty_file_remover = empty_file_remover
        self.empty_folder_remover = empty_folder_remover
        self.file_sorter = file_sorter
        self.event_manager = event_manager

        self.color1 = self.settings_repository.fetch_one("color1")
        self.color2 = self.settings_repository.fetch_one("color2")
        self.color3 = self.settings_repository.fetch_one("color3")
        self.color4 = self.settings_repository.fetch_one("color4")

        super().__init__(
            container=container,
            bg=self.color1
        )

        self.create_view()

    def create_view(self):
        self.event_manager.subscribe("output", self.__show_entry_in_main_output)

        SMSLabel(
            container=self,
            bg=self.color1,
            fg=self.color4,
            text="Console Output",
            font=("Arial", 24)
        ).grid(row=0, column=0, sticky='w')

        self.output = SMSTextBox(
            container=self,
            bg=self.color3,
            fg=self.color4,
            border_color=self.color2,
            height=35,
            width=115,
        )
        self.output.grid(column=1, row=1)

    def __show_entry_in_main_output(self, file_name: str):
        self.output.config(state=tk_constants.NORMAL)
        self.output.insert(tk_constants.END, file_name + "\n")
        self.output.config(state=tk_constants.DISABLED)
