import random
from multiprocessing import Pool
import time

class DummyManager(object):
    def __init__(self):
        self.cnt = 0
    def server(self):
        while (True):
            time.sleep(1)
            s = random.randint(0, 10000000000)
            self.callback(s)

    def callback(self,s):
        print("asfasfsda")
        return s

    def setinfo(self,s):
        self.cnt = s
    def getinfo(self):
        return self.cnt

    def run(self):
        pool = Pool(processes=2)
        print("tesT")
#        result = pool.apply_async(self.server)
        import threading
        t1 = threading.Thread(target=self.server)
        t1.start()
#        try:
#            print(result.get(timeout=5))
#        except:
#            print("excp")

    def getrnd(self):

        print("dummy")
        return random.randint(0,100)

    def getstatus(self, t):
        return t