# -*- coding: utf-8 -*-
"""
Alibris Book Guesser

This plugin allows you to search for a book's information
using Alibris' API 

More information about the API:
http://developer.alibris.com/docs
"""
import os
import sys
import urllib2
import json
import models

from PyQt4 import QtCore, QtGui, uic
from utils import validate_ISBN, SCRIPTPATH
from urllib import urlencode
from pluginmgr import Guesser
# Base URL for Alibris' Search Method
__baseurl__ = 'http://api.alibris.com/v1/public/search?'

# Alibris API Key
__apikey__ = '9q3rk555cg4aqttx6tyehwuk'

class AlibrisGuesser(Guesser):
    name = "Alibris"

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

class _Book (object):
    """Dummy object used to pass the data
       to the book_editor"""
    title = None
    author = None
    identifiers = []

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
        book = _Book()
        book.title = self.md['book'][row]['title']
        book.authors = [self.md['book'][row]['author']] # FIXME: check how to split this
        book.identifiers = [('ISBN', self.md['book'][row]['isbn'])]
        self.currentMD = book
        print "Selected: ",unicode(self.bookList.item(row).text())

    def _get_url (self, query):
        url = __baseurl__
        url += 'outputtype=json&'
        url += urlencode(query)
        url += '&apikey=%s' % __apikey__
        return url

    def search (self, query):
        """Implements Alibris' Search Method to retrieve the
           information of a book.

           More info on this method:
           http://developer.alibris.com/docs/read/Search_Method

           JSON Response example:
           http://developer.alibris.com/files/json-freakonomics.txt.
        """
        data = urllib2.urlopen(self._get_url(query)).read()
        return json.loads(data)

    @QtCore.pyqtSlot()
    def on_guess_clicked(self):
        # Try to guess based on the reliable data
        q = []
        self.bookList.clear()
        if self.title.isChecked():
            q.append(('qtit', self.book.title))
        if self.author.isChecked():
            q.append(('qauth', u', '.join([a.name for a in self.book.authors])))
        if self.isbn.isChecked():
            q['qisbn'] = self._isbn
            q.append(('qisbn', self._isbn))
        self._query = q
        if self._query:
            self.md = self.search(self._query)
        if 'status' in self.md \
            and self.md['status'] == '0': 
            if 'book' in self.md:
                for candidate in self.md['book']:
                    self.bookList.addItem("%s by %s" % \
                                          (candidate['title'], \
                                           candidate['author']))
            else:
                print "No matches found for the selected criteria"
                QtGui.QMessageBox.information(self, \
                                              u'No results', \
                                              u'No results found matching your criteria')
        else:
            print "Failed to load data from Alibris"
            QtGui.QMessageBox.warning(self, \
                                      u'Failed to load data', \
                                      u'Failed to load data from Alibris')
