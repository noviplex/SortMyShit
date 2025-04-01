from tkinter import Tk, Frame
from playsound import playsound

class SMSAudioPlayer(Frame):
    def __init__(
            self, 
            container: Tk, 
            audio_path: str, 
            backgroundColor: str,
    ):
        super().__init__(
            master=container,
            bg=backgroundColor,
            padx=5,
            pady=5
        )

        playsound(audio_path)