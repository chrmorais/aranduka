import os
from PyQt4 import QtCore, QtGui, uic
from utils import SCRIPTPATH
from pluginmgr import manager
import config
import ui

class PluginSettings(QtGui.QDialog):
    def __init__(self, parent = None):
        QtGui.QDialog.__init__(self, parent)

        uifile = ui.path('pluginconf.ui')
        uic.loadUi(uifile, self)
        self.ui = self
        self.plugin_widgets = []
        enabled_plugins = set(config.getValue("general","enabledPlugins", [None]))
        if enabled_plugins == set([None]):
            enabled_plugins = set()
            #Never configured... enable everything! (will change later ;-)
            for c in manager.getCategories():
                for p in manager.getPluginsOfCategory(c):
                    enabled_plugins.add(p.name)
        for category in manager.getCategories():
            w = QtGui.QScrollArea()
            l = QtGui.QVBoxLayout()
            w.setLayout(l)
            for plugin in manager.getPluginsOfCategory(category):
                pw = PluginWidget(plugin, plugin.name in enabled_plugins)
                self.plugin_widgets.append(pw)
                l.addWidget(pw)
            l.addStretch(1)
            self.toolBox.addItem(w, category)
        print self.page1
        # FIXME: En vez de ocultar page1, sacarlo.
        self.page1.hide()
        self.toolBox.removeItem(0)

    def accept(self):
        enabled_plugins = []
        for pw in self.plugin_widgets:
            if pw.enabled.isChecked():
                enabled_plugins.append(pw.plugin.name)
        config.setValue("general","enabledPlugins", enabled_plugins)
        return QtGui.QDialog.accept(self)

class PluginWidget(QtGui.QWidget):
    def __init__(self, plugin, enabled, parent = None):
        QtGui.QWidget.__init__(self, parent)

        uifile = ui.path('pluginwidget.ui')
        uic.loadUi(uifile, self)
        self.ui = self
        self.plugin = plugin
        self.enabled.setText(plugin.name)
        self.enabled.setChecked(enabled)
    
