from PyQt4 import QtCore, QtGui
from pluginmgr import Tool
import multiprocessing
import Queue
import sys, os

class Plugin(Tool):

    _proc = None
    
    def action(self):
        self._action = QtGui.QAction("Publish Catalog", None)
        self._action.triggered.connect(self.publish)
        return self._action

    def check_url (self):
        publisher = __import__('publisher')
        try:
            url = publisher.queue.get(False)
            if url is not None:
                QtGui.QMessageBox.information(None, \
                                              u'Catalog published', \
                                              u'You can access your catalog on: %s'%url, \
                                              QtGui.QMessageBox.Ok, \
                                              QtGui.QMessageBox.NoButton, \
                                              QtGui.QMessageBox.NoButton)
                self.timer.stop()
        except Queue.Empty:
            pass

    def publish(self):        
        if not self._proc:
            dirname = os.path.join(
                os.path.abspath(
                    os.path.dirname(__file__)))
            sys.path.append(dirname)

            self.timer = QtCore.QTimer()
            self.timer.timeout.connect(self.check_url)
            self.timer.start(1000)

            publisher = __import__('publisher')
            self._proc = multiprocessing.Process(target = publisher.real_publish)
            self._proc.daemon = True
            self._proc.start()
