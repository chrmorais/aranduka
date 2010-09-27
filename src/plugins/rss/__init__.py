from pluginmgr import BookStore
from PyQt4 import QtCore, QtGui, uic
import config
import os
from feedfinder import feeds as findFeed
import feedparser

class RSSWidget(QtGui.QWidget):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        uifile = os.path.join(
            os.path.abspath(
                os.path.dirname(__file__)),'store.ui')
        uic.loadUi(uifile, self)
        self.ui = self

        self.loadFeeds()

    def loadFeeds(self):
        self.feeds = config.getValue("RSSPlugin", "feeds", [])
        for title,url in self.feeds:
            i = QtGui.QListWidgetItem(title, self.feedList)
            self.feedList.addItem(i)

    def saveFeeds(self):
        config.setValue("RSSPlugin", "feeds", self.feeds)

    @QtCore.pyqtSlot()
    def on_add_clicked(self):
        t, ok = QtGui.QInputDialog.getText(self, "Aranduka - Add Feed", "Enter the URL of the feed or site:")
        if not ok:
            return
        t = unicode(t)
        print t
        # FIXME: make unblocking
        # FIXME: make the user choose a feed
        feeds = findFeed(unicode(t))
        print feeds
        feed = feeds[0]
        data = feedparser.parse(feed)
        self.feeds.append([data.feed.title, feed])
        self.saveFeeds()
        self.loadFeeds()

    @QtCore.pyqtSlot()
    def on_remove_clicked(self):
        pass

    @QtCore.pyqtSlot()
    def on_edit_clicked(self):
        pass
    
    @QtCore.pyqtSlot()
    def on_refresh_clicked(self):
        pass

class RSSStore(BookStore):
    """Fetch RSS feeds as ePub"""

    title = "RSS Feeds"
    itemText = "RSS Feeds"

    def __init__(self):
        print "INIT:", self.title
        self.widget = None
        self.w = None

    def treeItem(self):
        """Returns a QTreeWidgetItem representing this
        plugin"""
        return QtGui.QTreeWidgetItem([self.itemText])

    def setWidget (self, widget):
        self.widget = widget

    def operate(self):
        "Show the store"
        if not self.widget:
            print "Call setWidget first"
            return
        self.widget.title.setText(self.title)
        if not self.w:
            self.w = RSSWidget()
            self.pageNumber = self.widget.stack.addWidget(self.w)
        self.widget.stack.setCurrentIndex(self.pageNumber)

    showGrid = operate
    showList = operate


    @QtCore.pyqtSlot()
    def doSearch(self, *args):
        "No search here"
        pass
