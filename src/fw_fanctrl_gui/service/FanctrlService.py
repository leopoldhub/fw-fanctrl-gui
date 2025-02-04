import json
import subprocess
from json import JSONDecodeError

from fw_fanctrl_gui.exception.FailedCommandException import FailedCommandException
from fw_fanctrl_gui.exception.ServiceException import ServiceException


class FanctrlService:
    command = "fw-fanctrl --output-format=JSON"

    def runCommand(self, command):
        process = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            text=True,
        )
        if process.returncode == 0:
            return json.loads(str(process.stdout).strip())
        try:
            raise FailedCommandException(json.loads(str(process.stderr).strip()))
        except JSONDecodeError:
            raise ServiceException(str(process.stderr))

    def getAll(self):
        return self.runCommand(f"{self.command} print all")

    def getActive(self):
        return self.runCommand(f"{self.command} print active")["active"]

    def getCurrentStrategy(self):
        return self.runCommand(f"{self.command} print current")["strategy"]

    def getStrategies(self):
        return self.runCommand(f"{self.command} print list")["strategies"]

    def reload(self):
        return self.runCommand(f"{self.command} reload")["strategy"]

    def use(self, strategy):
        return self.runCommand(f'{self.command} use "{strategy}"')["strategy"]

    def reset(self):
        return self.runCommand(f"{self.command} reset")["strategy"]

    def pause(self):
        return self.runCommand(f"{self.command} pause")

    def resume(self):
        return self.runCommand(f"{self.command} resume")["strategy"]
