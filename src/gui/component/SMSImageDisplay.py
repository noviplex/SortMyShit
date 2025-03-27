from tkinter import Tk, Frame, Label
from PIL import Image, ImageTk

from src.entity.Settings import Settings
from src.configuration.ServiceManager import ServiceManager

class SMSImageDisplay(Frame):
    def __init__(self, container: Tk, image_path: str, serviceManager: ServiceManager = ServiceManager()):
        settings = serviceManager.get("Settings") # type: Settings
        
        super().__init__(
            master=container,
            bg=settings.backgroundColor,
            padx=10,
            pady=10
        )

        self.image = Image.open(image_path)
        self.image = ImageTk.PhotoImage(self.image)
        self.imageLabel = Label(self, image=self.image)
        self.imageLabel.pack()
