from tkinter import Tk, Label, StringVar

from src.service.SettingsService import SettingsService

from src.configuration.ServiceManager import ServiceManager

class SMSLabel(Label):
    def __init__(self, container: Tk, text: str, serviceManager: ServiceManager = ServiceManager()):
        settingsService = serviceManager.get("SettingsService") # type: SettingsService

        self.textVariable = StringVar(container, text)

        super().__init__(
            master=container,
            bg=settingsService.getSetting("backgroundColor"),
            fg=settingsService.getSetting("fontColor"),
            textvariable=self.textVariable,
            text=text,
            padx=10,
            pady=10
        )

    def setText(self, text: str):
        self.textVariable.set(text)
        self.update()
