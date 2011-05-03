# -*- coding: utf-8 -*-
import os
import sys
from PySide import QtCore
from PySide import QtGui
from PySide import QtDeclarative
from PySide import QtOpenGL

import models
from pluginmgr import manager, isPluginEnabled

models.initDB()

import epubparser
import epubviewer


class BookWrapper(QtCore.QObject):
    def __init__(self, book):
        QtCore.QObject.__init__(self)
        self._book = book

    def _title(self):
        return self._book.title

    def _cover(self):
        return self._book.cover()

    def _author(self):
        return ', '.join(unicode(a.name) for a in self._book.authors)
    
    @QtCore.Signal
    def changed(self): pass

    title = QtCore.Property(unicode, _title, notify=changed)
    cover = QtCore.Property(unicode, _cover, notify=changed)
    author = QtCore.Property(unicode, _author, notify=changed)


class BookListModel(QtCore.QAbstractListModel):
    COLUMNS = ('book',)
    def __init__(self):
        QtCore.QAbstractListModel.__init__(self)
        self._books = [BookWrapper(x) for x in models.Book.query.all()]
        self.setRoleNames(dict(enumerate(BookListModel.COLUMNS)))
    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._books)
    def data(self, index, role):
        if index.isValid() and role == BookListModel.COLUMNS.index('book'):
            return self._books[index.row()]
        return None


class BookStoreWrapper(QtCore.QObject):
    def __init__(self, bookstore):
        QtCore.QObject.__init__(self)
        self._bookstore = bookstore

    def _name(self):
        return self._bookstore.title

    @QtCore.Signal
    def changed(self): pass

    name = QtCore.Property(unicode, _name, notify=changed)


class BookStoreListModel(QtCore.QAbstractListModel):
    COLUMNS = ('store',)
    
    def __init__(self):
        QtCore.QAbstractListModel.__init__(self)
        self._bookstores = [BookStoreWrapper(x.plugin_object) for x in manager.getPluginsOfCategory("BookStore")]
        self.setRoleNames(dict(enumerate(BookStoreListModel.COLUMNS)))
        
    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._bookstores)
        
    def data(self, index, role):
        if index.isValid() and role == BookStoreListModel.COLUMNS.index('store'):
            return self._bookstores[index.row()]
        return None
        

class Controller(QtCore.QObject):
    @QtCore.Slot(QtCore.QObject)
    def bookSelected(self, wrapper):
        global view, episodeList
        view.rootObject().setProperty("state", "Contents")
        # TODO: display the book & contents
        self._doc = epubviewer.EPubWrapper(wrapper._book.files_for_format('.epub')[0])
        self._contentModel = self._doc.model()
        view.rootObject().setContents(self._contentModel)
        view.engine().networkAccessManager()._w = self._doc

    @QtCore.Slot(unicode)
    def gotoChapter(self, fname):
        view.rootObject().setProperty("state", "Text")
        view.rootObject().setURL('http://epub.epub/'+fname)

    @QtCore.Slot(BookStoreWrapper)
    def openStore(self, store):
        self._store = store
        view.rootObject().setBookStoreModel(store._bookstore.modelForURL(store._bookstore.url))
        view.rootObject().setProperty("state", "Bookstore2")

    @QtCore.Slot(unicode)
    def openStoreURL(self, url):
        model = self._store._bookstore.modelForURL(url)
        if model:
            view.rootObject().setBookStoreModel(model)
        else:
            view.rootObject().setBookStorePage(url)
            view.rootObject().setProperty("state", "Bookstore3")


app = QtGui.QApplication(sys.argv)
view = QtDeclarative.QDeclarativeView()
#glw = QtOpenGL.QGLWidget()
#view.setViewport(glw)
view.engine().setNetworkAccessManagerFactory(epubviewer.NMFactory())
view.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)

# initialize plugins
manager.locatePlugins()
manager.loadPlugins()

controller = Controller()
bookList = BookListModel()
bookStoreList = BookStoreListModel()

rc = view.rootContext()
rc.setContextProperty('controller', controller)
rc.setContextProperty('bookList', bookList)
rc.setContextProperty('bookStoreList', bookStoreList)

view.setSource(__file__.replace('.py', '.qml'))
view.show()
app.exec_()

