from feedparser import parse
from PyQt4 import QtGui, QtCore, uic
import sys, os

# This gets the main catalog from feedbooks.

class Catalog(QtGui.QTreeWidgetItem):
    def __init__(self, *args):
        QtGui.QTreeWidgetItem.__init__(self, *args)
        self.handler = self
        self.setText(0, "FeedBooks")
        self.addBranch(self, 'http://www.feedbooks.com/catalog.atom')

    def addBranch(self, parent, url):
        data = parse(url)
        for entry in data.entries:
            i = QtGui.QTreeWidgetItem(parent, [entry.title])
            i.handler = self
            i.url = entry.links[0].href
            if i.url.split('/')[-1].isdigit():
                # It's a book
                i.setChildIndicatorPolicy(i.DontShowIndicator)
            else:
                # It's a catalog
                i.setChildIndicatorPolicy(i.ShowIndicator)

    def on_catalog_itemExpanded(self, item):
        if item.childCount()==0:
            self.addBranch(item, item.url)

    def on_catalog_itemActivated(self, item, column):
        url=item.url
        if url.split('/')[-1].isdigit():
            # It's a book
            self.web.load(QtCore.QUrl(url))