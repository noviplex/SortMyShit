from tkinter import Tk, StringVar, Entry


class SMSEntry(Entry):
    def __init__(
        self,
        container: Tk,
        string_var: StringVar,
        width: int,
        border_color: str,
        bg: str,
        fg: str,
    ):
        super().__init__(
            master=container,
            textvariable=string_var,
            background=bg,
            highlightbackground=border_color,
            fg=fg,
            border=0,
            borderwidth=0,
            width=width,
            font=("Arial", 14),
        )
