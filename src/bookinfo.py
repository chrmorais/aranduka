from PySide import QtCore

class BookInfoWrapper(QtCore.QObject):
    def __init__(self, bookdata):
        QtCore.QObject.__init__(self)
        self._data = bookdata.entries[0]
        icon = "http://archive.org/favicon.ico"

    def _title(self):
        return self._data.get("title")

    def _cover(self):
        for l in self._data.links:
            if l.rel == u'http://opds-spec.org/image':
                return l.href

    def _subtitle(self):
        return self._data.get("subtitle")

    def _rights(self):
        return self._data.get("rights")

    @QtCore.Signal
    def changed(self): pass

    title = QtCore.Property(unicode, _title, notify=changed)
    cover = QtCore.Property(unicode, _cover, notify=changed)
    subtitle = QtCore.Property(unicode, _title, notify=changed)
    rights = QtCore.Property(unicode, _rights, notify=changed)


class ItemModel(QtCore.QAbstractListModel):
    COLUMNS=('item',)
    def __init__(self, items):
        QtCore.QAbstractListModel.__init__(self)
        self._items = items
        self.setRoleNames(dict(enumerate(ItemModel.COLUMNS)))
        
    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._items)
        
    def data(self, index, role):
        if index.isValid() and role == ItemModel.COLUMNS.index('item'):
            return self._items[index.row()]
        return None

    def setItems(self, items):
        self._items = items
        self.modelReset.emit()

class ItemWrapper(QtCore.QObject):
    def __init__(self, **data):
        QtCore.QObject.__init__(self)
        self._data = data

    def _icon(self):
        return self._data['icon']

    def _title(self):
        return self._data['title']

    def _subtitle(self):
        return self._data['subtitle']

    def _url(self):
        return self._data['url']

    @QtCore.Signal
    def changed(self): pass

    icon = QtCore.Property(unicode, _icon, notify=changed)
    title = QtCore.Property(unicode, _title, notify=changed)
    subtitle = QtCore.Property(unicode, _subtitle, notify=changed)
    url = QtCore.Property(unicode, _url, notify=changed)
