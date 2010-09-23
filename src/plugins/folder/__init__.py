from PyQt4 import QtGui, uic
from pluginmgr import Device
import os
import models

class FolderDevice(Device):
    """This device syncs books to a folder.
    For example, you could use this to make books available via
    dropbox to a device that supports it"""

    def actionNew(self):
        self.action = QtGui.QAction("New Sync Folder", None)
        self.action.triggered.connect(self.newfolder)
        return self.action

    def newfolder(self):
        uifile = os.path.join(
            os.path.abspath(
                os.path.dirname(__file__)),'new_device.ui')
        self.w = uic.loadUi(uifile)
    
        for f in ["epub","pdf","mobi","fb2","txt"]:
            self.w.formats.addItem(f)

        for t in models.Tag.query.order_by("name").all():
            self.w.tags.addItem(t.name)
        self.w.exec_()
        
        
        
    