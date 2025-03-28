from tkinter import Tk, StringVar, Frame

from src.gui.component.SMSEntry import SMSEntry
from src.gui.component.SMSLabel import SMSLabel

from src.service.SettingsService import SettingsService

from src.configuration.ServiceManager import ServiceManager

class SMSInputWithLabel(Frame):
    def __init__(
        self, 
        container: Tk, 
        text: str, 
        settingName: str,
        serviceManager: ServiceManager = ServiceManager(),
    ):
        self.settingsService = serviceManager.get("SettingsService") # type: SettingsService
        self.settingName = settingName

        super().__init__(
            master=container, 
            padx=10, 
            pady=10, 
            background=self.settingsService.getSetting("backgroundColor"),
            width=800,
            height=50
        )

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.grid_propagate(0)
        
        SMSLabel(container=self, text=text).grid(row=0, column=0, sticky="w")        
        settingVar = StringVar()
        settingVar.set(self.settingsService.getSetting(self.settingName))
        settingVar.trace_add("write", lambda name, index, mode, sv=settingVar: self.__changeSetting(sv))
        SMSEntry(container=self, stringVar=settingVar, width=50).grid(row=0, column=1, sticky="e")
    
    def __changeSetting(self, settingVar: StringVar):
        self.settingsService.setSetting(self.settingName, settingVar.get())