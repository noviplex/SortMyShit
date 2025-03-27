from tkinter import Tk, Frame

from src.entity.Settings import Settings
from src.configuration.ServiceManager import ServiceManager

class SMSView(Frame):
    def __init__(
            self, 
            container: Tk, 
            serviceManager: ServiceManager = ServiceManager(),
            width=1600,
            height=800
    ):
        settings = serviceManager.get("Settings") # type: Settings

        super().__init__(container, width=width, height=height, padx=10, pady=10)
        self.configure(bg=settings.backgroundColor)
