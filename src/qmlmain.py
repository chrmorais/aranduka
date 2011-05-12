# -*- coding: utf-8 -*-
import os
import sys
from PySide import QtCore
from PySide import QtGui
from PySide import QtDeclarative
from PySide import QtOpenGL
from PySide import QtUiTools

import models, config, ui
import rc_icons
from pluginmgr import manager, isPluginEnabled

import epubparser
import epubviewer
import network

class TocEntryWrapper(QtCore.QObject):
    def __init__(self, entry):
        QtCore.QObject.__init__(self)
        self._entry = entry

    def _title(self):
        return self._entry[0]

    def _fname(self):
        return self._entry[1]

    @QtCore.Signal
    def changed(self): pass

    title = QtCore.Property(unicode, _title, notify=changed)
    fname = QtCore.Property(unicode, _fname, notify=changed)


class ContentsModel(QtCore.QAbstractListModel):
    COLUMNS = ('entry',)
    def __init__(self, contents=[]):
        QtCore.QAbstractListModel.__init__(self)
        self.setContents(contents)
        self.setRoleNames(dict(enumerate(ContentsModel.COLUMNS)))

    def setContents(self, contents):
        self._contents = [TocEntryWrapper(x) for x in contents]
        self.modelReset.emit()

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._contents)

    def data(self, index, role):
        if index.isValid() and role == ContentsModel.COLUMNS.index('entry'):
            return self._contents[index.row()]
        return None


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

    def _icon(self):
        return self._bookstore.icon

    @QtCore.Signal
    def changed(self): pass

    name = QtCore.Property(unicode, _name, notify=changed)
    icon = QtCore.Property(unicode, _icon, notify=changed)


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

    def __init__(self):
        QtCore.QObject.__init__(self)
        self.view = QtDeclarative.QDeclarativeView()
        self.view.show()
        self.view.showFullScreen()

        #glw = QtOpenGL.QGLWidget()
        #self.view.setViewport(glw)
        self.fac = network.NMFactory()
        self.view.engine().setNetworkAccessManagerFactory(self.fac)
        self.view.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)

        # initialize plugins
        manager.locatePlugins()
        manager.loadPlugins()

        self.controller = self
        self.bookList = BookListModel()
        self.bookStoreList = BookStoreListModel()
        self.bookContents = ContentsModel([])

        rc = self.view.rootContext()
        rc.setContextProperty('controller', self.controller)
        rc.setContextProperty('bookList', self.bookList)
        rc.setContextProperty('bookStoreList', self.bookStoreList)
        rc.setContextProperty('bookContents', self.bookContents)
        js = """
            var b = document.getElementsByTagName("body")[0];
            b.style.backgroundColor = "#000";
            b.style.color = "#ccc";
            b.style.margin = "40px";
        """
        
        rc.setContextProperty('fixColors', "")

        self.view.setSource(__file__.replace('.py', '.qml'))


    @QtCore.Slot(QtCore.QObject)
    def bookSelected(self, wrapper):
        self.view.rootObject().setProperty("state", "Contents")
        # TODO: display the book & contents
        self._doc = epubparser.EpubDocument(wrapper._book.files_for_format('.epub')[0])
        self.bookContents.setContents(self._doc.tocentries)
        self.view.engine().networkAccessManager()._w = self._doc
        self.gotoChapter(self.bookContents._contents[0].fname)

    @QtCore.Slot(unicode)
    def gotoChapter(self, fname):
        self.view.rootObject().setProperty("state", "Text")
        self.view.rootObject().setHTML('<body style="background-color: #000;">HHHHH')
        self.view.rootObject().setURL('http://epub.epub/'+fname)

    @QtCore.Slot(BookStoreWrapper)
    def openStore(self, store):
        self._store = store
        self.fac._store = store
        self.view.rootObject().setBookStoreModel(store._bookstore.modelForURL(store._bookstore.url))
        
    @QtCore.Slot(unicode)
    def openStoreURL(self, url):
        if self._store._bookstore.isDetailsURL(url):
            self.view.rootObject().setBookDetailsModel(self._store._bookstore.modelForURL(url))
        else:
            self.view.rootObject().setBookStoreModel(self._store._bookstore.modelForURL(url))


def main():
    # Init the database before doing anything else
    models.initDB()

    # Again, this is boilerplate, it's going to be the same on
    # almost every app you write
    app = QtGui.QApplication(sys.argv)
    window=Controller()
    # It's exec_ because exec is a reserved word in Python
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
