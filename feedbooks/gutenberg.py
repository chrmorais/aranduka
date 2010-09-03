from feedparser import parse
from PyQt4 import QtGui, QtCore, uic
import sys, os, pprint

# This gets the main catalog from the gutenberg project.

class Catalog(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)

        uifile = os.path.join(
            os.path.abspath(
                os.path.dirname(__file__)),'catalog.ui')
        uic.loadUi(uifile, self)
        self.addBranch(self.catalog, 'http://www.gutenberg.org/catalog.opds/search')

    def addBranch(self, parent, url):
        data = parse(url)
        print pprint.pprint(data)
        print '--------------'
        for entry in data.entries:
            book = False
            for l in entry.links:
                if l.rel == u'http://opds-spec.org/acquisition':
                    book = True
            i = QtGui.QTreeWidgetItem(parent, [entry.title])
            i.url = entry.links[0].href
            if book:
                # It's a book
                i.setChildIndicatorPolicy(i.DontShowIndicator)
                i.__entry = entry
            else:
                # It's a catalog
                i.setChildIndicatorPolicy(i.ShowIndicator)
                i.__entry = None

    def on_catalog_itemExpanded(self, item):
        if item.childCount()==0:
            self.addBranch(item, item.url)

    def on_catalog_itemActivated(self, item, column):
        if item.__entry:
            # It's a book
            self.web.setHtml("""
            <h1>%s</h1>
            %s
            """%(item.__entry.title,
            item.__entry.subtitle,
            ))
        else:
            self.web.setHtml("")
        
def main():
    app = QtGui.QApplication(sys.argv)
    window=Catalog()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

