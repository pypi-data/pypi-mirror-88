from controller import Device


class FDevice(Device):
    def __init__(self):
        super(FDevice, self).__init__()

    def debug(self):
        print(self.__dict__)


fdevice = FDevice()
fdevice.debug()
