import json
import sys

from blinker import Signal

from fw_fanctrl_gui.dto.ServiceStatus import ServiceStatus
from fw_fanctrl_gui.exception.FailedCommandException import FailedCommandException
from fw_fanctrl_gui.service.FanctrlService import FanctrlService
from fw_fanctrl_gui.utils.RepeatingTimer import RepeatingTimer


class TimedStatusService(Signal):
    fanctrl_service: FanctrlService

    repeating_timer: RepeatingTimer

    previous_status: ServiceStatus = ServiceStatus(
        reachable=False,
        previously_reachable=False,
        active=False,
        previously_active=False,
        data=None,
        previous_status=None,
    )

    def __init__(self, fanctrl_service):
        super().__init__("status-update")
        self.fanctrl_service = fanctrl_service
        self.repeating_timer = RepeatingTimer(self.updateStatus, 1000)

    def updateStatus(self):
        fetch_result = None
        try:
            fetch_result = self.fanctrl_service.getAll()
        except FailedCommandException as e:
            fetch_result = e.args[0]
        except Exception as e:
            print(e, file=sys.stderr)
            fetch_result = json.loads('{"status": "error"}')
            fetch_result["reason"] = str(e)
        finally:
            previously_reachable = self.previous_status.reachable
            previously_active = self.previous_status.active

            reachable = fetch_result["status"] == "success"
            active = (lambda: fetch_result["active"])() if reachable else False
            status = ServiceStatus(
                reachable=reachable,
                previously_reachable=previously_reachable,
                active=active,
                previously_active=previously_active,
                data=fetch_result,
                previous_status=self.previous_status,
            )

            self.previous_status = status

            self.send(status)

    def start(self):
        self.repeating_timer.start()
