import subprocess

from src.exception.ServiceException import ServiceException


class FanctrlService:

    def runCommand(self, command):
        process = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            text=True,
        )
        if process.returncode != 0:
            raise ServiceException(str(process.stderr).strip())
        return str(process.stdout).strip()

    def getCurrentStrategy(self):
        return self.runCommand("fw-fanctrl print current")

    def getStrategies(self):
        return self.runCommand("fw-fanctrl print list").splitlines()

    def reload(self):
        return self.runCommand("fw-fanctrl reload")

    def use(self, strategy):
        return self.runCommand(f"fw-fanctrl use \"{strategy}\"")

    def reset(self):
        return self.runCommand("fw-fanctrl reset")

    def pause(self):
        return self.runCommand("fw-fanctrl pause")

    def resume(self):
        return self.runCommand("fw-fanctrl resume")
