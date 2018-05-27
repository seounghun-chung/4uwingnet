""" This class will be used for inherition.
    It will be conneced with console.py for
    referencing this class object.
"""

from console import console

class ConsoleConnect(object):
    def __init__(self, *argv):
        """
        argv[0] will be used as class variable in console.
        example)
            Allocate the class variable with name in CODE
            ConsoleConnect("connector")
            
            In GUI, you call this method as the way of below 
            >>> connect.method(param)
        """ 
        if len(argv) > 0:
            """ for using in console command """
            console.RegisterObjectInConsole(self, argv[0])
        else:
            """ not using in console command """
            pass