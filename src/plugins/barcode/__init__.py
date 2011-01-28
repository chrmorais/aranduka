from PyQt4 import QtCore, QtGui
from pluginmgr import Tool
import sys, os

class Plugin(Tool):

    _proc = None
    
    def action(self):
        self.action = QtGui.QAction("Scan Barcode", None)
        self.action.triggered.connect(self.scan)
        return self.action

    def scan(self): 
        pass


