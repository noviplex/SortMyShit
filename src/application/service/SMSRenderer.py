from tkinter import Tk, font as tkFont

from src.application.view.SMSView import SMSView
from src.application.component.SMSButton import SMSButton
from src.application.component.SMSButtonContainer import SMSButtonContainer

from src.infrastructure.repository.SettingsRepository import SettingsRepository

from src.manager.ViewManager import ViewManager


class SMSRenderer:
    def __init__(
        self,
        settingsRepository: SettingsRepository,
    ):
        self.settingsRepository = settingsRepository

    def render(self, root: Tk, viewManager: ViewManager):
        backgroundColor = self.settingsRepository.loadOne("backgroundColor")
        fontColor = self.settingsRepository.loadOne("fontColor")

        self.viewManager = viewManager

        default_font = tkFont.nametofont("TkDefaultFont")
        default_font.configure(size=14)

        root.title("SortMyShit")
        root.geometry('1600x900')
        root.resizable(width=False, height=False)
        root.configure(bg=backgroundColor)

        navbar = SMSButtonContainer(
            root,
            backgroundColor=backgroundColor,
            direction="horizontal",
            width=300,
            height=500,
            padx=10,
            pady=10,
        )
        navbar.setButtons([
            SMSButton(
                navbar,
                backgroundColor=backgroundColor,
                fontColor=fontColor,
                text="Home",
                command=lambda: self.changeView("home"),
                width=10,
                height=1,
            ),
            SMSButton(
                navbar,
                backgroundColor=backgroundColor,
                fontColor=fontColor,
                text="Settings",
                command=lambda: self.changeView("settings"),
                width=10,
                height=1,
            ),
        ])
        navbar.grid(row=0, column=0, sticky='w')

        self.view = self.viewManager.get("home")
        self.setView(self.view)

    def setView(self, view: SMSView):
        self.view = view
        self.view.grid(row=1, column=0, sticky="nswe")

    def hideCurrentView(self):
        self.view.grid_forget()

    def changeView(self, name: str):
        self.hideCurrentView()
        self.setView(self.viewManager.get(name))
