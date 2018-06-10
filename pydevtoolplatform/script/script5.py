import threading
import time

def func():
    for ii in range(0,10):
        print("test!")
        time.sleep(1)

th = threading.Thread(target = func)
th.daemon = True
th.start()
print("seounghun")
time.sleep(1)
print("hihi")
