from blinker import Signal

from fw_fanctrl_gui.dto.ServiceStatus import ServiceStatus
from fw_fanctrl_gui.service.FanctrlService import FanctrlService
from fw_fanctrl_gui.service.TimedStatusService import TimedStatusService


class APIBusiness:
    service_cached_status: TimedStatusService
    fanctrl_service: FanctrlService

    strategy_changed_signal: Signal
    active_changed_signal: Signal
    reachable_changed_signal: Signal
    is_default_change_signal: Signal

    def __init__(self, fanctrl_service):
        super().__init__()
        self.fanctrl_service = fanctrl_service
        self.service_cached_status = TimedStatusService(self.fanctrl_service)

        self.strategy_changed_signal = Signal()
        self.active_changed_signal = Signal()
        self.reachable_changed_signal = Signal()
        self.is_default_change_signal = Signal()

        self.service_cached_status.connect(self.on_status_change)

        self.service_cached_status.start()

    def status(self):
        return self.service_cached_status.previous_status

    def control(self):
        self.service_cached_status.updateStatus()

    def reload(self):
        self.fanctrl_service.reload()
        self.control()

    def pause(self):
        self.fanctrl_service.pause()
        self.control()

    def resume(self):
        self.fanctrl_service.resume()
        self.control()

    def use(self, strategy):
        self.fanctrl_service.use(strategy)
        self.control()

    def reset(self):
        self.fanctrl_service.reset()
        self.control()

    def on_status_change(self, service_status: ServiceStatus):
        self.check_strategy_change(service_status)
        self.check_active_change(service_status)
        self.check_reachable_change(service_status)
        self.check_is_default_change(service_status)

    def check_strategy_change(self, service_status: ServiceStatus):
        if (
            service_status.reachable == service_status.previously_reachable
            and service_status.previous_status.data is not None
            and (
                not service_status.reachable
                or (
                    service_status.data["strategy"]
                    == service_status.previous_status.data["strategy"]
                    and service_status.data["configuration"]["data"]["strategies"]
                    == service_status.previous_status.data["configuration"]["data"][
                        "strategies"
                    ]
                )
            )
        ):
            return

        if not service_status.reachable:
            self.strategy_changed_signal.send((False, None, None))
            return

        self.strategy_changed_signal.send(
            (
                service_status.reachable,
                service_status.data["strategy"],
                service_status.data["configuration"]["data"]["strategies"],
            )
        )

    def check_active_change(self, service_status: ServiceStatus):
        if (
            service_status.active != service_status.previously_active
            or service_status.previous_status.data is None
        ):
            self.active_changed_signal.send(
                (service_status.reachable, service_status.active)
            )

    def check_reachable_change(self, service_status: ServiceStatus):
        if (
            service_status.reachable != service_status.previously_reachable
            or service_status.previous_status.data is None
        ):
            self.reachable_changed_signal.send((service_status.reachable,))

    def check_is_default_change(self, service_status: ServiceStatus):
        if (
            service_status.reachable == service_status.previously_reachable
            and service_status.previous_status.data is not None
            and (
                not service_status.reachable
                or (
                    service_status.data["default"]
                    == service_status.previous_status.data["default"]
                )
            )
        ):
            return

        if not service_status.reachable:
            self.is_default_change_signal.send((service_status.reachable, None))
            return

        self.is_default_change_signal.send(
            (service_status.reachable, service_status.data["default"])
        )
