from tkinter import Tk

from src.gui.component.SMSButton import SMSButton
from src.gui.component.SMSButtonContainer import SMSButtonContainer

from src.event.ChangeViewEvent import ChangeViewEvent

from src.service.SettingsService import SettingsService

class SMSNavBar(SMSButtonContainer):
    def __init__(self, container: Tk, changeViewEvent: ChangeViewEvent, settingsService: SettingsService):
        backgroundColor = settingsService.getSetting("backgroundColor")
        fontColor = settingsService.getSetting("fontColor")
        super().__init__(container, backgroundColor=backgroundColor, direction="horizontal", width=300, height=500, padx=10, pady=10)

        self.setButtons([
            SMSButton(self, backgroundColor=backgroundColor, fontColor=fontColor, text="Home", command=lambda: changeViewEvent.trigger('home'), width=10, height=1),
            SMSButton(self, backgroundColor=backgroundColor, fontColor=fontColor, text="Settings", command=lambda: changeViewEvent.trigger('settings'), width=10, height=1),
        ])