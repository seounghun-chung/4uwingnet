from interface.can import can
from interface.lan import lan
from interface.serial import serial


class Command(object):
    def __init__(self):
        self.InterfaceCan = can.Can()
        self.InterfaceLan = lan.Lan()
        self.InterfaceSerial = serial.Serial()

    def connect(self, type):
        if   type == "can":
            pass
        elif type == "lan":
            pass
        elif type == 'serial':
            pass
        else:
            pass

    def Download(self):
        pass

    def FlashDump(self):
        pass

    def DownloadAfterReset(self):
        pass