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

    def accessManager(self):
        self.fac = NMFactory()
        return self.fac

        

class NMFactory(QtDeclarative.QDeclarativeNetworkAccessManagerFactory):

    def __init__(self,*args):
        QtDeclarative.QDeclarativeNetworkAccessManagerFactory.__init__(self, *args)

    def create(self, *args):
        self.new_manager = NetworkAccessManager()
        return self.new_manager

class NetworkAccessManager(QtNetwork.QNetworkAccessManager):

    def __init__(self):
        self._w = None
        QtNetwork.QNetworkAccessManager.__init__(self)

    def createRequest(self, operation, request, data):
        if request.url().host() != "epub.epub":
            return QtNetwork.QNetworkAccessManager.createRequest(self, operation, request, data)

        if operation == self.GetOperation:
            reply = DownloadReply(self, request.url(), self.GetOperation, self._w)
            return reply
        else:
            return QtNetwork.QNetworkAccessManager.createRequest(self, operation, request, data)


class DownloadReply(QtNetwork.QNetworkReply):

    def __init__(self, parent, url, operation, w):
        self._w = w
        QtNetwork.QNetworkReply.__init__(self, parent)
        self.content = self._w._doc.getData(unicode(url.path())[1:])
        self.open(self.ReadOnly | self.Unbuffered)
        self.setUrl(url)
        QtCore.QTimer.singleShot(0, self.readyRead.emit)
        QtCore.QTimer.singleShot(1, self.finished.emit)
        
    def __getattribute__(self,name):
        return QtNetwork.QNetworkReply.__getattribute__(self,name)

    def abort(self):
        pass

    def bytesAvailable(self):
        return len(self.content) + QtCore.QIODevice.bytesAvailable(self)

    def disconnectNotify(self, *args):
        QtNetwork.QNetworkReply.disconnectNotify(self, *args)

    def readData(self, size):
        size = min(size, len(self.content))
        data, self.content = self.content[:size], self.content[size:]
        return data
