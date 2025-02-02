from fw_fanctrl_gui.app.section.service.ResetStrategyButton import ResetStrategyButton
from fw_fanctrl_gui.app.section.service.CurrentStrategyOption import (
    CurrentStrategyOption,
)
from fw_fanctrl_gui.app.section.service.PauseResumeButton import PauseResumeButton
from fw_fanctrl_gui.app.section.service.ReloadConfigurationButton import (
    ReloadConfigurationButton,
)


class ServiceSection:
    pause_resume_button: PauseResumeButton
    reload_configuration_button: ReloadConfigurationButton
    current_strategy_option: CurrentStrategyOption
    reset_strategy_button: ResetStrategyButton

    def __init__(
        self, main_window, master, builder, fanctrl_service, timed_status_service
    ):
        self.main_window = main_window
        self.master = master
        self.builder = builder
        self.fanctrl_service = fanctrl_service
        self.timed_status_service = timed_status_service

        self.pause_resume_button = PauseResumeButton(
            self.main_window,
            self.master,
            self.builder,
            self.fanctrl_service,
            self.timed_status_service,
        )

        self.reload_configuration_button = ReloadConfigurationButton(
            self.main_window,
            self.master,
            self.builder,
            self.fanctrl_service,
            self.timed_status_service,
        )

        self.current_strategy_option = CurrentStrategyOption(
            self.main_window,
            self.master,
            self.builder,
            self.fanctrl_service,
            self.timed_status_service,
        )

        self.reset_strategy_button = ResetStrategyButton(
            self.main_window,
            self.master,
            self.builder,
            self.fanctrl_service,
            self.timed_status_service,
        )
