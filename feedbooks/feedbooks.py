from feedparser import parse
from PyQt4 import QtGui, QtCore, uic
import sys, os

# This gets the main catalog from feedbooks.

class Catalog(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)

        uifile = os.path.join(
            os.path.abspath(
                os.path.dirname(__file__)),'catalog.ui')
        uic.loadUi(uifile, self)
        self.addBranch(self.catalog, 'http://www.feedbooks.com/catalog.atom')

    def addBranch(self, parent, url):
        data = parse(url)
        for entry in data.entries:
            i = QtGui.QTreeWidgetItem(parent, [entry.title])
            i.url = entry.links[0].href
            #self.catalog.addTopLevelItem(i)

    def on_catalog_itemActivated(self, item, column):
        url=getattr(item,'url',None)
        if url:
            self.addBranch(item, url)
        
def main():
    app = QtGui.QApplication(sys.argv)
    window=Catalog()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

