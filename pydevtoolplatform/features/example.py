from features.consoleconnect import ConsoleConnect

class Example(ConsoleConnect):
    def func1(self):
        print("func1 ", self._argv)
