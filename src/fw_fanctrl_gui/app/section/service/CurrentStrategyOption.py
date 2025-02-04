from threading import Thread

import customtkinter


class CurrentStrategyOption:
    current_strategy_option: customtkinter.CTkOptionMenu

    def __init__(self, main_window, master, builder, api_business):
        self.main_window = main_window
        self.master = master
        self.builder = builder
        self.api_business = api_business

        self.current_strategy_option = self.main_window.builder.get_object(
            "ctk_option_current_strategy", self.main_window.master
        )
        self.current_strategy_option.configure(
            command=lambda v: Thread(target=self.command, args=[v], daemon=True).start()
        )

        self.api_business.strategy_changed_signal.connect(self.update)

    def update(self, data):
        reachable = data[0]
        current_strategy = data[1]
        strategies = data[2]
        if not reachable:
            self.current_strategy_option.configure(state=customtkinter.DISABLED)
            self.current_strategy_option.configure(values=[])
            self.current_strategy_option.set("")
            return
        self.current_strategy_option.configure(values=strategies)
        self.current_strategy_option.set(current_strategy)
        if self.current_strategy_option.cget("state") == customtkinter.DISABLED:
            self.current_strategy_option.configure(state=customtkinter.NORMAL)

    def command(self, val):
        if not self.api_business.status().reachable:
            return
        self.api_business.use(val)
