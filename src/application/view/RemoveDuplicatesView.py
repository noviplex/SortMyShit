from tkinter import Tk

from src.application.component.SMSComparisonCard import SMSComparisonCard
from src.application.component.SMSButton import SMSButton
from src.application.component.SMSButtonContainer import SMSButtonContainer
from src.application.component.SMSLabel import SMSLabel
from src.application.component.SMSScrollableFrame import SMSScrollableFrame
from src.application.view.SMSView import SMSView
from src.domain.entity.DuplicateMatch import DuplicateMatch
from src.domain.service.list.ListDuplicate import ListDuplicate
from src.domain.service.remove.RemoveDuplicate import RemoveDuplicate
from src.infrastructure.repository.SettingsRepository import SettingsRepository
from src.infrastructure.repository.TmpStorageRepository import TmpStorageRepository
from src.application.service.EventManager import EventManager


class RemoveDuplicatesView(SMSView):
    def __init__(
        self,
        container: Tk,
        settings_repository: SettingsRepository,
        list_duplicates: ListDuplicate,
        duplicate_remover: RemoveDuplicate,
        tmp_storage_repository: TmpStorageRepository,
        event_manager: EventManager,
    ):
        self.settings_repository = settings_repository
        self.list_duplicates = list_duplicates
        self.duplicate_remover = duplicate_remover
        self.tmp_storage_repository = tmp_storage_repository
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
            text="Remove Duplicates",
            font=("Arial", 24)
        ).grid(row=0, column=0, sticky='w')

        self.duplicates_list_display = SMSScrollableFrame(self, self.color1)
        self.duplicates_list_display.grid(row=1, column=1, sticky='nse')

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
                    text="Launch Analysis",
                    command=self.__list_duplicates,
                ),
                self.__create_button(
                    container=action_buttons,
                    text="Run Duplicate Removal",
                    command=self.__remove_duplicates,
                )
            ]
        )
        action_buttons.grid(row=1, column=0, sticky='nw', pady=5)

    def __list_duplicates(self):
        duplicate_matches = self.list_duplicates.list_duplicates()

        row = 0
        for duplicate_match in duplicate_matches:
            card = self.__create_duplicate_card(duplicate_match, self.duplicates_list_display.get_interior())
            card.grid(row=row, column=0, sticky='w')
            row += 1

        self.tmp_storage_repository.save_one("duplicate_matches", duplicate_matches)

    def __remove_duplicates(self):
        duplicate_matches = self.tmp_storage_repository.fetch_one("duplicate_matches")
        self.duplicate_remover.remove_duplicates(duplicate_matches)
        self.duplicates_list_display.reload()
        self.tmp_storage_repository.remove_one("duplicate_matches")

    def __create_button(self, container, text, command):
        return SMSButton(
            container=container,
            text=text,
            bg=self.color2,
            fg=self.color4,
            border_color=self.color2,
            command=command
        )

    def __create_duplicate_card(self, duplicate_match: DuplicateMatch, container):
        return SMSComparisonCard(
            container,
            duplicate_match,
            bg=self.color1,
            fg=self.color4,
            border_color=self.color2,
        )

    def __change_current_state(self, text: str, max_length: int = 150):
        text = text[:max_length - 3] + "..." if len(text) > max_length else text
        self.current_state.set_text(text)
