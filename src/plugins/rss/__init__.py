from pluginmgr import BookStore
from PyQt4 import QtCore, QtGui, uic
import config

class RSSStore(BookStore):
    """Fetch RSS feeds as ePub"""

    title = "RSS Feeds"
    itemText = "RSS Feeds"

    def __init__(self):
        print "INIT:", self.title
        self.widget = None

    def treeItem(self):
        """Returns a QTreeWidgetItem representing this
        plugin"""
        return QtGui.QTreeWidgetItem([self.itemText])

    def setWidget (self, widget):
        self.widget = widget

    @QtCore.pyqtSlot()
    def doSearch(self, *args):
        "No search here"
        pass
