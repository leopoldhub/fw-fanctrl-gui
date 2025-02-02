from threading import Thread

import customtkinter
from fw_fanctrl_gui.dto.ServiceStatus import ServiceStatus


class CurrentStrategyOption:
    current_strategy_option: customtkinter.CTkOptionMenu

    def __init__(
        self, main_window, master, builder, fanctrl_service, timed_status_service
    ):
        self.main_window = main_window
        self.master = master
        self.builder = builder
        self.fanctrl_service = fanctrl_service
        self.timed_status_service = timed_status_service

        self.current_strategy_option = self.main_window.builder.get_object(
            "ctk_option_current_strategy", self.main_window.master
        )
        self.current_strategy_option.configure(
            command=lambda v: Thread(
                target=self.current_strategy_option_command, args=[v]
            ).start()
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
                    or service_status.data["strategy"]
                    != service_status.previous_status.data["strategy"]
                    or service_status.data["configuration"]["data"]["strategies"]
                    != service_status.previous_status.data["configuration"]["data"][
                        "strategies"
                    ]
                )
            )
        ):
            self.update_current_strategy_option(
                service_status.reachable,
                service_status.data["configuration"]["data"]["strategies"],
                service_status.data["strategy"],
            )

    def update_current_strategy_option(self, reachable, strategies, current_strategy):
        if not reachable:
            self.current_strategy_option.configure(state=customtkinter.DISABLED)
            self.current_strategy_option.configure(values=[])
            self.current_strategy_option.set("")
            return
        self.current_strategy_option.configure(values=strategies)
        self.current_strategy_option.set(current_strategy)
        if self.current_strategy_option.cget("state") == customtkinter.DISABLED:
            self.current_strategy_option.configure(state=customtkinter.NORMAL)

    def current_strategy_option_command(self, val):
        if not self.timed_status_service.previous_status.reachable:
            return
        self.fanctrl_service.use(val)
        self.timed_status_service.updateStatus()
