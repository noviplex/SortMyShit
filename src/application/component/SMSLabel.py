from tkinter import Tk, Label, StringVar


class SMSLabel(Label):
    def __init__(
        self,
        container: Tk,
        text: str,
        bg: str,
        fg: str,
        font: str = ("Arial", 14),
        padx: int = 10,
        pady: int = 10
    ):
        self.text_variable = StringVar(container, text)

        super().__init__(
            master=container,
            bg=bg,
            fg=fg,
            textvariable=self.text_variable,
            text=text,
            padx=padx,
            pady=pady,
            font=font,
        )

    def set_text(self, text: str):
        self.text_variable.set(text)
        self.update()
