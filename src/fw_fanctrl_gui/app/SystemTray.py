import importlib
import os
import signal
from threading import Thread


class SystemTray:

    def __init__(self, main_window):
        pystray = importlib.import_module("pystray")
        Menu = pystray.Menu
        Item = pystray.MenuItem
        self.main_window = main_window
        self.menu = [
            Item("Reachable", (lambda: None), enabled=False),
            Menu.SEPARATOR,
            Item("Pause/Resume", (lambda: None)),
            Item(
                "Reload configuration",
                self.main_window.api_business.reload,
            ),
            Menu.SEPARATOR,
            Item("Current: aaa", (lambda: None), enabled=False),
            Item("Choose strategy", Menu((Item("", (lambda: None), enabled=False)))),
            Item("Reset to Default", self.main_window.api_business.reset),
            Menu.SEPARATOR,
            Item("Show", self.on_open, default=True),
            Item("Exit", self.on_exit),
        ]
        self.icon = pystray.Icon("icon", self.main_window.icon_image, "name", self.menu)
        self.main_window.api_business.reachable_changed_signal.connect(
            self.on_reachable_change
        )
        self.main_window.api_business.active_changed_signal.connect(
            self.on_active_change
        )
        self.main_window.api_business.strategy_changed_signal.connect(
            self.on_strategy_change
        )
        self.main_window.api_business.is_default_change_signal.connect(
            self.on_default_change
        )

    def on_open(self, icon, item):
        self.main_window.main_window.deiconify()

    def on_exit(self, icon, item):
        print("Exiting...")
        icon.stop()
        os.kill(os.getpid(), signal.SIGKILL)

    def run(self):
        Thread(target=self.icon.run, daemon=True).start()

    def on_reachable_change(self, data):
        reachable = data[0]
        self.menu[0] = clone_menu_item(
            self.menu[0], text="Reachable" if reachable else "Unreachable"
        )
        self.menu[2] = clone_menu_item(self.menu[2], enabled=reachable)
        self.menu[3] = clone_menu_item(self.menu[3], enabled=reachable)
        self.menu[6] = clone_menu_item(self.menu[6], enabled=reachable)
        self.menu[7] = clone_menu_item(self.menu[7], enabled=reachable)
        self.icon.menu = self.menu
        self.icon.update_menu()

    def on_active_change(self, data):
        active = data[1]
        self.menu[2] = clone_menu_item(
            self.menu[2],
            text="Pause" if active else "Resume",
            action=(
                self.main_window.api_business.pause
                if active
                else self.main_window.api_business.resume
            ),
        )
        self.icon.menu = self.menu
        self.icon.update_menu()

    def on_strategy_change(self, data):
        reachable = data[0]
        strategy = data[1]
        strategies = data[2]
        pystray = importlib.import_module("pystray")
        Menu = pystray.Menu
        Item = pystray.MenuItem
        if not reachable:
            self.menu[5] = clone_menu_item(self.menu[5], text="Current: =====")
            self.menu[6] = clone_menu_item(
                self.menu[6], action=Menu(Item("", (lambda: None), enabled=False))
            )
            return
        self.menu[5] = clone_menu_item(self.menu[5], text=f"Current: {strategy}")
        strategies_menu = [
            Item(
                st,
                (lambda _, s=st: self.main_window.api_business.use(s)),
            )
            for st in strategies
        ]
        self.menu[6] = clone_menu_item(self.menu[6], action=Menu(*strategies_menu))
        self.icon.menu = self.menu
        self.icon.update_menu()

    def on_default_change(self, data):
        reachable = data[0]
        default_behaviour = data[1]
        if not reachable:
            self.menu[7] = clone_menu_item(self.menu[7], enabled=reachable)
            return
        self.menu[7] = clone_menu_item(self.menu[7], enabled=(not default_behaviour))
        self.icon.update_menu()


def clone_menu_item(menu_item, text=None, action=None, enabled=None):
    if text is None:
        text = menu_item.text
    if action is None:
        action = menu_item._action
    if enabled is None:
        enabled = menu_item.enabled
    pystray = importlib.import_module("pystray")
    Item = pystray.MenuItem
    return Item(
        text,
        action,
        checked=menu_item.checked,
        radio=menu_item.radio,
        default=menu_item.default,
        visible=menu_item.visible,
        enabled=enabled,
    )
