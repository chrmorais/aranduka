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
            if not a.name:
                initial = '@@'
                name = 'Unknown Author'
            else:
                initial = a.name[0]
                name = a.name
            grouped_books[u'%s: Books by: %s'%(initial,name)] = [b for b in a.books]
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

