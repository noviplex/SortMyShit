from tkinter import Tk, Button


class SMSButton(Button):
    def __init__(
            self,
            container: Tk,
            text: str,
            command: callable,
            color3: str,
            color4: str,
            width=30,
            height=2,
    ):
        super().__init__(
            master=container,
            text=text,
            background=color3,
            fg=color4,
            activebackground=color4,
            activeforeground=color3,
            command=command,
            width=width,
            height=height,
            border=0,
            borderwidth=0,
        )
