from tkinter import Tk

from src.application.component.SMSButton import SMSButton
from src.application.component.SMSButtonContainer import SMSButtonContainer

from src.domain.event.ChangeViewEvent import ChangeViewEvent

from src.infrastructure.repository.SettingsRepository import SettingsRepository

class SMSNavBar(SMSButtonContainer):
    def __init__(self, container: Tk, changeViewEvent: ChangeViewEvent, settingsRepository: SettingsRepository):
        backgroundColor = settingsRepository.loadOne("backgroundColor")
        fontColor = settingsRepository.loadOne("fontColor")
        super().__init__(container, backgroundColor=backgroundColor, direction="horizontal", width=300, height=500, padx=10, pady=10)

        self.setButtons([
            SMSButton(self, backgroundColor=backgroundColor, fontColor=fontColor, text="Home", command=lambda: changeViewEvent.trigger('home'), width=10, height=1),
            SMSButton(self, backgroundColor=backgroundColor, fontColor=fontColor, text="Settings", command=lambda: changeViewEvent.trigger('settings'), width=10, height=1),
        ])