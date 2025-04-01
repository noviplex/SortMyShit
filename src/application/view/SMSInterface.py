from tkinter import Tk, font as tkFont

from src.application.view.layout.SMSView import SMSView

from src.domain.event.ChangeViewEvent import ChangeViewEvent

from src.infrastructure.repository.SettingsRepository import SettingsRepository

from src.manager.ViewManager import ViewManager

class SMSInterface:
    def __init__(
        self, 
        root: Tk,
        settingsRepository: SettingsRepository,
        changeViewEvent: ChangeViewEvent,
        viewManager = ViewManager
    ):
        self.viewManager = viewManager

        changeViewEvent.subscribe(self.changeView)

        default_font = tkFont.nametofont("TkDefaultFont")
        default_font.configure(size=14)

        root.title("SortMyShit")
        root.geometry('1600x900')
        root.resizable(width=False, height=False)
        root.configure(bg=settingsRepository.loadOne("backgroundColor"))

        navbar = self.viewManager.get("navBar")
        navbar.grid(row=0, column=0, sticky='w')
        
        view = self.viewManager.get("home")
        self.setView(view)
        
        root.mainloop()

    def setView(self, view: SMSView):
        self.view = view
        self.view.grid(row=1, column=0, sticky="nswe")

    def hideCurrentView(self):
        self.view.grid_forget()

    def changeView(self, name: str):
        self.hideCurrentView()
        self.setView(self.viewManager.get(name))