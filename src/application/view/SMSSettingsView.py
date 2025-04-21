from tkinter import Tk, Frame, BooleanVar, StringVar

from src.application.view.SMSView import SMSView
from src.application.component.SMSLabel import SMSLabel
from src.application.component.SMSCheckButton import SMSCheckButton
from src.application.component.SMSInputWithLabel import SMSInputWithLabel

from src.infrastructure.repository.SettingsRepository import SettingsRepository


class SMSSettingsView(SMSView):
    def __init__(
        self,
        container: Tk,
        settingsRepository: SettingsRepository,
    ):
        self.settingsRepository = settingsRepository

        self.color1 = self.settingsRepository.fetchOne("color1")
        self.color2 = self.settingsRepository.fetchOne("color2")
        self.color3 = self.settingsRepository.fetchOne("color3")
        self.color4 = self.settingsRepository.fetchOne("color4")

        super().__init__(
            container=container,
            bg=self.color1,
            height=500,
        )

        self.createView()

    def createView(self):
        self.__expand()

        SMSLabel(
            container=self,
            bg=self.color1,
            fg=self.color4,
            text="Settings"
        ).grid(row=0, column=0, sticky='w')

        SMSLabel(
            container=self,
            bg=self.color1,
            fg=self.color4,
            text="Sort Files"
        ).grid(row=1, column=0, sticky='w')

        Frame(
            self,
            bg=self.color2,
            height=1,
            bd=0
        ).grid(row=2, column=0, columnspan=2, sticky="ew")

        self.__createInputWithLabel(
            text="Folder to Sort",
            settingName="folderToProcess",
            value=self.settingsRepository.fetchOne("folderToProcess")
        ).grid(row=3, column=0, sticky='w')

        self.__createInputWithLabel(
            text="Destination folder",
            settingName="destinationFolder",
            value=self.settingsRepository.fetchOne("destinationFolder")
        ).grid(row=4, column=0, sticky='w')

        self.__createSettingCheckButton(
            settingName="keepOriginalFiles",
            text="Do not delete files in original folders",
        ).grid(row=5, column=0, sticky='w')

        SMSLabel(
            container=self,
            text="Remove Duplicates",
            bg=self.color1,
            fg=self.color4,
        ).grid(row=6, column=0, sticky='w')

        Frame(
            self,
            bg=self.color2,
            height=1,
            bd=0
        ).grid(row=7, column=0, columnspan=2, sticky="ew")

        self.__createInputWithLabel(
            text="Folder to Process",
            settingName="removeDuplicatesFolder",
            value=self.settingsRepository.fetchOne("removeDuplicatesFolder")
        ).grid(row=8, column=0, sticky='w')

        self.__createSettingCheckButton(
            settingName="binarySearch",
            text="Binary comparison (if disabled, will do a filename comparison instead)",
        ).grid(row=9, column=0, sticky='w')

        self.__createSettingCheckButton(
            settingName="binarySearchLargeFiles",
            text="Enable binary comparison for large files (warning: may crash on large files)",
        ).grid(row=9, column=1, sticky='w')

        SMSLabel(
            container=self,
            bg=self.color1,
            fg=self.color4,
            text="General"
        ).grid(row=10, column=0, sticky='w')

        Frame(
            self,
            bg=self.color2,
            height=1,
            bd=0
        ).grid(row=11, column=0, columnspan=2, sticky="ew")

        self.__createSettingCheckButton(
            settingName="logOutputInFile",
            text="Log output in logfile",
        ).grid(row=12, column=0, sticky='w')

    def __expand(self):
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.grid_propagate(0)

    def __createSettingCheckButton(self, settingName: str, text: str):
        booleanVar = BooleanVar()
        booleanVar.set(self.settingsRepository.fetchOne(settingName))
        return SMSCheckButton(
            container=self,
            text=text,
            variable=booleanVar,
            bg=self.color1,
            fg=self.color4,
            command=lambda: self.settingsRepository.saveOne(settingName, booleanVar.get())
        )

    def __createInputWithLabel(self, text: str, settingName: str, value: str):
        settingVar = StringVar()
        settingVar.set(value=value)
        settingVar.trace_add(
            "write",
            lambda name, index, mode, settingVar=settingVar:
            self.__changeInputWithLabelSetting(
                settingName=settingName,
                settingVar=settingVar
            )
        )

        return SMSInputWithLabel(
            container=self,
            text=text,
            entryBg=self.color3,
            bg=self.color1,
            fg=self.color4,
            settingVar=settingVar,
        )

    def __changeInputWithLabelSetting(
        self,
        settingName: str,
        settingVar: StringVar
    ):
        self.settingsRepository.saveOne(settingName, settingVar.get())
