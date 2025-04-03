from tkinter import Tk, Button


class SMSButton(Button):
    def __init__(
            self,
            container: Tk,
            text: str,
            command: callable,
            backgroundColor: str,
            fontColor: str,
            width=30,
            height=2,
    ):
        super().__init__(
            master=container,
            text=text,
            background=backgroundColor,
            fg=fontColor,
            activebackground=fontColor,
            activeforeground=backgroundColor,
            command=command,
            width=width,
            height=height,
            border=0,
            borderwidth=0,
        )
