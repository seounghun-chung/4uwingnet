from console import console

class Example(object):
    def __init__(self):
        console.RegisterCommandClassObjectMap(self)
        pass
        
    def func1(self):
        print("func1")