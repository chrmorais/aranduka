from PyQt4 import QtGui, QtCore
import sys, os
import models
from pluginmgr import ShelveView

# This gets the main catalog from feedbooks.

EBOOK_EXTENSIONS=['epub','mobi','pdf']

class Catalog(ShelveView):

    title = "Books By Title"
    
    def __init__(self):
        print "INIT: titles"
        self.widget = None

    def treeItem(self):
        """Returns a QTreeWidgetItem representing this
        plugin"""
        return QtGui.QTreeWidgetItem(["Titles"])

    def setWidget(self, widget):
        self.widget = widget

    def operate(self):
        """Get all books from the DB and show them"""

        if not self.widget:
            print "Call setWidget first"
            return
        
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
        
        for b in models.Book.query.order_by("title").all():
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
            shelf = QtGui.QListWidget()
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
