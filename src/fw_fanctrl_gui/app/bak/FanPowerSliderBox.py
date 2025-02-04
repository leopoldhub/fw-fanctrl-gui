import customtkinter as ctk

from fw_fanctrl_gui.app.FanPowerSlider import FanPowerSlider

SPEED_CURVE = [
    (0, 0),
    (45, 0),
    (65, 15),
    (65, 15),
    (65, 15),
    (65, 15),
    (65, 15),
    (65, 15),
    (70, 25),
    (75, 35),
    (85, 40),
]


class FanPowerSliderBox(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.pack(fill=ctk.BOTH, expand=True)

        self.canvas = ctk.CTkCanvas(
            self, background=parent.cget("fg_color"), highlightthickness=0
        )
        self.canvas.pack(side=ctk.TOP, fill=ctk.BOTH, expand=True)

        self.scrollbar_x = ctk.CTkScrollbar(
            self, orientation="horizontal", command=self.canvas.xview
        )
        self.scrollbar_x.pack(side=ctk.BOTTOM, fill=ctk.X)

        self.canvas.configure(xscrollcommand=self.scrollbar_x.set)

        self.main_frame = ctk.CTkFrame(self.canvas)
        self.canvas_window = self.canvas.create_window(
            (0, 0), window=self.main_frame, anchor="nw"
        )

        self.sliders = []
        for point in SPEED_CURVE:
            FanPowerSlider(self.main_frame, point[0], point[1])

        self.main_frame.bind("<Configure>", self.update_canvas)
        self.canvas.bind("<Configure>", self.update_canvas)  # Check on canvas resize
        self.bind("<Configure>", self.update_canvas)  # Check on window resize

    def update_canvas(self, event=None):
        # Update the scroll region to encompass all content
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        # Determine whether the scrollbar is needed
        canvas_width = self.canvas.winfo_width()
        content_width = self.main_frame.winfo_reqwidth()

        print(
            f"Canvas width: {canvas_width}, Content width: {content_width}"
        )  # Debugging

        if content_width > canvas_width:
            # Show scrollbar if content exceeds canvas width
            self.scrollbar_x.pack(side=ctk.BOTTOM, fill=ctk.X)
        else:
            # Hide scrollbar if content fits within the canvas
            self.scrollbar_x.pack_forget()
