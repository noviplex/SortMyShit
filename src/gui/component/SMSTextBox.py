from tkinter import Text, constants as tk_constants

from src.entity.Settings import Settings
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
        settings = serviceManager.get("Settings") # type: Settings

        super().__init__(
            master=container, 
            bg=settings.backgroundColor,
            fg=settings.fontColor,
            width=width,
            height=height,
            border=0,
            borderwidth=0,
            highlightcolor=settings.fontColor,
            padx=5,
            pady=5
        )

        if disabled == True:
            self.config(state=tk_constants.DISABLED)

        if text != None:
            self.insert(tk_constants.INSERT, text)