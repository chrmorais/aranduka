from PyQt4 import QtCore, QtGui
from pluginmgr import Tool
import multiprocessing
import sys, os

class Plugin(Tool):

    _proc = None
    _action = None
    
    def action(self):
        if self._action is None:
            self._action = QtGui.QAction("Publish Catalog", None)
            self._action.setCheckable(True)
            print "ISC", self._action.isCheckable()
            self._action.toggled.connect(self.publish)
        return self._action

    def publish(self, enable):
        print 
        if not self._proc:
            dirname = os.path.join(
                os.path.abspath(
                    os.path.dirname(__file__)))
            sys.path.append(dirname)
            publisher = __import__('publisher')
            self._proc = multiprocessing.Process(target = publisher.real_publish)
            self._proc.daemon = True
            self._proc.start()


