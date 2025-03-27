from tkinter import Tk, Frame
from playsound import playsound

from src.entity.Settings import Settings
from src.configuration.ServiceManager import ServiceManager

class SMSAudioPlayer(Frame):
    def __init__(self, container: Tk, audio_path: str, serviceManager: ServiceManager = ServiceManager()):
        settings = serviceManager.get("Settings") # type: Settings

        super().__init__(
            master=container,
            bg=settings.backgroundColor,
            padx=5,
            pady=5
        )

        playsound(audio_path)