"""Plugin manager for Aranduka, using Yapsy"""

from PyQt4 import QtCore, QtGui

import logging
#logging.basicConfig(level=logging.DEBUG)

import os
from yapsy.PluginManager import PluginManager
from yapsy.IPlugin import IPlugin
import utils

# These classes define our plugin categories

class Tool(object):
    """A plugin that gets added to the Tools menu in the main.ui"""
    pass

class ShelveView(QtCore.QObject):
    """Plugins that inherit this class display the contents
    of your book database."""
    
    title = "Base ShelveView"
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



class BookStore(object):
    """Plugins that inherit this class give access to some
    mechanism for book acquisition"""

    title = "Base Bookstore"
    itemText = "BASE"

    def __init__(self):
        print "INIT:", self.title
        self.widget = None

    def treeItem(self):
        """Returns a QTreeWidgetItem representing this
        plugin"""
        return QtGui.QTreeWidgetItem([self.itemText])

    def setWidget (self, widget):
        self.widget = widget

    @QtCore.pyqtSlot()
    def doSearch(self, *args):
        self.search(unicode(self.widget.searchWidget.text.text()))


class Converter(object): pass

manager = PluginManager(
    categories_filter={
        "ShelveView": ShelveView,
        "BookStore": BookStore,
        "Converter": Converter,
        "Tool": Tool,
    })

manager.setPluginPlaces(utils.PLUGINPATH)

