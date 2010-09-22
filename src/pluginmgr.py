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

    def showGrid(self, search=None):
        """Show a grid containing the (possibly filtered) books."""
        pass
    
    def showList(self, search=None):
        """Show a list containing the (possibly filtered) books."""
        pass

    operate = showGrid

    @QtCore.pyqtSlot()
    def doSearch(self, *args):
        """Perform a search and display the results"""
        self.operate(search = unicode(self.widget.searchWidget.text.text()))

    def shelfContextMenu(self, point):
        """Show context menu for the book where the user
        right-clicked.
        If you are not using QListViews to display the
        books, you probably need to reimplement this"""
        
        shelf = self.sender()
        item = shelf.currentItem()
        book = item.book
        point = shelf.mapToGlobal(point)
        self.widget.bookContextMenuRequested(book, point)



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

