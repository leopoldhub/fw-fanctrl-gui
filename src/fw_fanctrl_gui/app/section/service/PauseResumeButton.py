from threading import Thread

import customtkinter

from fw_fanctrl_gui.dto.ServiceStatus import ServiceStatus


class PauseResumeButton:
    pause_resume_button: customtkinter.CTkButton

    def __init__(
        self, main_window, master, builder, fanctrl_service, timed_status_service
    ):
        self.main_window = main_window
        self.master = master
        self.builder = builder
        self.fanctrl_service = fanctrl_service
        self.timed_status_service = timed_status_service

        self.pause_resume_button = self.main_window.builder.get_object(
            "ctk_button_pause_resume", master
        )
        self.pause_resume_button.configure(
            command=lambda: Thread(target=self.pause_resume_button_command).start()
        )

        self.timed_status_service.connect(self.update_status_event)

    def update_status_event(self, service_status: ServiceStatus):
        if (
            service_status.active != service_status.previously_active
            or service_status.previous_status.data is None
        ):
            self.update_pause_resume_button(
                service_status.reachable, service_status.active
            )

    def pause_resume_button_command(self):
        if not self.timed_status_service.previous_status.reachable:
            return
        if self.timed_status_service.previous_status.active:
            self.fanctrl_service.pause()
        else:
            self.fanctrl_service.resume()
        self.timed_status_service.updateStatus()

    def update_pause_resume_button(self, reachable, active):
        if not reachable:
            self.pause_resume_button.configure(state=customtkinter.DISABLED)
            return
        if active:
            self.pause_resume_button.configure(text="Pause")
        else:
            self.pause_resume_button.configure(text="Resume")
        if self.pause_resume_button.cget("state") == customtkinter.DISABLED:
            self.pause_resume_button.configure(state=customtkinter.NORMAL)
