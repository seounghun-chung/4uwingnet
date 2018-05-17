import time
from threading import Thread, Lock
from queue import Queue, Empty

class Serial(object):
    def __init__(self):
        self.semaphore = Lock()
        self.th = None
        self._running = False
        self.count = 9
        self.q = Queue(maxsize = 100000)

    def connect(self):
        pass

    def WaitForResponse(self, msg, timeout = 1):
        ret = False
        # clear queue for getting current q value
        with self.semaphore:
            while not self.q.empty():
                self.q.get_nowait()

        _start_time = time.time()

        while (time.time() - _start_time < timeout):
            try:
                r = self.q.get(timeout = timeout)
            except Empty:
                r = 0

            if (r == msg):
                ret = True
                break
            else:
                ret = False

            print("cnt:%d " % self.count, end="")
            print("%f wait response, cnt:%s" % (time.time(), r))
            # recv serial msg
        return ret

    def run(self):
        self.th = Thread(target = self._run)
        self.th.daemon = True
        self.th.start()

    def stop(self):
        self._running = False

    def _run(self):
        self._running = True
        while self._running is True:
            with self.semaphore:
                # recv serial msg
                if self.q.full() is True:   # circular queue
                    r = self.q.get()
                self.q.put(self.count)
                self.count += 1
                print("%f running...%d " % (time.time(),self.count))
                time.sleep(0.1)

    def test(self):
        with self.semaphore:
            self.count = 99999