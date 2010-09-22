from PyQt4 import QtGui, QtCore
import sys, os
import models
from pluginmgr import ShelveView

# This gets the main catalog from feedbooks.

EBOOK_EXTENSIONS=['epub','mobi','pdf']

class Catalog(ShelveView):

    title = "Books By Author"

    def __init__(self):
        print "INIT: authors"
        self.widget = None

    def setWidget(self, widget):
        self.widget = widget

    def treeItem(self):
        """Returns a QTreeWidgetItem representing this
        plugin"""
        return QtGui.QTreeWidgetItem(["Authors"])

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
        
        for a in models.Author.query.order_by("name").all():
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
            shelf.setMinimumWidth(153*len(a.books))
            
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
