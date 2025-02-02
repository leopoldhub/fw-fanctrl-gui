import customtkinter

from fw_fanctrl_gui.app.MainWindow_UI import MainWindow_UI
from fw_fanctrl_gui.app.section.service.ServiceSection import ServiceSection
from fw_fanctrl_gui.dto.ServiceStatus import ServiceStatus
from fw_fanctrl_gui.service.TimedStatusService import ServiceCachedStatus


class MainWindow(MainWindow_UI):
    fanctrl_service = None
    cached_service_details = None
    radio_status_indicator: customtkinter.CTkRadioButton

    service_section: ServiceSection

    def __init__(self, master=None, fanctrl_service=None):
        super().__init__(master)
        self.master = master
        self.fanctrl_service = fanctrl_service

        self.serviceCachedStatus = ServiceCachedStatus(self.fanctrl_service)
        self.serviceCachedStatus.connect(self.update_status_event)

        self.mainwindow.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.radio_status_indicator = self.builder.get_object(
            "ctk_radio_status", self.master
        )

        self.service_section = ServiceSection(
            self,
            self.master,
            self.builder,
            self.fanctrl_service,
            self.serviceCachedStatus,
        )

        self.serviceCachedStatus.repeatingTimer.start()

    def update_status_event(self, service_status: ServiceStatus):
        if (
            service_status.reachable != service_status.previously_reachable
            or service_status.previous_status is None
        ):
            self.update_reachable_status(service_status.reachable)

    def update_reachable_status(self, reachable):
        if reachable:
            self.radio_status_indicator.configure(fg_color="green", text="Reachable")
        else:
            self.radio_status_indicator.configure(fg_color="red", text="Unreachable")

    def on_closing(self):
        self.serviceCachedStatus.repeatingTimer.join(0)
        self.mainwindow.destroy()
        exit(0)
