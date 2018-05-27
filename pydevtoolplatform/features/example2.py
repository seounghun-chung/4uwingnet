from console import console

class Example2(object):
    def __init__(self):
        console.RegisterCommandClassObjectMap(self)
        pass
        
    def func2(self):
        print("func2")