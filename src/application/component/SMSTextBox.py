from tkinter import Text, constants as tk_constants


class SMSTextBox(Text):
    def __init__(
            self,
            container,
            backgroundColor: str,
            fontColor: str,
            text: str = None,
            width: int = 50,
            height: int = 2,
            disabled: bool = True,
    ):
        super().__init__(
            master=container,
            bg=backgroundColor,
            fg=fontColor,
            width=width,
            height=height,
            border=0,
            borderwidth=0,
            highlightcolor=fontColor,
            padx=5,
            pady=5,
        )

        if disabled is True:
            self.config(state=tk_constants.DISABLED)

        if text is not None:
            self.insert(tk_constants.INSERT, text)
