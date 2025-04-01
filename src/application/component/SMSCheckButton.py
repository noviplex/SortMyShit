from tkinter import Checkbutton

class SMSCheckButton(Checkbutton):
    def __init__(
        self, 
        container, 
        text,
        variable,
        command,
        backgroundColor: str,
        fontColor: str,
        padx=10,
        pady=10,
    ):

        super().__init__(
            container, 
            text=text, 
            variable=variable,
            command=command,
            background=backgroundColor, 
            fg=fontColor, 
            border=None, 
            borderwidth=0,
            highlightthickness=0,
            padx=padx,
            pady=pady
        )