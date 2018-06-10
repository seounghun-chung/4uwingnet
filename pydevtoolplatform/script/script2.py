if __name__ == '__main__':
    from console.console import *
    from features.example import Example
    from features.example2 import Example2
    
    example = Example()    # for connecting class object with console.py
    example2 = Example2()   # for connecting class object with console.py

example.func1()
example2.func2()