from console.console import *
from features.example import Example
from features.example2 import Example2

import unittest
import time

class MyTestCase(unittest.case.TestCase):
    @classmethod
    def setUpClass(self):
        try:
            self.example = example
        except NameError as e:
            # in GUI, example is declared but there is not in console
            self.example = Example()
        try:
            self.example2 = example2
        except NameError as e:
            # in GUI, example is declared but there is not in console        
            self.example2 = Example2()

    def test_func1(self):
        time.sleep(1)
        self.example.func1()

    def test_func2(self):
        self.example2.func2()
