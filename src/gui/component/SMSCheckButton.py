from tkinter import Checkbutton

from src.configuration.ServiceManager import ServiceManager

from src.service.SettingsService import SettingsService

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
        settingsService = serviceManager.get("SettingsService") # type: SettingsService

        super().__init__(
            container, 
            text=text, 
            variable=variable,
            command=command,
            background=settingsService.getSetting("backgroundColor"), 
            fg=settingsService.getSetting("fontColor"), 
            border=None, 
            borderwidth=0,
            highlightthickness=0,
            padx=padx,
            pady=pady
        )