from tkinter import Text, constants as tk_constants


class SMSTextBox(Text):
    def __init__(
        self,
        container,
        bg: str,
        fg: str,
        border_color: str,
        text: str = None,
        width: int = 50,
        height: int = 2,
        disabled: bool = True,
    ):
        super().__init__(
            master=container,
            bg=bg,
            fg=fg,
            width=width,
            height=height,
            border=0,
            borderwidth=0,
            highlightcolor=bg,
            highlightbackground=border_color,
            highlightthickness=1,
            padx=5,
            pady=5,
            font=("Courier New", 12),
        )

        if disabled:
            self.config(state=tk_constants.DISABLED)

        if text is not None:
            self.insert(tk_constants.INSERT, text)
