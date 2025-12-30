from tkinter import Tk, Frame, BooleanVar, StringVar

from src.application.view.SMSView import SMSView
from src.application.component.SMSLabel import SMSLabel
from src.application.component.SMSCheckButton import SMSCheckButton
from src.application.component.SMSInputWithLabel import SMSInputWithLabel

from src.infrastructure.repository.SettingsRepository import SettingsRepository


class SettingsView(SMSView):
    def __init__(
        self,
        container: Tk,
        settings_repository: SettingsRepository,
    ):
        self.settings_repository = settings_repository

        self.color1 = self.settings_repository.fetch_one("color1")
        self.color2 = self.settings_repository.fetch_one("color2")
        self.color3 = self.settings_repository.fetch_one("color3")
        self.color4 = self.settings_repository.fetch_one("color4")

        super().__init__(
            container=container,
            bg=self.color1,
            height=500,
        )

        self.create_view()

    def create_view(self):
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.grid_propagate(0)

        SMSLabel(
            container=self,
            bg=self.color1,
            fg=self.color4,
            text="Settings",
            font=("Arial", 24)
        ).grid(row=0, column=0, sticky='w')

        SMSLabel(
            container=self,
            bg=self.color1,
            fg=self.color4,
            text="Sort Files"
        ).grid(row=1, column=0, sticky='w')

        Frame(
            self,
            bg=self.color2,
            height=1,
            bd=0
        ).grid(row=2, column=0, columnspan=2, sticky="ew")

        self.__create_input_with_label(
            text="Folder to Sort",
            setting_name="folder_to_process",
            value=self.settings_repository.fetch_one("folder_to_process")
        ).grid(row=3, column=0, sticky='w')

        self.__create_input_with_label(
            text="Destination folder",
            setting_name="destination_folder",
            value=self.settings_repository.fetch_one("destination_folder")
        ).grid(row=4, column=0, sticky='w')

        self.__create_setting_check_button(
            setting_name="keep_original_files",
            text="Do not delete files in original folders",
        ).grid(row=5, column=0, sticky='w')

        SMSLabel(
            container=self,
            text="Remove Duplicates",
            bg=self.color1,
            fg=self.color4,
        ).grid(row=6, column=0, sticky='w')

        Frame(
            self,
            bg=self.color2,
            height=1,
            bd=0
        ).grid(row=7, column=0, columnspan=2, sticky="ew")

        self.__create_input_with_label(
            text="Folder to Process",
            setting_name="remove_duplicates_folder",
            value=self.settings_repository.fetch_one("remove_duplicates_folder")
        ).grid(row=8, column=0, sticky='w')

        self.__create_setting_check_button(
            setting_name="binary_search",
            text="Binary comparison (if disabled, will do a filename comparison instead)",
        ).grid(row=9, column=0, sticky='w')

        self.__create_setting_check_button(
            setting_name="binary_search_large_files",
            text="Enable binary comparison for large files (warning: may crash on large files)",
        ).grid(row=9, column=1, sticky='w')

        SMSLabel(
            container=self,
            bg=self.color1,
            fg=self.color4,
            text="General"
        ).grid(row=10, column=0, sticky='w')

        Frame(
            self,
            bg=self.color2,
            height=1,
            bd=0
        ).grid(row=11, column=0, columnspan=2, sticky="ew")

        self.__create_setting_check_button(
            setting_name="log_output_in_file",
            text="Log output in logfile",
        ).grid(row=12, column=0, sticky='w')

    def __create_setting_check_button(self, setting_name: str, text: str):
        boolean_var = BooleanVar()
        boolean_var.set(self.settings_repository.fetch_one(setting_name))
        return SMSCheckButton(
            container=self,
            text=text,
            variable=boolean_var,
            bg=self.color1,
            fg=self.color4,
            command=lambda: self.settings_repository.save_one(setting_name, boolean_var.get())
        )

    def __create_input_with_label(self, text: str, setting_name: str, value: str):
        setting_var = StringVar()
        setting_var.set(value=value)
        setting_var.trace_add(
            "write",
            lambda name, index, mode, setting_var=setting_var:
            self.__change_input_with_label_setting(
                setting_name=setting_name,
                setting_var=setting_var
            )
        )

        return SMSInputWithLabel(
            container=self,
            text=text,
            entry_bg=self.color3,
            bg=self.color1,
            fg=self.color4,
            setting_var=setting_var,
        )

    def __change_input_with_label_setting(
        self,
        setting_name: str,
        setting_var: StringVar
    ):
        self.settings_repository.save_one(setting_name, setting_var.get())
