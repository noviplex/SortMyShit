from tkinter import Tk, StringVar, Frame

from src.application.component.SMSEntry import SMSEntry
from src.application.component.SMSLabel import SMSLabel


class SMSInputWithLabel(Frame):
    def __init__(
        self,
        container: Tk,
        text: str,
        entryBg: str,
        bg: str,
        fg: str,
        settingVar: StringVar,
    ):
        super().__init__(
            master=container,
            padx=10,
            pady=10,
            background=bg,
            width=800,
            height=50,
        )

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.grid_propagate(0)

        SMSLabel(
            container=self,
            bg=bg,
            fg=fg,
            text=text
        ).grid(row=0, column=0, sticky="w")
        SMSEntry(
            container=self,
            bg=entryBg,
            fg=fg,
            stringVar=settingVar,
            width=50
        ).grid(row=0, column=1, sticky="e")
