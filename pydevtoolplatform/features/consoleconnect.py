""" This class will be used for inherition.
    It will be conneced with console.py for
    referencing this class object.
    This class can be inherited when class is assigned only at one time"""

from console import console

class ConsoleConnect(object):
    def __init__(self, *argv):
        self._argv = argv
        console.RegisterCommandClassObjectMap(self)
