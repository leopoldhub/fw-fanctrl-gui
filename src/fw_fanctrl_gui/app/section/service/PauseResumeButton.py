from threading import Thread

import customtkinter

from fw_fanctrl_gui.dto.ServiceStatus import ServiceStatus


class PauseResumeButton:
    pause_resume_button: customtkinter.CTkButton

    def __init__(self, main_window, master, builder, api_business):
        self.main_window = main_window
        self.master = master
        self.builder = builder
        self.api_business = api_business

        self.pause_resume_button = self.main_window.builder.get_object(
            "ctk_button_pause_resume", master
        )
        self.pause_resume_button.configure(
            command=lambda: Thread(target=self.command, daemon=True).start()
        )

        self.api_business.active_changed_signal.connect(self.update)

    def command(self):
        if not self.api_business.status().reachable:
            return
        if self.api_business.status().active:
            self.api_business.pause()
        else:
            self.api_business.resume()

    def update(self, data):
        reachable = data[0]
        active = data[1]
        if not reachable:
            self.pause_resume_button.configure(state=customtkinter.DISABLED)
            return
        if active:
            self.pause_resume_button.configure(text="Pause")
        else:
            self.pause_resume_button.configure(text="Resume")
        if self.pause_resume_button.cget("state") == customtkinter.DISABLED:
            self.pause_resume_button.configure(state=customtkinter.NORMAL)
