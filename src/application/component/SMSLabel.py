from tkinter import Tk, Label, StringVar


class SMSLabel(Label):
    def __init__(
        self,
        container: Tk,
        text: str,
        backgroundColor: str,
        fontColor: str,
    ):

        self.textVariable = StringVar(container, text)

        super().__init__(
            master=container,
            bg=backgroundColor,
            fg=fontColor,
            textvariable=self.textVariable,
            text=text,
            padx=10,
            pady=10,
        )

    def setText(self, text: str):
        self.textVariable.set(text)
        self.update()
