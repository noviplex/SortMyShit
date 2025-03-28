from tkinter import Tk, StringVar, Entry

from src.service.SettingsService import SettingsService

from src.configuration.ServiceManager import ServiceManager

class SMSEntry(Entry):
    def __init__(
        self, 
        container: Tk, 
        stringVar: StringVar,
        width: int,
        serviceManager: ServiceManager = ServiceManager()
    ):
        settingsService = serviceManager.get("SettingsService") # type: SettingsService

        super().__init__(
            master=container, 
            textvariable=stringVar,
            background=settingsService.getSetting("backgroundColor"),
            highlightcolor=settingsService.getSetting("fontColor"),
            fg=settingsService.getSetting("fontColor"),
            border=0,
            borderwidth=0,
            width=width,
            font="Arial 14"
        )