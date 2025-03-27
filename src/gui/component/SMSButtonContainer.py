from tkinter import Tk, Frame

from src.entity.Settings import Settings
from src.configuration.ServiceManager import ServiceManager

class SMSButtonContainer(Frame):
    def __init__(
            self,
            container: Tk,
            height: int,
            width: int,
            direction: str="horizontal",
            padx=0,
            pady=0,
            buttonSpacingX=0,
            buttonSpacingY=0,
            ServiceManager: ServiceManager = ServiceManager()
    ):
        settings = ServiceManager.get("Settings") # type: Settings

        super().__init__(
            master=container,
            height=height,
            width=width,
            border=0,
            borderwidth=0,
            bg=settings.backgroundColor,
            padx=padx,
            pady=pady
        )

        self.direction = direction
        self.buttonSpacingX = buttonSpacingX
        self.buttonSpacingY = buttonSpacingY

    def setButtons(self, buttons: list):
        lastButtonIndex = len(buttons) - 1

        for index, button in enumerate(buttons):
            isFirstOrLastButton = (index == 0 or index == lastButtonIndex)

            button.grid(
                row=index if self.direction == "vertical" else 0, 
                column=index if self.direction == "horizontal" else 0,
                padx=0 if isFirstOrLastButton and self.direction == "horizontal" else self.buttonSpacingX,
                pady=0 if isFirstOrLastButton and self.direction == "vertical" else  self.buttonSpacingY
            )
