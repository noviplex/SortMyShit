from tkinter import Tk, Frame
from playsound import playsound


class SMSAudioButton(Frame):
    def __init__(
        self,
        container: Tk,
        audio_path: str,
        color3: str,
    ):
        super().__init__(
            master=container,
            bg=color3,
            padx=5,
            pady=5,
        )

        playsound(audio_path)
