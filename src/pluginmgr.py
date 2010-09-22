"""Plugin manager for Aranduka, using Yapsy"""

from PyQt4 import QtCore, QtGui

import logging
#logging.basicConfig(level=logging.DEBUG)

import os
from yapsy.PluginManager import PluginManager
from yapsy.IPlugin import IPlugin

# These classes define our plugin categories
class ShelveView(QtCore.QObject):
    title = "base ShelveView"
    itemText = "BASE"
    
    def __init__(self):
        print "INIT: ", self.title
        self.widget = None
        QtCore.QObject.__init__(self)
        
    def setWidget(self, widget):
        self.widget = widget

    def treeItem(self):
        """Returns a QTreeWidgetItem representing this
        plugin"""
        return QtGui.QTreeWidgetItem([self.itemText])

    @QtCore.pyqtSlot()
    def doSearch(self, *args):
        self.operate(search = unicode(self.widget.searchWidget.text.text()))
    
class BookStore(object): pass
class Converter(object): pass

manager = PluginManager(
    categories_filter={
        "ShelveView": ShelveView,
        "BookStore": BookStore,
        "Converter": Converter,
    })

plugindir = os.path.join(
            os.path.abspath(
            os.path.dirname(__file__)),'plugins')

manager.setPluginPlaces([plugindir])

