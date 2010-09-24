from pluginmgr import BookStore
from PyQt4 import QtCore, QtGui, uic
import config
import os

class RSSWidget(QtGui.QWidget):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        uifile = os.path.join(
            os.path.abspath(
                os.path.dirname(__file__)),'store.ui')
        uic.loadUi(uifile, self)
        self.ui = self

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
