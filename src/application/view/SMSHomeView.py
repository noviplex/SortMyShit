from tkinter import Tk, constants as tk_constants

from src.application.component.SMSButton import SMSButton
from src.application.component.SMSButtonContainer import SMSButtonContainer
from src.application.component.SMSTextBox import SMSTextBox
from src.application.component.SMSLabel import SMSLabel
from src.application.service.EventManager import EventManager
from src.application.view.SMSView import SMSView

from src.domain.service.FileSorter import FileSorter
from src.domain.service.FileManager import FileManager
from src.domain.service.EmptyFolderRemover import EmptyFolderRemover
from src.domain.service.EmptyFileRemover import EmptyFileRemover

from src.infrastructure.repository.SettingsRepository import SettingsRepository


class SMSHomeView(SMSView):
    def __init__(
        self,
        container: Tk,
        settingsRepository: SettingsRepository,
        fileManager: FileManager,
        emptyFolderRemover: EmptyFolderRemover,
        emptyFileRemover: EmptyFileRemover,
        fileSorter: FileSorter,
        eventManager: EventManager
    ):
        self.settingsRepository = settingsRepository
        self.fileManager = fileManager
        self.emptyFileRemover = emptyFileRemover
        self.emptyFolderRemover = emptyFolderRemover
        self.fileSorter = fileSorter
        self.eventManager = eventManager

        self.color1 = self.settingsRepository.fetchOne("color1")
        self.color3 = self.settingsRepository.fetchOne("color3")

        super().__init__(
            container=container,
            bg=self.color1
        )

        self.createView()

    def createView(self):
        color4 = self.settingsRepository.fetchOne("color4")

        self.eventManager.subscribe("status", self.__changeCurrentState)
        self.eventManager.subscribe("output", self.__showEntryInMainOutput)

        SMSLabel(
            container=self,
            bg=self.color1,
            fg=color4,
            text="Select action to perform",
        ).grid(column=0, row=0, sticky='w')

        buttonFrame = SMSButtonContainer(
            container=self,
            direction="vertical",
            bg=self.color1,
            width=300,
            height=500,
            padx=0,
            pady=0,
            buttonSpacingX=10,
            buttonSpacingY=10,
        )
        buttonFrame.setButtons([
            SMSButton(
                buttonFrame,
                color3=self.color3,
                color4=color4,
                text="Remove Empty Folders",
                command=self.__removeEmptyFolders,
            ),
            SMSButton(
                buttonFrame,
                color3=self.color3,
                color4=color4,
                text="Remove Empty Files",
                command=self.__removeEmptyFiles,
            ),
            SMSButton(
                buttonFrame,
                color3=self.color3,
                color4=color4,
                text="Remove duplicate files",
                command=self.__removeDuplicatesInMovedFiles
            ),
            SMSButton(
                buttonFrame,
                color3=self.color3,
                color4=color4,
                text="Move Files to Sorted Folder",
                command=self.__moveFilesToSortedFolder
            ),
        ])
        buttonFrame.grid(column=0, row=1, sticky='n')

        self.output = SMSTextBox(
            container=self,
            color3=self.color3,
            color4=color4,
            height=40,
            width=140,
        )
        self.output.grid(column=1, row=1)

        self.currentState = SMSLabel(
            container=self,
            fg=color4,
            bg=self.color1,
            text="Idle",
        )
        self.currentState.grid(column=0, row=2, sticky='w', columnspan=2)

    def __changeCurrentState(self, text: str, maxLength: int = 150):
        text = text[:maxLength - 3] + "..." if len(text) > maxLength else text
        self.currentState.setText(text)

    def __showEntryInMainOutput(self, fileName: str):
        self.output.config(state=tk_constants.NORMAL)
        self.output.insert(tk_constants.END, fileName + "\n")
        self.output.config(state=tk_constants.DISABLED)

    def __removeEmptyFolders(self):
        self.__clearOutput()
        self.emptyFolderRemover.removeEmptyFolders()

    def __removeEmptyFiles(self):
        self.__clearOutput()
        self.emptyFileRemover.removeEmptyFiles()

    def __moveFilesToSortedFolder(self):
        self.__clearOutput()
        self.fileSorter.moveFilesToSortedFolder()

    def __removeDuplicatesInMovedFiles(self):
        self.__clearOutput()
        self.fileManager.removeDuplicatesInMovedFiles()

    def __clearOutput(self):
        self.output.config(state=tk_constants.NORMAL)
        self.output.delete("1.0", tk_constants.END)
        self.output.config(state=tk_constants.DISABLED)
