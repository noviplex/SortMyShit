from abc import ABC, abstractmethod
from tkinter import Tk, Frame

class SMSView(ABC, Frame):
    def __init__(
            self,
            container: Tk, 
            backgroundColor: str,
            width: int=1600,
            height: int=800,
    ):
        super().__init__(container, width=width, height=height, padx=10, pady=10)
        self.configure(bg=backgroundColor)

    @abstractmethod
    def createView():
        pass