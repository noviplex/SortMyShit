from tkinter import Tk, StringVar, Frame, filedialog

from src.application.component.SMSEntry import SMSEntry
from src.application.component.SMSLabel import SMSLabel
from src.application.component.SMSButton import SMSButton


class SMSInputWithLabel(Frame):
    def __init__(
        self,
        container: Tk,
        text: str,
        entry_bg: str,
        bg: str,
        fg: str,
        setting_var: StringVar,
    ):
        super().__init__(
            master=container,
            padx=10,
            pady=10,
            background=bg,
            width=800,
            height=50,
        )

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.grid_propagate(0)

        SMSLabel(
            container=self,
            bg=bg,
            fg=fg,
            text=text
        ).grid(row=0, column=0, sticky="w")

        SMSButton(
            container=self,
            text="...",
            width=5,
            height=1,
            bg=bg,
            fg=fg,
            border_color=entry_bg,
            command=lambda setting_var=setting_var: setting_var.set(
                filedialog.askdirectory(
                    initialdir="~/",
                    title="Select a Directory",
                )
            )
        ).grid(row=0, column=1)

        SMSEntry(
            container=self,
            bg=entry_bg,
            fg=fg,
            border_color=fg,
            string_var=setting_var,
            width=50
        ).grid(row=0, column=2, sticky="e")
