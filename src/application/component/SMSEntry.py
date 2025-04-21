from tkinter import Tk, StringVar, Entry


class SMSEntry(Entry):
    def __init__(
        self,
        container: Tk,
        stringVar: StringVar,
        width: int,
        bg: str,
        fg: str,
    ):

        super().__init__(
            master=container,
            textvariable=stringVar,
            background=bg,
            highlightcolor=bg,
            fg=fg,
            border=0,
            borderwidth=0,
            width=width,
            font="Arial 14",
        )
