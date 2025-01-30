from threading import Thread

import customtkinter

from fw_fanctrl_gui.dto.ServiceStatus import ServiceStatus


class CurrentStrategyOption:
    current_strategy_option: customtkinter.CTkOptionMenu

    def __init__(self, main_window, master, builder, fanctrl_service, service_cached_status):
        self.main_window = main_window
        self.master = master
        self.builder = builder
        self.fanctrl_service = fanctrl_service
        self.service_cached_status = service_cached_status

        self.current_strategy_option = self.main_window.builder.get_object(
            "ctk_option_current_strategy", self.main_window.master
        )
        self.current_strategy_option.configure(
            command=lambda v: Thread(target=self.current_strategy_option_command, args=[v]).start()
        )

        self.service_cached_status.connect(self.update_status_event)

    previous_strategies = None

    def update_status_event(self, service_status: ServiceStatus):
        strategies = None
        current_strategy = None
        if service_status.reachable:
            # TODO: implement strategy list print in "print all" and clean buffer
            strategies = self.fanctrl_service.getStrategies()
            current_strategy = service_status.data["strategy"]
        if (
            service_status.previous_status.data is None or
            service_status.reachable != service_status.previously_reachable or
            (service_status.reachable and service_status.previously_reachable and
             service_status.data["strategy"] != service_status.previous_status.data["strategy"]) or
            strategies != self.previous_strategies):
            self.previous_strategies = strategies
            self.update_current_strategy_option(service_status.reachable, strategies, current_strategy)

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
        if not self.service_cached_status.previous_status.reachable:
            return
        self.fanctrl_service.use(val)
