from tkinter import Tk, Button
from src.entity.Settings import Settings

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
        settings = serviceManager.get("Settings") # type: Settings

        super().__init__(
            master=container,
            text=text, 
            background=settings.backgroundColor,
            fg=settings.fontColor, 
            activebackground=settings.fontColor,
            activeforeground=settings.backgroundColor,
            command=command,
            width=width,
            height=height,
            border=0,
            borderwidth=0,
        )