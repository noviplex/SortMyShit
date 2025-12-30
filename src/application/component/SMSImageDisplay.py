from tkinter import Tk, Label
from PIL import Image, ImageFile, ImageTk


class SMSImageDisplay(Label):
    def __init__(
        self,
        container: Tk,
        full_path: str,
        target_width: int = 600,
        target_height: int = 600,
        bg: str = "#FFFFFF",
    ):
        image = ImageTk.PhotoImage(self.__resize_image(Image.open(full_path), target_width, target_height))

        super().__init__(container, image=image, width=target_width, height=target_height, background=bg)
        self.image = image

    def __resize_image(self, image: ImageFile, target_width: int, target_height: int) -> ImageFile:
        image_width = image.size[0]
        image_height = image.size[1]

        height_ratio = image_width / target_width
        width_ratio = image_height / target_height

        if image_height / height_ratio > target_height:
            image_height = target_height
            image_width = int(image_width / width_ratio)
        else:
            image_height = int(image_height / height_ratio)
            image_width = target_width

        return image.resize((image_width, image_height))
