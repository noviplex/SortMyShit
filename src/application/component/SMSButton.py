from tkinter import Tk, Button
from typing import Callable


class SMSButton(Button):
    def __init__(
        self,
        container: Tk,
        text: str,
        command: Callable,
        bg: str,
        fg: str,
        border_color: str,
        width: int = 30,
        height: int = 2,
    ):
        super().__init__(
            master=container,
            text=text,
            background=bg,
            fg=fg,
            activebackground=fg,
            activeforeground=bg,
            highlightbackground=border_color,
            highlightthickness=1,
            command=command,
            width=width,
            height=height,
            border=0,
            borderwidth=0,
            font=("Arial", 14),
        )
