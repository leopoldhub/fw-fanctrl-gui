from threading import Thread

import customtkinter

from fw_fanctrl_gui.dto.ServiceStatus import ServiceStatus


class ReloadConfigurationButton:
    reload_configuration_button: customtkinter.CTkButton

    def __init__(self, main_window, master, builder, fanctrl_service, service_cached_status):
        self.main_window = main_window
        self.master = master
        self.builder = builder
        self.fanctrl_service = fanctrl_service
        self.service_cached_status = service_cached_status

        self.reload_configuration_button = self.main_window.builder.get_object(
            "ctk_button_reload", builder
        )
        self.reload_configuration_button.configure(
            command=lambda: Thread(target=self.reload_configuration_button_command).start()
        )

        self.service_cached_status.connect(self.update_status_event)

    def update_status_event(self, service_status: ServiceStatus):
        if service_status.active != service_status.previously_active or service_status.previous_status.data is None:
            self.update_reload_configuration_button(service_status.reachable)

    def reload_configuration_button_command(self):
        if not self.service_cached_status.previous_status.reachable:
            return
        self.fanctrl_service.reload()

    def update_reload_configuration_button(self, reachable):
        if not reachable:
            self.reload_configuration_button.configure(state=customtkinter.DISABLED)
            return
        if self.reload_configuration_button.cget("state") == customtkinter.DISABLED:
            self.reload_configuration_button.configure(state=customtkinter.NORMAL)
