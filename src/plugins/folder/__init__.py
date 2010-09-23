from PyQt4 import QtGui
from pluginmgr import Device

class FolderDevice(Device):
    """This device syncs books to a folder.
    For example, you could use this to make books available via
    dropbox to a device that supports it"""

    def actionNew(self):
        self.action = QtGui.QAction("New Sync Folder", None)
        self.action.triggered.connect(self.newfolder)
        return self.action

    def newfolder(self):
        print "Create new sync folder"
        
    