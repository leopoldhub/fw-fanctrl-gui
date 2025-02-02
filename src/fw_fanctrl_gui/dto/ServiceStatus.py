class ServiceStatus:
    def __init__(
        self,
        reachable: bool,
        previously_reachable: bool,
        active: bool,
        previously_active: bool,
        data,
        previous_status,
    ):
        self.reachable = reachable
        self.previously_reachable = previously_reachable
        self.active = active
        self.previously_active = previously_active
        self.data = data
        self.previous_status = previous_status
