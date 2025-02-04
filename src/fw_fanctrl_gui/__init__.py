import importlib.resources

RESOURCES_PATH = importlib.resources.files("fw_fanctrl_gui").joinpath("_resources")
UIS_PATH = RESOURCES_PATH.joinpath("ui")
