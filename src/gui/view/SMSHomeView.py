from tkinter import Tk, Scrollbar, constants as tk_constants

from src.gui.component.SMSButton import SMSButton
from src.gui.component.SMSButtonContainer import SMSButtonContainer
from src.gui.component.SMSTextBox import SMSTextBox
from src.gui.component.SMSLabel import SMSLabel
from src.gui.view.SMSView import SMSView

from src.service.FileManager import FileManager
from src.service.FolderManager import FolderManager
from src.configuration.ServiceManager import ServiceManager
from src.event.LogActivityEvent import LogActivityEvent
from src.event.RemoveDuplicatesEvent import RemoveDuplicatesEvent
from src.event.SortFilesEvent import SortFilesEvent
from src.event.RemoveEmptyFoldersEvent import RemoveEmptyFoldersEvent

class SMSHomeView(SMSView):
    def __init__(
        self, 
        container: Tk,
        serviceManager: ServiceManager = ServiceManager()
    ):
        super().__init__(container)

        self.fileManager = serviceManager.get("FileManager") # type: FileManager
        self.folderManager = serviceManager.get("FolderManager") # type: FolderManager
        logActivityEvent = serviceManager.get("LogActivityEvent") # type: LogActivityEvent
        removeDuplicatesEvent = serviceManager.get("RemoveDuplicatesEvent") # type: RemoveDuplicatesEvent
        removeEmptyFoldersEvent = serviceManager.get("RemoveEmptyFoldersEvent") # type: RemoveEmptyFoldersEvent
        removeEmptyFilesEvent = serviceManager.get("RemoveEmptyFilesEvent") # type: RemoveEmptyFoldersEvent
        sortFilesEvent = serviceManager.get("SortFilesEvent") # type: SortFilesEvent

        logActivityEvent.subscribe(self.__logOutput)

        removeDuplicatesEvent.subscribe(self.__showEntryInMainOutput)
        sortFilesEvent.subscribe(self.__showEntryInMainOutput)
        removeEmptyFilesEvent.subscribe(self.__showEntryInMainOutput)
        removeEmptyFoldersEvent.subscribe(self.__showEntryInMainOutput)

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
            SMSButton(buttonFrame, "Remove Empty Files", self.__removeEmptyFiles),
            SMSButton(buttonFrame, "Remove duplicate files", self.__removeDuplicatesInMovedFiles),
            SMSButton(buttonFrame, "Move Files to Sorted Folder", self.__moveFilesToSortedFolder),
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
