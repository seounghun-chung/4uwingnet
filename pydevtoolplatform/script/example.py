if __name__ == '__main__':
    # __main__ is used for executing this script in windows python
    # if there are not compatilbility codes in windows python,
    # the methods in console.py is not available.
    # Because features class object is not assigned.
    #
    # e.g) c:\pydevtoolplatform> python -m script.example

    from console.console import *
    from features.example import Example
    from features.example2 import Example2
    
    example = Example()    # for connecting class object with console.py
    example2 = Example2()   # for connecting class object with console.py
else:
    # it means that this script was executed in PyQt GUI
    example1 = classObjectList["Example"]
    example2 = classObjectList["Example2"]

func1()    # == example1.func1()
func2()    # == example2.func2()
