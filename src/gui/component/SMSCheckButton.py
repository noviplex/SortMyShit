from tkinter import Checkbutton

from src.entity.Settings import Settings
from src.configuration.ServiceManager import ServiceManager

class SMSCheckButton(Checkbutton):
    def __init__(
        self, 
        container, 
        text,
        variable,
        command,
        serviceManager: ServiceManager = ServiceManager(),
        padx=10,
        pady=10
    ):
        settings = serviceManager.get("Settings") # type: Settings

        super().__init__(
            container, 
            text=text, 
            variable=variable,
            command=command,
            background=settings.backgroundColor, 
            fg=settings.fontColor, 
            border=None, 
            borderwidth=0,
            highlightthickness=0,
            padx=padx,
            pady=pady
        )