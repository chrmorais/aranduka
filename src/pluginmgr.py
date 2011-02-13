"""Plugin manager for Aranduka, using Yapsy"""

from PyQt4 import QtCore, QtGui

import logging
logging.basicConfig(level=logging.DEBUG)

import os
from yapsy.PluginManager import PluginManager
from yapsy.IPlugin import IPlugin
import utils
import config

# These classes define our plugin categories

class BasePlugin(object):
    """Base abstract class, you don't want to inherit this one
    but one of the specific plugin classes below."""
    
    name = "Base Plugin"
    title = "Base Plugin"
    configurable = False
    
    # What icons should be visible on the top-right corner
    has_grid = False
    has_list = False
    has_search = False

    # If you implement both showGrid and showList, then
    # set has_grid and has_table to True.
    # If you implement one, set both to False.
    
    def showGrid(self, currentBook = None, search = None):
        """Show contents in a grid, if applicable.
        If currentBook is given, the plugin should attempt
        to ensure that item is visible and selected.
        
        If search is given, it should display the results of
        that search.
        """

    def showList(self, currentBook = None, search = None):
        """Show contents in a list, if applicable.
        If currentBook is given, the plugin should attempt
        to ensure that item is visible and selected.

        If search is given, it should display the results of
        that search.        
        """
    

class Guesser(BasePlugin):
    """These plugins take a filename and guess data from it.
    They can read the file itself, parse it and get data,
    or could look it up on the internet"""

    name = "Base Guesser"
    def __init__(self):
        print "INIT: ", self.name

    def can_guess(self, book):
        """Given a book object, it will return True if it
        believes it can guess something.

        For example, a guesser that parses ePub files will only
        guess if the book has an ePub file assigned.
        """
        return False

    def guess(self, book):
        """Try to fill in as much metadata as possible,
        offer the user alternatives if needed.

        Returns an instance of Metadata, or None.
        """
        return None

class Device(BasePlugin):
    """A plugin that represents a device to read books.
    These get added in the 'Devices' menu
    """

class Tool(BasePlugin):
    """A plugin that gets added to the Tools menu in the main.ui"""

class Importer(BasePlugin):
    """A plugin that gets added to the Tools menu in the main.ui"""
    
class ShelfView(BasePlugin, QtCore.QObject):
    """Plugins that inherit this class display the contents
    of your book database."""
    
    title = "Base ShelfView"
    itemText = "BASE"
    has_grid = True
    has_list = True
    has_search = True
    
    class BookListItemDelegate(QtGui.QStyledItemDelegate):
        def paint (self, painter, option, index):
            """Draws nice list items for books"""
            book = index.data(900)
            if book.isValid():
                book = book.toPyObject()
                r = option.rect;
                v = QtGui.QIcon(index.data(QtCore.Qt.DecorationRole))
                v.paint(painter, QtCore.QRect(r.x()+2, r.y()+2, 124, 124))
                
                text = "%s\nby %s"%(book.title, ', '.join(a.name for a in book.authors) or 'Unknown Author')
                
                painter.drawText(
                    QtCore.QRect(r.x()+128, r.y()+2, 
                        r.width()-128, r.height()-4),
                    QtCore.Qt.AlignLeft,
                    text)
                return
            QtGui.QStyledItemDelegate.paint(self,painter,option,index)
            
        def sizeHint(self, option, index):
            if index.data(900).isValid():
                return QtCore.QSize(128,128)
            return QtGui.QStyledItemDelegate.sizeHint(self,option,index)
    
    
    def __init__(self):
        print "INIT: ", self.title
        self.widget = None
        QtCore.QObject.__init__(self)
        
    def setWidget(self, widget):
        self.widget = widget
        self.widget.updateShelves.connect(self.updateShelves)
        self.widget.updateBook.connect(self.updateBook)

    def treeItem(self):
        """Returns a QTreeWidgetItem representing this
        plugin"""
        return QtGui.QTreeWidgetItem([self.itemText])

    def updateBook(self, book):
        """Update the item of this specific book, because
        it has been edited"""
        pass

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

    def group_books(self, currentBook=None, search=None):
        """Group the books by shelf.
        This should return a dictionary where the keys are
        shelf names, and the values are lists of books"""
        return {}
        
    def showGrid(self, currentBook=None, search=None):
        """Get all books from the DB and show them"""

        if not self.widget:
            print "Call setWidget first"
            return
        self.operate = self.showGrid
        self.items = {}
        
        self.widget.title.setText(self.title)
        css = '''
        ::item {
                padding: 0;
                margin: 0;
                width: 150px;
                height: 150px;
            }
        '''

        # Setup widgetry
        self.widget.stack.setCurrentIndex(0)
        self.shelves = QtGui.QWidget()
        self.shelvesLayout = QtGui.QVBoxLayout()
        self.shelves.setLayout(self.shelvesLayout)

        grouped_books = self.group_books(currentBook, search)
        keys = grouped_books.keys()
        keys.sort()
        for k in keys:
            # Make a shelf
            shelf_label = QtGui.QLabel(k)
            shelf = QtGui.QListWidget()
            self.shelvesLayout.addWidget(shelf_label)
            self.shelvesLayout.addWidget(shelf)
            # Make it look right
            shelf.setStyleSheet(css)
            shelf.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
            shelf.setFrameShape(shelf.NoFrame)
            shelf.setIconSize(QtCore.QSize(128,128))
            shelf.setViewMode(shelf.IconMode)
            shelf.setMinimumHeight(153)
            shelf.setMaximumHeight(153)
            shelf.setMinimumWidth(153*len(grouped_books[k]))
            shelf.setFlow(shelf.LeftToRight)
            shelf.setWrapping(False)
            shelf.setDragEnabled(False)
            shelf.setSelectionMode(shelf.NoSelection)

            # Hook the shelf context menu
            shelf.customContextMenuRequested.connect(self.shelfContextMenu)
            
            # Hook book editor
            shelf.itemActivated.connect(self.widget.on_books_itemActivated)
            
            # Fill the shelf
            for b in grouped_books[k]:
                pixmap = QtGui.QPixmap(b.cover())
                if pixmap.isNull():
                    pixmap = QtGui.QPixmap(b.default_cover())
                icon =  QtGui.QIcon(pixmap.scaledToHeight(128, QtCore.Qt.SmoothTransformation))
                item = QtGui.QListWidgetItem(icon, b.title, shelf)
                item.book = b
                self.items[b.id] = item
                
        
        self.shelvesLayout.addStretch(1)
        self.widget.shelfStack.setWidget(self.shelves)
        
    def showList(self, currentBook = None, search = None):
        """Get all books from the DB and show them"""

        if not self.widget:
            print "Call setWidget first"
            return
        self.operate = self.showList
        self.items = {}
        css = '''
        ::item {
                padding: 0;
                margin: 0;
                height: 48;
            }
        '''

        self.widget.title.setText(self.title)
        # Setup widgetry
        self.widget.stack.setCurrentIndex(0)
        self.shelf = QtGui.QListWidget()
        self.shelf.setItemDelegate(self.BookListItemDelegate(self.shelf))
        # Make it look right
        self.shelf.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.shelf.setFrameShape(self.shelf.NoFrame)
        self.shelf.setDragEnabled(False)
        self.shelf.setSelectionMode(self.shelf.NoSelection)
        self.shelf.setStyleSheet(css)
        self.shelf.setIconSize(QtCore.QSize(48,48))
        # Hook the shelf context menu
        self.shelf.customContextMenuRequested.connect(self.shelfContextMenu)

        # Hook book editor
        self.shelf.itemActivated.connect(self.widget.on_books_itemActivated)
        
        grouped_books = self.group_books(currentBook, search)
        keys = grouped_books.keys()
        keys.sort()
        for a in keys:
            a_item = QtGui.QListWidgetItem(a, self.shelf)
            for b in grouped_books[a]:
                icon = QtGui.QIcon(QtGui.QPixmap(b.cover()).scaledToHeight(128, QtCore.Qt.SmoothTransformation))
                item = QtGui.QListWidgetItem(icon, b.title, self.shelf)
                item.setData(900, b)
                item.book = b
                self.items[b.id] = item

        self.widget.shelfStack.setWidget(self.shelf)


class BookStore(BasePlugin, QtCore.QObject):
    """Plugins that inherit this class give access to some
    mechanism for book acquisition"""

    title = "Base Bookstore"
    itemText = "BASE"
    configurable = False
    
    # These are signals the plugin uses to provide feedback
    # to the main UI
    loadStarted = QtCore.pyqtSignal()
    loadFinished = QtCore.pyqtSignal()
    loadProgress = QtCore.pyqtSignal("int")
    setStatusMessage = QtCore.pyqtSignal("PyQt_PyObject")
    
    def __init__(self):
        print "INIT:", self.title
        self.widget = None
        super(QtCore.QObject, self).__init__(None)    

    def treeItem(self):
        """Returns a QTreeWidgetItem representing this
        plugin"""
        return QtGui.QTreeWidgetItem([self.itemText])

    def setWidget (self, widget):
        self.widget = widget

    @QtCore.pyqtSlot()
    def doSearch(self, *args):
        """Slot that triggers search on this store"""
        self.search(unicode(self.widget.searchWidget.text.text()))
        
    def search(self, key):
        """Search the store contents for this key, and display the results"""
        
class Converter(BasePlugin):
    configurable = False

def isPluginEnabled (name):
    enabled_plugins = set(config.getValue("general","enabledPlugins", [None]))
    print "EP:", enabled_plugins
    if enabled_plugins == set([None]):
        print "FLAG"
        #Never configured... enable everything! (will change later ;-)
        enabled_plugins = set()
        for c in manager.getCategories():
            for p in manager.getPluginsOfCategory(c):
                enabled_plugins.add(p.name)
    return name in enabled_plugins

manager = PluginManager(
    categories_filter={
        "ShelfView": ShelfView,
        "BookStore": BookStore,
        "Converter": Converter,
        "Tool": Tool,
        "Importer": Importer,
        "Device": Device,
        "Guesser": Guesser,
    })

manager.setPluginPlaces(utils.PLUGINPATH)

