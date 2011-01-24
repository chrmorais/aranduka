from PyQt4 import QtCore, QtGui
from pluginmgr import Tool
import multiprocessing
import sys, os

class Plugin(Tool):

    _proc = None
    
    def action(self):
        self.action = QtGui.QAction("Publish Catalog", None)
        self.action.triggered.connect(self.publish)
        return self.action

    def publish(self):        
        if not self._proc:
            dirname = os.path.join(
                os.path.abspath(
                    os.path.dirname(__file__)))
            sys.path.append(dirname)
            publisher = __import__('publisher')
            self._proc = multiprocessing.Process(target = publisher.real_publish)
            self._proc.daemon = True
            self._proc.start()


