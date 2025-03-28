from tkinter import Tk, Frame, Label
from PIL import Image, ImageTk

from src.service.SettingsService import SettingsService

from src.configuration.ServiceManager import ServiceManager

class SMSImageDisplay(Frame):
    def __init__(self, container: Tk, image_path: str, serviceManager: ServiceManager = ServiceManager()):
        settingsService = serviceManager.get("SettingsService") # type: SettingsService
        
        super().__init__(
            master=container,
            bg=settingsService.getSetting("backgroundColor"),
            padx=10,
            pady=10
        )

        self.image = Image.open(image_path)
        self.image = ImageTk.PhotoImage(self.image)
        self.imageLabel = Label(self, image=self.image)
        self.imageLabel.pack()