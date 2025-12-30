from tkinter import Tk

from src.application.component.SMSButton import SMSButton
from src.application.component.SMSButtonContainer import SMSButtonContainer
from src.application.component.SMSLabel import SMSLabel
from src.application.view.SMSView import SMSView
from src.infrastructure.repository.SettingsRepository import SettingsRepository
from src.application.service.EventManager import EventManager
from src.domain.service.sort.SortFile import SortFile


class SortFilesView(SMSView):
    def __init__(
        self,
        container: Tk,
        settings_repository: SettingsRepository,
        sort_files: SortFile,
        event_manager: EventManager,
    ):
        self.settings_repository = settings_repository
        self.sort_files = sort_files
        self.event_manager = event_manager

        self.color1 = self.settings_repository.fetch_one("color1")
        self.color2 = self.settings_repository.fetch_one("color2")
        self.color3 = self.settings_repository.fetch_one("color3")
        self.color4 = self.settings_repository.fetch_one("color4")

        super().__init__(
            container=container,
            bg=self.settings_repository.fetch_one("color1")
        )

        self.create_view()

    def create_view(self):
        self.event_manager.subscribe("status", self.__change_current_state)

        self.current_state = SMSLabel(
            container=self,
            fg=self.color4,
            bg=self.color1,
            text="Idle",
        )
        self.current_state.grid(column=0, row=2, sticky='w', columnspan=2)

        SMSLabel(
            container=self,
            bg=self.color1,
            fg=self.color4,
            text="Sort Files By Type",
            font=("Arial", 24)
        ).grid(row=0, column=0, sticky='w')

        action_buttons = SMSButtonContainer(
            container=self,
            bg=self.color1,
            direction="vertical",
            padx=15,
            height=200,
            width=400,
            button_spacing_y=10,
        )
        action_buttons.set_buttons(
            [
                self.__create_button(
                    container=action_buttons,
                    text="Sort Files",
                    command=self.__sort_files,
                )
            ]
        )
        action_buttons.grid(row=1, column=0, sticky='nw', pady=5)

    def __sort_files(self):
        self.sort_files.move_files_to_sorted_folder()

    def __create_button(self, container, text, command):
        return SMSButton(
            container=container,
            text=text,
            bg=self.color2,
            fg=self.color4,
            border_color=self.color2,
            command=command
        )

    def __change_current_state(self, text: str, max_length: int = 150):
        text = text[:max_length - 3] + "..." if len(text) > max_length else text
        self.current_state.set_text(text)
