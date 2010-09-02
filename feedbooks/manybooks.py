from feedparser import parse
from PyQt4 import QtGui, QtCore, uic
import sys, os

# This gets the main catalog from manybooks.

class Catalog(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)

        uifile = os.path.join(
            os.path.abspath(
                os.path.dirname(__file__)),'catalog.ui')
        uic.loadUi(uifile, self)
        self.addBranch(self.catalog, 'http://manybooks.net/opds/')

    def addBranch(self, parent, url):
        data = parse(url)
        print data
        print '--------------'
        for entry in data.entries:
            i = QtGui.QTreeWidgetItem(parent, [entry.title])
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
        
def main():
    app = QtGui.QApplication(sys.argv)
    window=Catalog()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

