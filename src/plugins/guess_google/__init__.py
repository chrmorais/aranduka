import os, sys, urllib2

from gdata.books.service import BookService
from PyQt4 import QtCore, QtGui, uic

import models
from utils import validate_ISBN, SCRIPTPATH
from metadata import get_metadata

from pluginmgr import Guesser

class GoogleGuesser(Guesser):
    name = "Google Books"

    def can_guess(self, book):
        return True

    def guess(self, book):
        self.book = book
        dlg = GuessDialog(self.book)
        r = dlg.exec_()
        if not r == dlg.Accepted:
            return None
        if dlg.currentMD:
            return dlg.currentMD
        return None

service = BookService()

class GuessDialog(QtGui.QDialog):
    def __init__(self, book, *args):
        QtGui.QDialog.__init__(self,*args)
        uifile = os.path.join(
            os.path.abspath(
                os.path.dirname(__file__)),'guess.ui')
        uic.loadUi(uifile, self)
        self.ui = self
        self._query = None

        self.md=[]
        self.currentMD=None
        self.book = book
        self.title.setText("Title: %s"%book.title)
        self.author.setText("Author: %s"%(u', '.join([a.name for a in book.authors])))
        ident = models.Identifier.get_by(key='ISBN',book=book)
        if ident:
            self.isbn.setText('ISBN: %s'%ident.value)
            self._isbn=ident.value
        else:
            self.isbn.hide()

    def on_bookList_currentRowChanged(self, row):
        self.currentMD=self.md[row]
        print "Selected: ",unicode(self.bookList.item(row).text())

    @QtCore.pyqtSlot()
    def on_guess_clicked(self):
        # Try to guess based on the reliable data
        q=''
        self.bookList.clear()
        if self.title.isChecked():
            q+='TITLE %s '%self.book.title
        if self.author.isChecked():
            q+='AUTHOR %s '%u', '.join([a.name for a in self.book.authors])
        if self.isbn.isChecked():
            q+='ISBN %s'%self._isbn
        self._query = q
        if self._query:
            self.md = get_metadata(self._query) or []
        for candidate in self.md:
            authors = ', '.join(candidate.authors)
            self.bookList.addItem("%s by %s"%(candidate.title, authors))
