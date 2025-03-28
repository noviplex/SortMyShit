from tkinter import Tk, Scrollbar, constants as tk_constants

from src.gui.component.SMSButton import SMSButton
from src.gui.component.SMSButtonContainer import SMSButtonContainer
from src.gui.component.SMSTextBox import SMSTextBox
from src.gui.component.SMSLabel import SMSLabel
from src.gui.view.SMSView import SMSView

from src.service.FileManagement import FileManagement
from src.service.FolderManagement import FolderManagement
from src.configuration.ServiceManager import ServiceManager
from src.event.LogActivityEvent import LogActivityEvent
from src.event.DuplicateFoundEvent import DuplicateFoundEvent
from src.event.FileMovedEvent import FileMovedEvent
from src.event.FolderDeletedEvent import FolderDeletedEvent

class SMSHomeView(SMSView):
    def __init__(
        self, 
        container: Tk,
        serviceManager: ServiceManager = ServiceManager()
    ):
        super().__init__(container)

        self.fileManagement = serviceManager.get("FileManagement") # type: FileManagement
        self.folderManagement = serviceManager.get("FolderManagement") # type: FolderManagement
        logActivityEvent = serviceManager.get("LogActivityEvent") # type: LogActivityEvent
        duplicateFoundEvent = serviceManager.get("DuplicateFoundEvent") # type: DuplicateFoundEvent
        fileMovedEvent = serviceManager.get("FileMovedEvent") # type: FileMovedEvent
        folderDeletedEvent = serviceManager.get("FolderDeletedEvent") # type: FolderDeletedEvent

        logActivityEvent.subscribe(self.__logOutput)
        duplicateFoundEvent.subscribe(self.__showEntryInMainOutput)
        fileMovedEvent.subscribe(self.__showEntryInMainOutput)
        folderDeletedEvent.subscribe(self.__showEntryInMainOutput)

        mainText = SMSLabel(container=self, text="Select action to perform")
        mainText.grid(column=0, row=0, sticky='w')

        buttonFrame = SMSButtonContainer(
            container=self, 
            direction="vertical", 
            width=300, 
            height=500,
            padx=0,
            pady=0,
            buttonSpacingX=10,
            buttonSpacingY=10
        )
        buttonFrame.setButtons([
            SMSButton(buttonFrame, "Remove Empty Folders", self.__removeEmptyFolders),
            SMSButton(buttonFrame, "Move Files to Sorted Folder", self.__moveFilesToSortedFolder),
            SMSButton(buttonFrame, "Remove duplicate files", self.__removeDuplicatesInMovedFiles),
        ])
        buttonFrame.grid(column=0, row=1, sticky='n')

        self.output = SMSTextBox(container=self, height=40, width=140)
        self.output.grid(column=1, row=1)

        self.currentState = SMSLabel(container=self, text="Idle")
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
        self.folderManagement.removeEmptyFolder()

    def __moveFilesToSortedFolder(self):
        self.__clearOutput()
        self.fileManagement.moveFilesToSortedFolder()

    def __removeDuplicatesInMovedFiles(self):
        self.__clearOutput()
        self.fileManagement.removeDuplicatesInMovedFiles()

    def __clearOutput(self):
        self.output.config(state=tk_constants.NORMAL)
        self.output.delete("1.0", tk_constants.END)
        self.output.config(state=tk_constants.DISABLED)
