import sys
from PySide6.QtWidgets import QApplication

from src.GCBypass import GCBYPASS
from src.app.MainWindow import main
from src.service.FanctrlService import FanctrlService


def start():
    fanctrlService = FanctrlService()
    app = QApplication(sys.argv)
    app.GCBYPASS = GCBYPASS
    window = main(app, fanctrlService)
    window.GCBYPASS = GCBYPASS
    sys.exit(app.exec())

