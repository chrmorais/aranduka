from PyQt4 import QtGui, QtCore
import sys, os
import models
from pluginmgr import ShelveView
from functools import partial

# This plugin lists the books by title

EBOOK_EXTENSIONS=['epub','mobi','pdf']

class Catalog(ShelveView, QtCore.QObject):

    title = "Books By Title"
    
    def treeItem(self):
        """Returns a QTreeWidgetItem representing this
        plugin"""
        return QtGui.QTreeWidgetItem(["Titles"])

    def setWidget(self, widget):
        self.widget = widget

    @QtCore.pyqtSlot()
    def doSearch(self, *args):
        self.operate(search = unicode(self.widget.searchWidget.text.text()))

    def showList(self, search = None):
        """Get all books from the DB and show them"""

        if not self.widget:
            print "Call setWidget first"
            return
        self.operate = self.showList
        css = '''
        ::item {
                padding: 0;
                margin: 0;
                height: 48;
            }
        '''

        self.widget.title.setText(self.title)
        nocover = QtGui.QIcon("nocover.png")
        # Setup widgetry
        self.widget.stack.setCurrentIndex(0)
        self.shelf = QtGui.QListWidget()
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

        # Fill the shelf
        if search:
            books = models.Book.query.filter(models.Book.title.like("%%%s%%"%search))
        else:
            books = models.Book.query.order_by("title").all()
        
        for b in books:
            icon = nocover
            cname = os.path.join("covers",str(b.id)+".jpg")
            if os.path.isfile(cname):
                try:
                    icon =  QtGui.QIcon(QtGui.QPixmap(cname).scaledToHeight(128, QtCore.Qt.SmoothTransformation))
                except:
                    pass
            item = QtGui.QListWidgetItem(icon, b.title, self.shelf)
            item.book = b

        self.widget.shelveStack.setWidget(self.shelf)


    def showGrid(self, search=None):
        """Get all books from the DB and show them"""

        if not self.widget:
            print "Call setWidget first"
            return
        self.operate = self.showGrid
        
        self.widget.title.setText(self.title)
        nocover = QtGui.QIcon("nocover.png")
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


        # Group books by initial (FIXME: make the DB do it)
        grouped_books={}
        def add_book(b, k):
            if k in grouped_books:
                grouped_books[k].append(b)
            else:
                grouped_books[k]=[b]
        
        # Fill the shelf
        if search:
            books = models.Book.query.filter(models.Book.title.like("%%%s%%"%search))
        else:
            books = models.Book.query.order_by("title").all()
            
        for b in books:
            initial = b.title[0].upper()
            if initial.isdigit():
                add_book(b,'#')
            elif initial.isalpha():
                add_book(b,initial)
            else:
                add_book(b,'@')
        keys = grouped_books.keys()
        keys.sort()
        for k in keys:
            # Make a shelf
            shelf_label = QtGui.QLabel("Books starting with: %s"%k)
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
                icon = nocover
                cname = os.path.join("covers",str(b.id)+".jpg")
                if os.path.isfile(cname):
                    try:
                        icon =  QtGui.QIcon(QtGui.QPixmap(cname).scaledToHeight(128, QtCore.Qt.SmoothTransformation))
                    except:
                        pass
                item = QtGui.QListWidgetItem(icon, b.title, shelf)
                item.book = b


        self.widget.shelveStack.setWidget(self.shelves)

    def shelfContextMenu(self, point):
        shelf = self.sender()
        item = shelf.currentItem()
        book = item.book
        point = shelf.mapToGlobal(point)
        self.widget.bookContextMenuRequested(book, point)
        
