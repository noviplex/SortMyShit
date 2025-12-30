from tkinter import Checkbutton


class SMSCheckButton(Checkbutton):
    def __init__(
        self,
        container,
        text,
        variable,
        command,
        bg: str,
        fg: str,
        padx=10,
        pady=10,
    ):
        super().__init__(
            container,
            text=text,
            variable=variable,
            command=command,
            background=bg,
            fg=fg,
            border=None,
            borderwidth=0,
            highlightthickness=0,
            padx=padx,
            pady=pady,
            font=("Arial", 14),
        )
