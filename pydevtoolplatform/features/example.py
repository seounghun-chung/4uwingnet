from threading import *
import time

class Example():
    _running = False
    def func1(self):
        print("func1")
        
    def run(self):
        """run thread"""
        t1 = Thread(target = self._thread)
        self._running = True
        t1.daemon = True
        t1.start()
        
    def stop(self):
        """ stop thread """
        self._running = False
        
    def _thread(self):
        while(self._running is True):
            print("hello", time.time())
            time.sleep(0.5)
        
