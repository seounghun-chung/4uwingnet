from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from PyQt5.QtCore import QObject, pyqtSignal, Qt, QEventLoop
from PyQt5.QtWidgets import QApplication, QFileDialog

from copytoolui import Ui_MainWindow
from pathlib import Path
from multiprocessing import cpu_count

from multiprocessing.pool import Pool
from multiprocessing import Lock, Queue, Process, freeze_support, Value


import threading
import shutil
import logging
import os
import time

logger = logging.getLogger("copytool")
    
class MySignal(QObject):
    sig = pyqtSignal(int,name="mysig")
    txt = pyqtSignal(str,name="mysig.str")
    
    def __init__(self):
        QObject.__init__(self)
        
    def set(self,p):        
        self.sig.emit(p)
        QApplication.processEvents(QEventLoop.AllEvents)
    def text(self,p):
        self.txt.emit(p)
        
_mysigtest = MySignal()        
def _mycallback(q,sharedVar):
#    print(os.getpid(), sharedVar.value)
    _mysigtest.text(str(q))
    pass
    
def readonly_handler(func, path, execinfo): 
    os.chmod(path, 128) #or os.chmod(path, stat.S_IWRITE) from "stat" module
    func(path)
    
def _filecopy(src, dst, q, callback, sharedVar):
    __change_target_path = lambda x : Path(str(x).replace(src, dst))    # replace the path from src to dst
    while(q.empty() is not True):
        orgin = q.get()
        if callback is not None:
            callback(orgin,sharedVar)
            sharedVar.value = q.qsize()
        else:
            print(os.getpid(), orgin)
        shutil.copy('\\\\?\\'+str(orgin), __change_target_path(orgin))
        print(os.getpid(), orgin)
class CopyTool(object):
    def __init__(self):
        self._filequeue = Queue()
    
    def search(self, src, exclude_pattern = ["**/*.pyc"], include_pattern = ["**/*.py"]):
        """
        search all files under 'src'
        include_patterns will be searched althought it was included in exclude_pattern
        
        e.g.) exclude_pattern = ['**/*.py'], include_pattern = ['target/*.py']
              -> only target/*.py will be searched and other .py files will not be searched
        """
        src = os.path.abspath(src)
     
        _target = Path(src)
        _target._flavour.casefold = lambda x : x    # basic windows path don't distinguish upper / lower case.
        allfiles = list(_target.glob("**/*"))
        
        exclude = list()
        for _ex in exclude_pattern:
            exclude += _target.glob(_ex)        
        
        include = list()
        for _in in include_pattern:
            include += _target.glob(_in)  
            
        _target_path = set(allfiles) - set(exclude) | set(include)
        
        _target_dir_path = sorted(list(x for x in _target_path if x.is_dir() is True))
        _target_file_path = sorted(list(x for x in _target_path if x.is_file() is True))
        
        return _target_dir_path, _target_file_path
        
    def copy(self, src, dst, complete_handler, sharedVar,exclude_pattern = ["**/*.pyc"], include_pattern = ["**/*.py"]):
        src = os.path.abspath(src)
        dst = os.path.abspath(dst)
        target = None
        
        if target is None:
            _target_dir, _target_file = self.search(src, exclude_pattern=exclude_pattern, include_pattern=include_pattern)
        else:
            if type(target) != tuple:
                logger.error("type of target must be tuple, use output of self.search for input param")
                return False
            else:
                _target_dir, _target_file = target

        if not os.path.exists(dst):
            os.mkdir(dst)
        else:
            shutil.rmtree(dst,onerror=readonly_handler)
            os.mkdir(dst)            

        for ii in _target_file:
            self._filequeue.put(ii)
        
        self.__mkdir(src,dst,_target_dir)
        
        res = list()                
        for ii in range(0,4):
            res.append(Process(target=_filecopy, args=(src,dst, self._filequeue, complete_handler, sharedVar)))
        for ii in res:
            ii.start()
#        for ii in res:
#            ii.join()

    def __mkdir(self, src, dst, _target_dir):
        __change_target_path = lambda x : Path(str(x).replace(src, dst))    # replace the path from src to dst
        for orgin in _target_dir:
            target = __change_target_path(orgin)
            if not os.path.exists(target):
                os.mkdir(target)

    
class DiaglogSample(Ui_MainWindow):    
    def __init__(self, *argv):
        global _mysigtest
        
        super().setupUi(*argv)
        self.pushButton_6.clicked.connect(lambda : self._btn_copytree())
        self.CopyTool = CopyTool()
        self.progressBar.setRange(0,4000)
        self.remain = Value('i',0)

        self._sig = MySignal()
        self._sig.sig.connect(lambda x : self.progressBar.setValue(x))
        _mysigtest.txt.connect(lambda x : self._dummy(x))
        
    def _btn_copytree(self):
        start = time.time()   
        th = threading.Thread(target=self._progress_thread)
        th.start()     
#        th2 = threading.Thread(target=self.CopyTool.copy,args=('C:\\Users\\seoung\\workspace', 'C:\\test', _mycallback, self.remain,))
#        th2.start()          
        self.CopyTool.copy('C:\\Users\\seoung\\workspace', 'C:\\test', complete_handler=_mycallback, sharedVar=self.remain)
        
        print(time.time() - start)

    def _progress_thread(self):
        while(self.remain.value == 0):
            print("busy wait", self.remain.value)
            import time
            time.sleep(0.1)
        
        total = self.remain.value
        while(self.remain.value >= 10):
            out = total - self.remain.value
            print(out)
            time.sleep(0.1)
            self._sig.set(out)
#            print(total - self.remain.value)
#            self.progressBar.setValue(out)     
        self.progressBar.setValue(total)  
        print("complete")
        
    def _dummy(self, x):
        print("dummy", x)
        
if __name__ == "__main__":
    import sys
    freeze_support()
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QMainWindow()
    ui = DiaglogSample(Form)
    Form.show()
    sys.exit(app.exec_())
    
#    a = CopyTool()
#    b = a.search('C:\\Users\\seoung\\workspace')
#    start = time.time()
#    a.copy('C:\\Users\\seoung\\workspace', 'C:\\test', target = b)
#    print(time.time() - start)
#    #pool = Pool(cpu_count())
#    #pool.apply_async(a.copy, args=('C:\\Users\\seoung\\workspace\\pytool\\pydevtoolplatform', 'D:/merong'), kwds={'target': b})
#    #pool.join()