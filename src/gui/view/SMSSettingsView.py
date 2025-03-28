from tkinter import Tk, Frame, BooleanVar

from src.gui.view.SMSView import SMSView
from src.gui.component.SMSLabel import SMSLabel
from src.gui.component.SMSCheckButton import SMSCheckButton
from src.gui.component.SMSInputWithLabel import SMSInputWithLabel

from src.configuration.ServiceManager import ServiceManager

from src.service.SettingsService import SettingsService

class SMSSettingsView(SMSView):
    def __init__(
        self, 
        container: Tk,
        serviceManager: ServiceManager = ServiceManager()
    ):
        super().__init__(container, height=500)
        self.__expand()

        self.settingsService = serviceManager.get("SettingsService") # type: SettingsService

        SMSLabel(container=self, text="Settings").grid(row=0, column=0, sticky='w')

        SMSLabel(container=self, text="Sort Files").grid(row=1, column=0, sticky='w')

        Frame(self, bg=self.settingsService.getSetting("fontColor"), height=1, bd=0).grid(row=2, column=0, columnspan=2, sticky="ew")

        SMSInputWithLabel(
            self, 
            text="Folder to sort", 
            settingName="folderToProcess"
        ).grid(row=3, column=0, sticky='w')

        SMSInputWithLabel(
            self, 
            text="Destination folder", 
            settingName="destinationFolder"
        ).grid(row=4, column=0, sticky='w')

        self.__createSettingCheckButton(
            settingName="keepOriginalFiles",
            text="Do not delete files in original folders"
        ).grid(row=5, column=0, sticky='w')

        SMSLabel(container=self, text="Remove Duplicates").grid(row=6, column=0, sticky='w')

        Frame(self, bg=self.settingsService.getSetting("fontColor"), height=1, bd=0).grid(row=7, column=0, columnspan=2, sticky="ew")

        SMSInputWithLabel(
            self, 
            text="Folder to Process", 
            settingName="removeDuplicatesFolder"
        ).grid(row=8, column=0, sticky='w')

        self.__createSettingCheckButton(
            settingName="binarySearch",
            text="Binary comparison (if disabled, will do a filename comparison instead)"
        ).grid(row=9, column=0, sticky='w')

        self.__createSettingCheckButton(
            settingName="binarySearchLargeFiles",
            text="Enable binary comparison for large files (warning: may crash on large files)"
        ).grid(row=9, column=1, sticky='w')

        SMSLabel(container=self, text="General").grid(row=10, column=0, sticky='w')

        Frame(self, bg=self.settingsService.getSetting("fontColor"), height=1, bd=0).grid(row=11, column=0, columnspan=2, sticky="ew")

        self.__createSettingCheckButton(
            settingName="logOutputInFile",
            text="Log output in logfile"
        ).grid(row=12, column=0, sticky='w')

    def __expand(self):
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.grid_propagate(0)

    def __createSettingCheckButton(self, settingName: str, text: str):
        booleanVar = BooleanVar()
        booleanVar.set(self.settingsService.getSetting(settingName))
        return SMSCheckButton(
            container=self, 
            text=text, 
            variable=booleanVar,
            command=lambda: self.settingsService.setSetting(settingName, booleanVar.get())
        )