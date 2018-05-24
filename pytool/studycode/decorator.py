from functools import wraps

def _isconnect(self):
    if hasattr(self, 'a'):
        if self.a is None:
            return False
        else:
            print("ok") 
            return True
    
    
def isconnect(method):
    @wraps(method)
    def _impl(self, *args, **kwargs):
        ret = _isconnect(self)
        if ret is True:
            method(self, *args, **kwargs)
        else:
            print("skip function call")
    return _impl

class A(object):
    def __init__(self):
        self.a = None

    @isconnect
    def func(self,b):
        print(self.a)

    @isconnect
    def func2(self,b):
        print(self.a+1)        
        
classA = A()
classA.a = 43
classA.func(3)
classA.func2(4)