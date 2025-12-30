from tkinter import Tk, Menu, Frame, font as tkFont

from src.application.view.SMSView import SMSView
from src.infrastructure.repository.SettingsRepository import SettingsRepository
from src.manager.ViewManager import ViewManager


class SMSRenderer:
    def __init__(
        self,
        settingsRepository: SettingsRepository,
    ):
        self.settingsRepository = settingsRepository

    def render(self, root: Tk, viewManager: ViewManager):
        self.viewManager = viewManager
        self.color1 = self.settingsRepository.fetch_one("color1")
        self.color2 = self.settingsRepository.fetch_one("color2")
        self.color3 = self.settingsRepository.fetch_one("color3")
        self.color4 = self.settingsRepository.fetch_one("color4")

        default_font = tkFont.nametofont("TkDefaultFont")
        default_font.configure(size=15)

        root.title("SortMyShit")
        root.geometry('1600x900')
        root.resizable(width=False, height=False)
        root.configure(bg=self.color1)

        menu = Menu(root)
        root.config(menu=menu)

        root.bind('<KeyPress-d>', lambda event: self.change_view("remove_duplicates"))
        root.bind('<KeyPress-f>', lambda event: self.change_view("remove_empty_folders"))
        root.bind('<KeyPress-i>', lambda event: self.change_view("remove_empty_files"))
        root.bind('<KeyPress-s>', lambda event: self.change_view("sort_files"))
        root.bind('<KeyPress-c>', lambda event: self.change_view("console"))

        actions_menu = Menu(menu, tearoff=0)
        actions_menu.add_command(label="Remove duplicate files (D)", command=lambda: self.change_view("remove_duplicates"))
        actions_menu.add_command(label="Remove Empty Folders (F)", command=lambda: self.change_view("remove_empty_folders"))
        actions_menu.add_command(label="Remove Empty Files (I)", command=lambda: self.change_view("remove_empty_files"))
        actions_menu.add_command(label="Sort Files by Folder (S)", command=lambda: self.change_view("sort_files"))
        actions_menu.add_command(label="Show Console (C)", command=lambda: self.change_view("console"))

        file_menu = Menu(menu, tearoff=0)
        file_menu.add_command(label="Settings", command=lambda: self.change_view("settings"))
        file_menu.add_command(label='Exit', command=root.destroy)

        menu.add_cascade(label="File", menu=file_menu)
        menu.add_cascade(label="Actions", menu=actions_menu)
        menu.add_cascade(label="Help (H)", command=lambda: self.change_view("console"))

        Frame(
            root,
            bg=self.color2,
            height=2,
            bd=0
        ).grid(row=1, column=0, columnspan=2, sticky="ew")

        self.view = self.viewManager.get("console")
        self.set_view(self.view)

    def set_view(self, view: SMSView):
        self.view = view
        self.view.grid(row=2, column=0, sticky="nswe")

    def hide_current_view(self):
        self.view.grid_forget()

    def change_view(self, name: str):
        self.hide_current_view()
        self.set_view(self.viewManager.get(name))
