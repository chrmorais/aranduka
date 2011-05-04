from PySide import QtNetwork, QtCore, QtGui, QtDeclarative
import os, sys
from epubparser import EpubDocument
import epubparser
import feedparser
import ui
from config import *
import hashlib

class ContentsModel(QtCore.QAbstractListModel):
    COLUMNS = ('title','fname')
    def __init__(self, contents):
        QtCore.QAbstractListModel.__init__(self)
        self._contents = contents
        self.setRoleNames(dict(enumerate(ContentsModel.COLUMNS)))

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._contents)

    def data(self, index, role):
        if index.isValid() and role == ContentsModel.COLUMNS.index('title'):
            return self._contents[index.row()][0]
        elif index.isValid() and role == ContentsModel.COLUMNS.index('fname'):
            return self._contents[index.row()][1]
        return None

class EPubWrapper(QtCore.QObject):
    def __init__(self, epubfile):
        QtCore.QObject.__init__(self)
        self._doc = epubparser.EpubDocument(epubfile)

    def model(self):
        return ContentsModel(self._doc.tocentries)


        

