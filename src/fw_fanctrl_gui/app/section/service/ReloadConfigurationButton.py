from threading import Thread

import customtkinter


class ReloadConfigurationButton:
    reload_configuration_button: customtkinter.CTkButton

    def __init__(self, main_window, master, builder, api_business):
        self.main_window = main_window
        self.master = master
        self.builder = builder
        self.api_business = api_business

        self.reload_configuration_button = self.main_window.builder.get_object(
            "ctk_button_reload", builder
        )
        self.reload_configuration_button.configure(
            command=lambda: Thread(
                target=self.reload_configuration_button_command, daemon=True
            ).start()
        )

        self.api_business.active_changed_signal.connect(self.update)

    def reload_configuration_button_command(self):
        if not self.api_business.status().reachable:
            return
        self.api_business.reload()

    def update(self, data):
        reachable = data[0]
        if not reachable:
            self.reload_configuration_button.configure(state=customtkinter.DISABLED)
            return
        if self.reload_configuration_button.cget("state") == customtkinter.DISABLED:
            self.reload_configuration_button.configure(state=customtkinter.NORMAL)
