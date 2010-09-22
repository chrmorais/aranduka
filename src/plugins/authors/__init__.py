from PyQt4 import QtGui, QtCore
import sys, os
import models
from pluginmgr import ShelveView

# This plugin lists the books by author

EBOOK_EXTENSIONS=['epub','mobi','pdf']

class Catalog(ShelveView, QtCore.QObject):

    title = "Books By Author"

    def setWidget(self, widget):
        self.widget = widget

    @QtCore.pyqtSlot()
    def doSearch(self, *args):
        self.operate(search = unicode(self.widget.searchWidget.text.text()))

    def treeItem(self):
        """Returns a QTreeWidgetItem representing this
        plugin"""
        return QtGui.QTreeWidgetItem(["Authors"])

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
            authors = models.Author.query.order_by("name").filter(models.Author.name.like("%%%s%%"%search))
        else:
            authors = models.Author.query.order_by("name").all()
        
        for a in authors:
            a_item = QtGui.QListWidgetItem(a.name, self.shelf)
            for b in a.books:
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


    def showGrid(self, search = None):
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
        
        if search:
            authors = models.Author.query.order_by("name").filter(models.Author.name.like("%%%s%%"%search))
        else:
            authors = models.Author.query.order_by("name").all()
        for a in authors:
            # Make a shelf
            shelf_label = QtGui.QLabel(a.name)
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
            shelf.setMinimumWidth(153*len(a.books))
            shelf.setFlow(shelf.LeftToRight)
            shelf.setWrapping(False)
            shelf.setDragEnabled(False)
            shelf.setSelectionMode(shelf.NoSelection)

            # Hook the shelf context menu
            shelf.customContextMenuRequested.connect(self.shelfContextMenu)

            # Hook book editor
            shelf.itemActivated.connect(self.widget.on_books_itemActivated)
            
            # Fill the shelf
            for b in a.books:
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
