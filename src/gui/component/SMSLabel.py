from src.entity.Settings import Settings
from tkinter import Tk, Label, StringVar

from src.configuration.ServiceManager import ServiceManager

class SMSLabel(Label):
    def __init__(self, container: Tk, text: str, serviceManager: ServiceManager = ServiceManager()):
        settings = serviceManager.get("Settings") # type: Settings
        self.textVariable = StringVar(container, text)

        super().__init__(
            master=container,
            bg=settings.backgroundColor,
            fg=settings.fontColor,
            textvariable=self.textVariable,
            text=text,
            padx=10,
            pady=10
        )

    def setText(self, text: str):
        self.textVariable.set(text)
        self.update()
