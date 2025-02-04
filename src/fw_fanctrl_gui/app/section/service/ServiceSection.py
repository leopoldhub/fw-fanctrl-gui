from fw_fanctrl_gui.app.section.service.CurrentStrategyOption import (
    CurrentStrategyOption,
)
from fw_fanctrl_gui.app.section.service.PauseResumeButton import PauseResumeButton
from fw_fanctrl_gui.app.section.service.ReloadConfigurationButton import (
    ReloadConfigurationButton,
)
from fw_fanctrl_gui.app.section.service.ResetStrategyButton import ResetStrategyButton


class ServiceSection:
    pause_resume_button: PauseResumeButton
    reload_configuration_button: ReloadConfigurationButton
    current_strategy_option: CurrentStrategyOption
    reset_strategy_button: ResetStrategyButton

    def __init__(self, main_window, master, builder, api_business):
        self.main_window = main_window
        self.master = master
        self.builder = builder
        self.api_business = api_business

        self.pause_resume_button = PauseResumeButton(
            self.main_window,
            self.master,
            self.builder,
            self.api_business,
        )

        self.reload_configuration_button = ReloadConfigurationButton(
            self.main_window,
            self.master,
            self.builder,
            self.api_business,
        )

        self.current_strategy_option = CurrentStrategyOption(
            self.main_window,
            self.master,
            self.builder,
            self.api_business,
        )

        self.reset_strategy_button = ResetStrategyButton(
            self.main_window,
            self.master,
            self.builder,
            self.api_business,
        )
