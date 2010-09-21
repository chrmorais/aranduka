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
        self.widget.stack.setCurrentIndex(0)
        nocover = QtGui.QIcon("nocover.png")
        self.widget.books.clear()
        for b in models.Book.query.order_by("title").all():
            icon = nocover
            cname = os.path.join("covers",str(b.id)+".jpg")
            if os.path.isfile(cname):
                try:
                    icon =  QtGui.QIcon(QtGui.QPixmap(cname).scaledToHeight(128, QtCore.Qt.SmoothTransformation))
                except:
                    pass
            item = QtGui.QListWidgetItem(icon, b.title, self.widget.books)
            item.book = b
