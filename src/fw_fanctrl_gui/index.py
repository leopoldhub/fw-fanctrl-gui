import argparse
import shlex
import sys

import customtkinter

from fw_fanctrl_gui import RESOURCES_PATH
from fw_fanctrl_gui.app.MainWindow import MainWindow
from fw_fanctrl_gui.app.SystemTray import SystemTray
from fw_fanctrl_gui.service.FanctrlService import FanctrlService

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("dark-blue")


def parse_args(args=None):
    if args is None:
        args = shlex.split(shlex.join(sys.argv[1:]))
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
    return parser.parse_args(args)


def start():
    args = parse_args()
    fanctrl_service = FanctrlService()
    app = MainWindow(
        background_start=args.background,
        icon_path=RESOURCES_PATH.joinpath("icon.ico"),
        fanctrl_service=fanctrl_service,
    )
    tray = SystemTray(app)
    tray.run()
    app.run()
