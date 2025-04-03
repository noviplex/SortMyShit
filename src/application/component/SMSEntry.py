from tkinter import Tk, StringVar, Entry


class SMSEntry(Entry):
    def __init__(
        self,
        container: Tk,
        stringVar: StringVar,
        width: int,
        backgroundColor: str,
        fontColor: str,
    ):

        super().__init__(
            master=container,
            textvariable=stringVar,
            background=backgroundColor,
            highlightcolor=fontColor,
            fg=fontColor,
            border=0,
            borderwidth=0,
            width=width,
            font="Arial 14",
        )
