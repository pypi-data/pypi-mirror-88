from numpy.lib.function_base import select


class Config:
    def __init__(self) -> None:
        super().__init__()
        self.device = "cpu"
        self.conf = {}

    def set(self, setting, value):
        self.conf[setting] = value

    def has(self, setting):
        return setting in self.conf

    def get(self, setting, default=None):
        return self.conf.get(setting, default)

    def set_channels(self, channels):
        self.set("channels", channels)

    def set_start_frame(self, sframe):
        self.set("fstart", sframe)

    def set_end_frame(self, eframe):
        self.set("fend", eframe)

    def use_device(self, device):
        self.device = device
