from tkinter import Frame

from src.application.component.SMSLabel import SMSLabel


class SMSEmptyFileCard(Frame):
    def __init__(
        self,
        master,
        text: str,
        bg: str,
        fg: str,
        border_color: str,
    ):
        super().__init__(
            master,
            background=bg,
        )
        self.fg = fg
        self.bg = bg
        self.border_color = border_color

        text_container = Frame(self, width=1200, height=40, background=self.border_color)
        text_container.grid_propagate(0)
        text_container.grid(row=0, column=0, padx=10, pady=10, sticky='w')

        SMSLabel(
            text_container,
            text=text,
            bg=self.border_color,
            fg=self.fg,
            font=("Arial", 12),
        ).grid(row=0, column=0, sticky='w')
