import customtkinter as ctk

MIN_POWER = 0
MAX_POWER = 100


def validate_input(string_value, entry, entry_var):
    if string_value == "":
        return True

    if string_value.isdigit():
        print(string_value)
        try:
            int_value = int(string_value)
            if int_value < MIN_POWER:
                entry_var.set(f"{MIN_POWER}")
                return False
            if int_value > MAX_POWER:
                entry_var.set(f"{MIN_POWER}")
                return False
            return True
        except Exception as e:
            print("except")
            print(e)
            return False

    return False


class FanPowerSlider(ctk.CTkFrame):
    def __init__(self, parent, temperature=0, initial_power=50):
        super().__init__(parent)

        self.initial_power = initial_power
        self.temperature = temperature

        self.pack(side=ctk.LEFT, fill=ctk.Y, expand=True, padx=1)

        self.slider = ctk.CTkSlider(
            self,
            from_=MIN_POWER,
            to=MAX_POWER,
            orientation="vertical",
            height=300,
            width=20,
        )
        self.slider.set(self.initial_power)
        self.slider.pack(fill=ctk.Y, expand=True)

        self.int_value_label = ctk.CTkLabel(
            self,
            text=f"{self.temperature}\N{DEGREE SIGN}C",
            width=60,
            font=("Arial", 18),
        )
        self.int_value_label.pack()

        self.percent_label = ctk.CTkLabel(
            self, text=f"{self.initial_power} %", width=60, font=("Arial", 18)
        )
        self.percent_label.pack()

        self.slider.configure(command=self.on_slider_move)

        self.main_button_1 = ctk.CTkButton(
            master=self,
            fg_color="transparent",
            border_width=0,
            width=60,
            text="🗑",
            font=("Arial", 18),
        )
        self.main_button_1.pack()

        entry_var = ctk.StringVar()
        entry = ctk.CTkEntry(self, width=100, textvariable=entry_var)
        validate_cmd = self.register(
            lambda p: validate_input(p, entry, entry_var)
        )  # Register the validation function
        entry.configure(validate="key", validatecommand=(validate_cmd, "%P"))
        entry.pack(side="left", padx=(0, 5))

    def on_slider_move(self, value):
        power = int(value)
        self.percent_label.configure(text=f"{power}%")
        self.slider.set(power)
