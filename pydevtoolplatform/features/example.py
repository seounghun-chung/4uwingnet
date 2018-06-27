from threading import *
import time
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore

class TestThread(QThread):
    # 쓰레드의 커스텀 이벤트
    # 데이터 전달 시 형을 명시해야 함
#    threadEvent = QtCore.pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__()
        self.n = 0
        self.main = parent
        self.isRun = False
        self.time = 1000
        
    def run(self):
        while self.isRun:
#            print('thread : ' + str(self.n), type(self.time))
            self.main.func5()
            # 'threadEvent' 이벤트 발생
            # 파라미터 전달 가능(객체도 가능)
#            self.threadEvent.emit(self.n)

            self.n += 1
            self.msleep(self.time)
            
class Example():
    _running = False
    def __init__(self):
        self.th = TestThread(self)
    
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
            time.sleep(0.01)
    def func2(self):
        self.th.isRun = True
        self.th.start()
    def func3(self):
        self.th.isRun = False
        
    def func5(self):
        print(time.time())
        
    def func4(self):
        for ii in range(0,1000):
            print(ii)
            
if __name__ == '__main__':
    A = Example()
    A.func2()
    time.sleep(100)