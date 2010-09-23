from PyQt4 import QtCore, QtGui, uic
from pluginmgr import Device
import os
import models
import utils
import json

class FolderDevice(object):
    """Syncs a set of tags' books to a folder, using specified
    formats.
    """
    def __init__(self, tags, formats, name, folder):
        self.tags = tags
        self.formats = formats
        self.name = name
        self.folder = folder

    def sync(self):
        """Perform the sync"""
        print "syncing tags:", self.tags, "to folder", self.folder 

class NewDeviceDialog(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        uifile = os.path.join(
            os.path.abspath(
                os.path.dirname(__file__)),'new_device.ui')
        self.w = uic.loadUi(uifile, self)
        self.w.choose.clicked.connect(self.choosePath)
        for f in ["epub","pdf","mobi","fb2","txt"]:
            self.w.formats.addItem(f)

        for t in models.Tag.query.order_by("name").all():
            self.w.tags.addItem(t.name)

    def choosePath(self):
        d = QtGui.QFileDialog.getExistingDirectory()
        self.path.setText(d)

class FolderDevicePlugin(Device, QtCore.QObject):
    """This device syncs books to a folder.
    For example, you could use this to make books available via
    dropbox to a device that supports it"""

    name = "Tag Folders"

    def __init__(self):
        QtCore.QObject.__init__(self)
        self.loadDevices()

    def deviceActions(self):
        """Returns a list of actions, one for each device"""
        return [QtGui.QAction(d.name, self, triggered = d.sync)
            for d in self.devices]

    def actionNew(self):
        self.action = QtGui.QAction("New Sync Folder", None)
        self.action.triggered.connect(self.newfolder)
        return self.action

    def saveDevices(self):
        devfn = os.path.join(utils.BASEPATH,"folderdevices")
        f = open(devfn,"w+")
        data = json.dumps([{"tags": d.tags,
                    "formats": d.formats,
                    "name": d.name,
                    "folder": d.folder
                } for d in self.devices])
        print data
        f.write(data)
        f.close()

    def loadDevices(self):
        self.devices = []
        try:
            devfn = os.path.join(utils.BASEPATH,"folderdevices")
            f = open(devfn,"r")
            data = json.loads(f.read())
            f.close()
            for d in data:
                self.devices.append(FolderDevice(**d))
        except ValueError:
            pass
        
    def newfolder(self):
        while True:
            self.w = NewDeviceDialog()
            r = self.w.exec_()
            if r == self.w.Rejected:
                return
            # Accepted, create new device
            tags = [unicode(i.text()) for i in self.w.tags.selectedItems()]
            print tags
            formats = [unicode(i.text()) for i in self.w.formats.selectedItems()]
            print formats
            path = unicode(self.w.path.text())
            name = unicode(self.w.name.text())

            # Validate
            if not path or not name or not tags:
                QtGui.QMessageBox.critical(None, "Error", "Path, name and tags are mandatory")
                continue
            self.devices.append(FolderDevice(tags, formats, name, path))
            self.saveDevices()
            break
            