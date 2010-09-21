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
        self.widget.stack.setCurrentIndex(0)
        self.widget.title.setText(self.title)
        nocover = QtGui.QIcon("nocover.png")
        self.widget.books.clear()
        for a in models.Author.query.order_by("name").all():
            for b in a.books:
                icon = nocover
                cname = os.path.join("covers",str(b.id)+".jpg")
                if os.path.isfile(cname):
                    try:
                        icon =  QtGui.QIcon(QtGui.QPixmap(cname).scaledToHeight(128, QtCore.Qt.SmoothTransformation))
                    except:
                        pass
                item = QtGui.QListWidgetItem(icon, b.title, self.widget.books)
                item.book = b
