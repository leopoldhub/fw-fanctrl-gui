from fw_fanctrl_gui.app.section.service.CurrentStrategyOption import CurrentStrategyOption
from fw_fanctrl_gui.app.section.service.PauseResumeButton import PauseResumeButton
from fw_fanctrl_gui.app.section.service.ReloadConfigurationButton import ReloadConfigurationButton


class ServiceSection:
    pause_resume_button: PauseResumeButton
    reload_configuration_button: ReloadConfigurationButton
    current_strategy_option: CurrentStrategyOption

    def __init__(self, main_window, master, builder, fanctrl_service, service_cached_status):
        self.main_window = main_window
        self.master = master
        self.builder = builder
        self.fanctrl_service = fanctrl_service
        self.service_cached_status = service_cached_status

        self.pause_resume_button = PauseResumeButton(self.main_window, self.master, self.builder, self.fanctrl_service,
                                                     self.service_cached_status)

        self.reload_configuration_button = ReloadConfigurationButton(self.main_window, self.master, self.builder,
                                                                     self.fanctrl_service,
                                                                     self.service_cached_status)

        self.current_strategy_option = CurrentStrategyOption(self.main_window, self.master, self.builder,
                                                             self.fanctrl_service,
                                                             self.service_cached_status)
