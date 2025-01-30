import argparse

import customtkinter

from fw_fanctrl_gui.app.MainWindow import MainWindow
from fw_fanctrl_gui.service.FanctrlService import FanctrlService

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("dark-blue")


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
    # aaaPath=RESOURCES_PATH.joinpath("ui").joinpath("aaa.ui")
    # print(aaaPath)
    # with open(aaaPath) as f: s = f.read()
    # print(s)
    # exit(0)
    fanctrlService = FanctrlService()
    app = MainWindow(fanctrl_service=fanctrlService)
    app.run()
