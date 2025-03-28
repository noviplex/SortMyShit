from tkinter import Tk, Frame

from src.service.SettingsService import SettingsService

from src.configuration.ServiceManager import ServiceManager

class SMSView(Frame):
    def __init__(
            self, 
            container: Tk, 
            serviceManager: ServiceManager = ServiceManager(),
            width=1600,
            height=800
    ):
        settingsService = serviceManager.get("SettingsService") # type: SettingsService

        super().__init__(container, width=width, height=height, padx=10, pady=10)
        self.configure(bg=settingsService.getSetting("backgroundColor"))
