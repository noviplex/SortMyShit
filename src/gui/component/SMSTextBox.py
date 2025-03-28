from tkinter import Text, constants as tk_constants

from src.service.SettingsService import SettingsService

from src.configuration.ServiceManager import ServiceManager

class SMSTextBox(Text):
    def __init__(
            self, 
            container, 
            text: str=None, 
            width: int=50, 
            height: int=2, 
            disabled: bool=True,
            serviceManager: ServiceManager = ServiceManager()
    ):
        settingsService = serviceManager.get("SettingsService") # type: SettingsService

        super().__init__(
            master=container, 
            bg=settingsService.getSetting("backgroundColor"),
            fg=settingsService.getSetting("fontColor"),
            width=width,
            height=height,
            border=0,
            borderwidth=0,
            highlightcolor=settingsService.getSetting("fontColor"),
            padx=5,
            pady=5,
        )

        if disabled == True:
            self.config(state=tk_constants.DISABLED)

        if text != None:
            self.insert(tk_constants.INSERT, text)