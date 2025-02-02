from threading import Thread

import customtkinter
from fw_fanctrl_gui.dto.ServiceStatus import ServiceStatus


class ResetStrategyButton:
    reset_strategy_button: customtkinter.CTkButton

    def __init__(
        self, main_window, master, builder, fanctrl_service, timed_status_service
    ):
        self.main_window = main_window
        self.master = master
        self.builder = builder
        self.fanctrl_service = fanctrl_service
        self.timed_status_service = timed_status_service

        self.reset_strategy_button = self.main_window.builder.get_object(
            "ctk_button_reset_strategy", builder
        )
        self.reset_strategy_button.configure(
            command=lambda: Thread(target=self.reset_strategy_button_command).start()
        )

        self.timed_status_service.connect(self.update_status_event)

    def update_status_event(self, service_status: ServiceStatus):
        if (
            service_status.active != service_status.previously_active
            or service_status.previous_status.data is None
            or (
                service_status.reachable
                and (
                    not service_status.previously_reachable
                    or service_status.data["default"]
                    != service_status.previous_status.data["default"]
                )
            )
        ):
            self.update_reset_strategy_button(
                service_status.reachable,
                (
                    (lambda: service_status.data["default"])()
                    if service_status.active
                    else None
                ),
            )

    def reset_strategy_button_command(self):
        if not self.timed_status_service.previous_status.reachable:
            return
        self.fanctrl_service.reset()
        self.timed_status_service.updateStatus()

    def update_reset_strategy_button(self, reachable, default_behaviour):
        if not reachable or default_behaviour:
            self.reset_strategy_button.configure(state=customtkinter.DISABLED)
            return
        if self.reset_strategy_button.cget("state") == customtkinter.DISABLED:
            self.reset_strategy_button.configure(state=customtkinter.NORMAL)
