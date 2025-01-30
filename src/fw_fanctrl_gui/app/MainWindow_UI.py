import pathlib

import customtkinter as ctk
import pygubu

from fw_fanctrl_gui import RESOURCES_PATH, UIS_PATH


class MainWindow_UI:
    def __init__(
        self, master=None, translator=None, on_first_object_cb=None, data_pool=None
    ):
        self.master = master
        self.builder = pygubu.Builder(
            translator=translator,
            on_first_object=on_first_object_cb,
            data_pool=data_pool,
        )
        self.builder.add_resource_paths([pathlib.Path(RESOURCES_PATH)])
        self.builder.add_from_file(pathlib.Path(UIS_PATH.joinpath("main.ui")))
        # Main widget
        self.mainwindow: ctk.CTk = self.builder.get_object("ctk_window_main", master)
        self.builder.connect_callbacks(self)

    def run(self):
        self.mainwindow.mainloop()
