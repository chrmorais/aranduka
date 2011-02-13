from PyQt4 import QtGui, QtCore
import sys, os
import models
from pluginmgr import ShelfView

# This plugin lists the books by author

EBOOK_EXTENSIONS=['epub','mobi','pdf']

class Catalog(ShelfView):

    title = "Books By Author"
    itemText = "Authors"
    items = {}

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
                icon = QtGui.QIcon(QtGui.QPixmap(b.cover()).scaledToHeight(128, QtCore.Qt.SmoothTransformation))
                item = QtGui.QListWidgetItem(icon, b.title, self.shelf)
                item.book = b
                self.items[b.id] = item

        self.shelvesLayout.addStretch(1)
        self.widget.shelfStack.setWidget(self.shelf)

    def group_books(self, currentBook=None, search=None):
    
        grouped_books={}
        def add_book(b, k):
            if k in grouped_books:
                grouped_books[k].append(b)
            else:
                grouped_books[k]=[b]        
        if search:
            authors = models.Author.query.order_by("name").filter(models.Author.name.like("%%%s%%"%search))
        else:
            authors = models.Author.query.order_by("name").all()

        for a in authors:
            grouped_books[a.name] = [b for b in a.books]            
        return grouped_books
                
    def updateBook(self, book):
        # This may get called when no books
        # have been loaded in this view, so make it cheap
        if self.items and book.id in self.items:
            item = self.items[book.id]
            icon = QtGui.QIcon(QtGui.QPixmap(book.cover()).scaledToHeight(128, QtCore.Qt.SmoothTransformation))
            item.setText(book.title)
            item.setIcon(icon)
            item.book = book

