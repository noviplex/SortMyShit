from tkinter import Tk

from src.gui.component.SMSButton import SMSButton
from src.gui.component.SMSButtonContainer import SMSButtonContainer

from src.event.ChangeViewEvent import ChangeViewEvent

from src.configuration.ServiceManager import ServiceManager

class SMSNavBar(SMSButtonContainer):
    def __init__(self, container: Tk, serviceManager: ServiceManager = ServiceManager()):
        super().__init__(container, direction="horizontal", width=300, height=500, padx=10, pady=10)

        changeViewEvent = serviceManager.get("ChangeViewEvent") # type: ChangeViewEvent

        self.setButtons([
            SMSButton(self, "Home", lambda: changeViewEvent.trigger('home'), width=10, height=1),
            SMSButton(self, "Settings", lambda: changeViewEvent.trigger('settings'), width=10, height=1),
        ])