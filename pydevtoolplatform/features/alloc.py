"""
All class object used in console of GUI app is allocated in here.
This method is for running the script in stand alone except GUI interface.

script execution in GUI app
-> GUI console and GUI qtcode used class object getted in here
script execution except GUI app
-> ClassObject variable can be used through defining from features.alloc import *
"""

from features.example import Example
from features.example2 import Example2

isExistGlobalVariable = lambda x : x in globals()
listOfAllocatedClassObject = list() # it is used for help() functions

if isExistGlobalVariable("example") is False:
    example = Example()
    listOfAllocatedClassObject.append("example")
if isExistGlobalVariable("example2") is False:
    example2 = Example2()
    listOfAllocatedClassObject.append("example2")