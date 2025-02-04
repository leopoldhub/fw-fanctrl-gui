import time
from threading import Thread


class RepeatingTimer(Thread):
    target = None
    delayMs = None

    def __init__(self, target, delayMs):
        super().__init__(target=self._run, daemon=True)
        self.target = target
        self.delayMs = delayMs
        self.daemon = True

    def _run(self):
        while True:
            self.target()
            time.sleep(self.delayMs / 1000)
