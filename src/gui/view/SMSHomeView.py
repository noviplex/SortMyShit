from tkinter import Tk, constants as tk_constants

from src.gui.component.SMSButton import SMSButton
from src.gui.component.SMSButtonContainer import SMSButtonContainer
from src.gui.component.SMSTextBox import SMSTextBox
from src.gui.component.SMSLabel import SMSLabel
from src.gui.view.SMSView import SMSView

from src.service.SettingsService import SettingsService
from src.service.FileManager import FileManager
from src.service.FolderManager import FolderManager
from src.event.LogActivityEvent import LogActivityEvent
from src.event.RemoveDuplicatesEvent import RemoveDuplicatesEvent
from src.event.SortFilesEvent import SortFilesEvent
from src.event.RemoveEmptyFoldersEvent import RemoveEmptyFoldersEvent
from src.event.RemoveEmptyFilesEvent import RemoveEmptyFilesEvent

class SMSHomeView(SMSView):
    def __init__(
        self, 
        container: Tk,
        settingsService: SettingsService,
        fileManager: FileManager,
        folderManager: FolderManager,
        logActivityEvent: LogActivityEvent,
        removeDuplicatesEvent: RemoveDuplicatesEvent,
        removeEmptyFoldersEvent: RemoveEmptyFoldersEvent,
        removeEmptyFilesEvent: RemoveEmptyFilesEvent,
        sortFilesEvent: SortFilesEvent
    ):
        self.settingsService = settingsService
        self.fileManager = fileManager
        self.folderManager = folderManager
        self.logActivityEvent = logActivityEvent
        self.removeDuplicatesEvent = removeDuplicatesEvent
        self.removeEmptyFoldersEvent = removeEmptyFoldersEvent
        self.removeEmptyFilesEvent = removeEmptyFilesEvent
        self.sortFilesEvent = sortFilesEvent

        self.backgroundColor = self.settingsService.getSetting("backgroundColor")

        super().__init__(container=container, backgroundColor=self.backgroundColor)

        self.createView()

    def createView(self):
        fontColor = self.settingsService.getSetting("fontColor")

        self.logActivityEvent.subscribe(self.__logOutput)
        self.removeDuplicatesEvent.subscribe(self.__showEntryInMainOutput)
        self.sortFilesEvent.subscribe(self.__showEntryInMainOutput)
        self.removeEmptyFilesEvent.subscribe(self.__showEntryInMainOutput)
        self.removeEmptyFoldersEvent.subscribe(self.__showEntryInMainOutput)

        mainText = SMSLabel(container=self, backgroundColor=self.backgroundColor, fontColor=fontColor, text="Select action to perform")
        mainText.grid(column=0, row=0, sticky='w')

        buttonFrame = SMSButtonContainer(
            container=self, 
            direction="vertical",
            backgroundColor=self.backgroundColor,
            width=300, 
            height=500,
            padx=0,
            pady=0,
            buttonSpacingX=10,
            buttonSpacingY=10
        )
        buttonFrame.setButtons([
            SMSButton(buttonFrame, backgroundColor=self.backgroundColor, fontColor=fontColor, text="Remove Empty Folders", command=self.__removeEmptyFolders),
            SMSButton(buttonFrame, backgroundColor=self.backgroundColor, fontColor=fontColor, text="Remove Empty Files", command=self.__removeEmptyFiles),
            SMSButton(buttonFrame, backgroundColor=self.backgroundColor, fontColor=fontColor, text="Remove duplicate files", command=self.__removeDuplicatesInMovedFiles),
            SMSButton(buttonFrame, backgroundColor=self.backgroundColor, fontColor=fontColor, text="Move Files to Sorted Folder", command=self.__moveFilesToSortedFolder),
        ])
        buttonFrame.grid(column=0, row=1, sticky='n')

        self.output = SMSTextBox(container=self, backgroundColor=self.backgroundColor, fontColor=fontColor, height=40, width=140)
        self.output.grid(column=1, row=1)

        self.currentState = SMSLabel(container=self, backgroundColor=self.backgroundColor, fontColor=fontColor, text="Idle")
        self.currentState.grid(column=0, row=2, sticky='w', columnspan=2)

    def __logOutput(self, text: str, maxLength: int=150):
        text = text[:maxLength - 3] + "..." if len(text) > maxLength else text
        self.currentState.setText(text)

    def __showEntryInMainOutput(self, fileName: str):
        self.output.config(state=tk_constants.NORMAL)
        self.output.insert(tk_constants.END, fileName + "\n")
        self.output.config(state=tk_constants.DISABLED)

    def __removeEmptyFolders(self):
        self.__clearOutput()
        self.folderManager.removeEmptyFolder()

    def __removeEmptyFiles(self):
        self.__clearOutput()
        self.fileManager.removeEmptyFiles()

    def __moveFilesToSortedFolder(self):
        self.__clearOutput()
        self.fileManager.moveFilesToSortedFolder()

    def __removeDuplicatesInMovedFiles(self):
        self.__clearOutput()
        self.fileManager.removeDuplicatesInMovedFiles()

    def __clearOutput(self):
        self.output.config(state=tk_constants.NORMAL)
        self.output.delete("1.0", tk_constants.END)
        self.output.config(state=tk_constants.DISABLED)
