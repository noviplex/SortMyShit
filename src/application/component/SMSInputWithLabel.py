from tkinter import Tk, StringVar, Frame

from src.application.component.SMSEntry import SMSEntry
from src.application.component.SMSLabel import SMSLabel

class SMSInputWithLabel(Frame):
    def __init__(
        self, 
        container: Tk, 
        text: str, 
        backgroundColor: str,
        fontColor: str,
        settingVar: StringVar
    ):
        super().__init__(
            master=container, 
            padx=10, 
            pady=10, 
            background=backgroundColor,
            width=800,
            height=50
        )

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.grid_propagate(0)

        SMSLabel(container=self, backgroundColor=backgroundColor, fontColor=fontColor, text=text).grid(row=0, column=0, sticky="w")        
        SMSEntry(container=self, backgroundColor=backgroundColor, fontColor=fontColor, stringVar=settingVar, width=50).grid(row=0, column=1, sticky="e")
    