import customtkinter

from fw_fanctrl_gui.app.MainWindow_UI import MainWindow_UI
from fw_fanctrl_gui.app.section.service.ServiceSection import ServiceSection
from fw_fanctrl_gui.business.APIBusiness import APIBusiness
from fw_fanctrl_gui.dto.ServiceStatus import ServiceStatus


class MainWindow(MainWindow_UI):
    api_business: APIBusiness

    radio_status_indicator: customtkinter.CTkRadioButton

    service_section: ServiceSection

    def __init__(
        self, master=None, background_start=None, fanctrl_service=None, icon_path=None
    ):
        super().__init__(master, icon_path=icon_path)
        self.master = master
        self.api_business = APIBusiness(fanctrl_service)

        self.main_window.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.radio_status_indicator = self.builder.get_object(
            "ctk_radio_status", self.master
        )

        self.service_section = ServiceSection(
            self,
            self.master,
            self.builder,
            self.api_business,
        )

        if background_start:
            self.main_window.withdraw()

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
        self.main_window.withdraw()

    def run(self):
        super().run()
