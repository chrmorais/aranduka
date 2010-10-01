"""Plugin manager for Aranduka, using Yapsy"""

from PyQt4 import QtCore, QtGui

import logging
#logging.basicConfig(level=logging.DEBUG)

import os
from yapsy.PluginManager import PluginManager
from yapsy.IPlugin import IPlugin
import utils

# These classes define our plugin categories

class Guesser(object):
    """These plugins take a filename and guess data from it.
    They can read the file itself, parse it and get data,
    or could look it up on the internet"""
    pass

class Device(object):
    """A plugin that represents a device to read books.
    These get added in the 'Devices' menu
    """
    pass

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
        self.widget.updateShelves.connect(self.updateShelves)
        self.widget.updateBook.connect(self.updateBook)

    def updateShelves(self):
        """Refresh the book listings"""
        pass

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

    def updateBook(self, book):
        """Update the item of this specific book, because
        it has been edited"""
        pass

    operate = showGrid

    def updateShelves(self):
        """Update the whole listing"""
        self.operate()

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
        "Device": Device,
    })

manager.setPluginPlaces(utils.PLUGINPATH)

