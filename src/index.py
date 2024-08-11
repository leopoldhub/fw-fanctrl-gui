import argparse
import sys

from PySide6.QtWidgets import QApplication

from src.GCBypass import GCBYPASS
from src.app.MainWindow import main
from src.service.FanctrlService import FanctrlService


def parseArgs():
    parser = argparse.ArgumentParser(
        prog="fw-fanctrl",
        description="simple pyside Qt6 python gui with system tray for fw-fanctrl",
    )
    parser.add_argument(
        "--background",
        "-b",
        help="do not open the main window on startup",
        action="store_true",
    )
    return parser.parse_args()


def start():
    fanctrlService = FanctrlService()
    app = QApplication()
    app.GCBYPASS = GCBYPASS
    args = parseArgs()
    window = main(args, app, fanctrlService)
    window.GCBYPASS = GCBYPASS
    sys.exit(app.exec())
