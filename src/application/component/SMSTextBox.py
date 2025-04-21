from tkinter import Text, constants as tk_constants


class SMSTextBox(Text):
    def __init__(
            self,
            container,
            color3: str,
            color4: str,
            text: str = None,
            width: int = 50,
            height: int = 2,
            disabled: bool = True,
    ):
        super().__init__(
            master=container,
            bg=color3,
            fg=color4,
            width=width,
            height=height,
            border=0,
            borderwidth=0,
            highlightcolor=color4,
            padx=5,
            pady=5,
        )

        if disabled is True:
            self.config(state=tk_constants.DISABLED)

        if text is not None:
            self.insert(tk_constants.INSERT, text)
