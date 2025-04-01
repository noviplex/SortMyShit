from tkinter import Tk, StringVar, Frame

from src.gui.component.SMSEntry import SMSEntry
from src.gui.component.SMSLabel import SMSLabel

from src.service.SettingsService import SettingsService

class SMSInputWithLabel(Frame):
    def __init__(
        self, 
        container: Tk, 
        text: str, 
        settingName: str,
        settingsService: SettingsService
    ):
        self.settingsService = settingsService
        self.settingName = settingName

        backgroundColor = self.settingsService.getSetting("backgroundColor")
        fontColor = self.settingsService.getSetting("fontColor")

        super().__init__(
            master=container, 
            padx=10, 
            pady=10, 
            background=backgroundColor,
            width=800,
            height=50
        )

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.grid_propagate(0)
        
        SMSLabel(container=self, backgroundColor=backgroundColor, fontColor=fontColor, text=text).grid(row=0, column=0, sticky="w")        
        settingVar = StringVar()
        settingVar.set(self.settingsService.getSetting(self.settingName))
        settingVar.trace_add("write", lambda name, index, mode, sv=settingVar: self.__changeSetting(sv))
        SMSEntry(container=self, backgroundColor=backgroundColor, fontColor=fontColor, stringVar=settingVar, width=50).grid(row=0, column=1, sticky="e")
    
    def __changeSetting(self, settingVar: StringVar):
        self.settingsService.setSetting(self.settingName, settingVar.get())