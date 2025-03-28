from tkinter import Tk, Button

from src.service.SettingsService import SettingsService

from src.configuration.ServiceManager import ServiceManager

class SMSButton(Button):
    def __init__(
            self, 
            container: Tk, 
            text: str, 
            command: callable, 
            width=30, 
            height=2,
            serviceManager: ServiceManager = ServiceManager()
    ):
        settingsService = serviceManager.get("SettingsService") # type: SettingsService

        super().__init__(
            master=container,
            text=text, 
            background=settingsService.getSetting("backgroundColor"),
            fg=settingsService.getSetting("fontColor"), 
            activebackground=settingsService.getSetting("fontColor"),
            activeforeground=settingsService.getSetting("backgroundColor"),
            command=command,
            width=width,
            height=height,
            border=0,
            borderwidth=0,
        )