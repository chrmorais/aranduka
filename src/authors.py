from PyQt4 import QtGui, QtCore
import sys, os
import models

# This gets the main catalog from feedbooks.

EBOOK_EXTENSIONS=['epub','mobi','pdf']

class Catalog(object):
    def __init__(self, widget):
        self.widget = widget

    def loadBooks(self):
        """Get all books from the DB and show them"""
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
