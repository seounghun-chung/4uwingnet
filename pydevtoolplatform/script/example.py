if __name__ == '__main__':
    # __main__ is used for executing this script in windows python
    # if there are not compatilbility codes in windows python,
    # the methods in console.py is not available.
    # Because features class object is not assigned.
    #
    # e.g) c:\pydevtoolplatform> python -m script.example
    
    from features.example import Example
    from features.example2 import Example2
    
    abc = Example("example")    # for connecting class object with console.py
    efs = Example2("example2")   # for connecting class object with console.py
    
    # Load console after registering ClassObject in console
    # not doing it, registered var name is not updated in globals()
    from console.console import *       
else:
    # it means that this script was executed in PyQt GUI
    pass
    
example.func1()  
example2.func2()
