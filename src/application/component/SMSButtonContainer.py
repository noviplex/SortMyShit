from tkinter import Tk, Frame


class SMSButtonContainer(Frame):
    def __init__(
        self,
        container: Tk,
        height: int,
        width: int,
        bg: str,
        direction: str = "horizontal",
        padx: int = 0,
        pady: int = 0,
        button_spacing_x: int = 0,
        button_spacing_y: int = 0,
    ):
        super().__init__(
            master=container,
            height=height,
            width=width,
            border=0,
            borderwidth=0,
            bg=bg,
            padx=padx,
            pady=pady,
        )

        self.direction = direction
        self.button_spacing_x = button_spacing_x
        self.button_spacing_y = button_spacing_y

    def set_buttons(self, buttons: list):
        for index, button in enumerate(buttons):
            button.grid(
                row=index if self.direction == "vertical" else 0,
                column=index if self.direction == "horizontal" else 0,
                padx=(0, self.button_spacing_x) if self.direction == "horizontal" else self.button_spacing_x,
                pady=(0, self.button_spacing_y) if self.direction == "vertical" else self.button_spacing_y,
            )
