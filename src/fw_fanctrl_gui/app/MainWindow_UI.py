import pathlib

import customtkinter as ctk
import pygubu
from PIL import Image, ImageTk

from fw_fanctrl_gui import RESOURCES_PATH, UIS_PATH


class MainWindow_UI:
    def __init__(
        self,
        master=None,
        translator=None,
        on_first_object_cb=None,
        data_pool=None,
        icon_path=None,
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
        self.main_window: ctk.CTk = self.builder.get_object("ctk_window_main", master)
        self.builder.connect_callbacks(self)

        icon_path = pathlib.Path(icon_path)
        self.icon_image = Image.open(icon_path)
        tk_image = ImageTk.PhotoImage(self.icon_image)
        self.main_window.iconphoto(True, tk_image)

    def run(self):
        self.main_window.mainloop()
