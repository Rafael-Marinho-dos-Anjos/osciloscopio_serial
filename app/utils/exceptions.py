class PortNotSelectedException(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class InvalidSerialDeviceException(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class DeviceAlreadySelectedException(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class InvalidUpdatingFrequenceException(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class InvalidSizeException(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class InvalidEntrySizeException(Exception):
    def __init__(self, *args):
        super().__init__(*args)