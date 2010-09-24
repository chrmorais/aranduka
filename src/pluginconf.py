import os
from PyQt4 import QtCore, QtGui, uic
from utils import SCRIPTPATH
from pluginmgr import manager

class PluginSettings(QtGui.QDialog):
    def __init__(self, parent = None):
        QtGui.QDialog.__init__(self, parent)

        uifile = os.path.join(SCRIPTPATH,'pluginconf.ui')
        uic.loadUi(uifile, self)
        self.ui = self
        self.pages = {}
        for category in manager.getCategories():
            w = QtGui.QScrollArea()
            l = QtGui.QVBoxLayout()
            w.setLayout(l)
            for plugin in manager.getPluginsOfCategory(category):
                l.addWidget(PluginWidget(plugin))
            l.addStretch(1)
            self.toolBox.addItem(w, category)
        self.toolBox.removeItem(0)

class PluginWidget(QtGui.QWidget):
    def __init__(self, plugin, parent = None):
        QtGui.QWidget.__init__(self, parent)

        uifile = os.path.join(SCRIPTPATH,'pluginwidget.ui')
        uic.loadUi(uifile, self)
        self.ui = self

        self.enabled.setText(plugin.name)
    