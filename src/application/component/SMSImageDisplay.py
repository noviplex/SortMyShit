from tkinter import Tk, Frame, Label
from PIL import Image, ImageTk


class SMSImageDisplay(Frame):
    def __init__(
            self,
            container: Tk,
            imagePath: str,
            color3: str,
    ):
        super().__init__(
            master=container,
            bg=color3,
            padx=10,
            pady=10,
        )

        self.image = Image.open(imagePath)
        self.image = ImageTk.PhotoImage(self.image)
        self.imageLabel = Label(self, image=self.image)
        self.imageLabel.pack()
