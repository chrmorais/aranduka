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
        for b in models.Book.query.order_by("title").all():
            icon = nocover
            cname = os.path.join("covers",str(b.id)+".jpg")
            if os.path.isfile(cname):
                try:
                    icon =  QtGui.QIcon(cname)
                except:
                    pass
            item = QtGui.QListWidgetItem(icon, b.title, self.widget.books)
            item.book = b
