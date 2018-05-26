from unittest.case import TestCase
import unittest
import time
import traceback

print("hello load script!")
info()
setinfo(4)
print(getinfo())
ret = WaitForResponse(100,2)
print(ret)
print("test complete")