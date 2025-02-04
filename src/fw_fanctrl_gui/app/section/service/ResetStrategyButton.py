from threading import Thread

import customtkinter


class ResetStrategyButton:
    reset_strategy_button: customtkinter.CTkButton

    def __init__(self, main_window, master, builder, api_business):
        self.main_window = main_window
        self.master = master
        self.builder = builder
        self.api_business = api_business

        self.reset_strategy_button = self.main_window.builder.get_object(
            "ctk_button_reset_strategy", builder
        )
        self.reset_strategy_button.configure(
            command=lambda: Thread(target=self.command, daemon=True).start()
        )

        self.api_business.is_default_change_signal.connect(self.update)

    def command(self):
        if not self.api_business.status().reachable:
            return
        self.api_business.reset()

    def update(self, data):
        reachable = data[0]
        default_behaviour = data[1]
        if not reachable or default_behaviour:
            self.reset_strategy_button.configure(state=customtkinter.DISABLED)
            return
        if self.reset_strategy_button.cget("state") == customtkinter.DISABLED:
            self.reset_strategy_button.configure(state=customtkinter.NORMAL)
