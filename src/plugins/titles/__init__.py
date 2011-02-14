from PyQt4 import QtGui, QtCore
import sys, os
import models
from pluginmgr import ShelfView
from functools import partial

# This plugin lists the books by title

class Catalog(ShelfView):

    title = "Books By Title"
    itemText = "Titles"
    items = {}
    

    def group_books(self, currentBook=None, search=None):
        # Group books by initial (FIXME: make the DB do it)
        grouped_books={}
        # FIXME: use a defaultdict
        def add_book(b, k):
            if k in grouped_books:
                grouped_books[k].append(b)
            else:
                grouped_books[k]=[b]
        
        if search:
            books = models.Book.query.filter(models.Book.title.like("%%%s%%"%search))
        else:
            books = models.Book.query.order_by("title").all()
            
        for b in books:
            initial = b.title[0].upper()
            if initial.isdigit():
                add_book(b,'#: Titles Starting with Numbers')
            elif initial.isalpha():
                add_book(b,'%s: Titles Starting with %s'%(initial,initial))
            else:
                add_book(b,'@: Titles Starting with Symbols')
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
