from PyQt4 import QtGui, QtCore, uic
import sys, os, urllib
from elementtree.ElementTree import XML

# This gets the main catalog from smashwords.

url = 'http://www.smashwords.com/'

class Catalog(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)

        uifile = os.path.join(
            os.path.abspath(
                os.path.dirname(__file__)),'catalog.ui')
        uic.loadUi(uifile, self)
        self.addBranch(self.catalog, 0)

    def addBranch(self, parent, level):
        print 'Expanding level:', level
        if level == 0:
            # Categories
            data = urllib.urlopen("%s/%s/?output=xml"%(url,'category')).read()
            root_elem = XML(data)
            subnodes = root_elem.findall('subcategory')
            for node in subnodes:
                print node.find('name').text,node.attrib['id']
                i = QtGui.QTreeWidgetItem(parent, [node.find('name').text])
                i.__id = node.attrib['id']
                i.setChildIndicatorPolicy(i.ShowIndicator)
        elif level in [1,2]:
            # SubCategories
            data = urllib.urlopen("%s/%s/%s?output=xml"%(url,
                'category/view/',parent.__id)).read()
            print '-----------\n',data
            root_elem = XML(data)
            subnodes = root_elem.findall('subcategory')
            for node in subnodes:
                print node.find('name').text,node.attrib['id']
                i = QtGui.QTreeWidgetItem(parent, [node.find('name').text])
                i.__id = node.attrib['id']
                i.setChildIndicatorPolicy(i.ShowIndicator)
            if not subnodes:
                # Book list
                data = urllib.urlopen("%s/%s/%s?output=xml"%(url,
                    'books/category/',parent.__id)).read()
                print '-----------\n',data
                root_elem = XML(data)
                subnodes = root_elem.findall('book')
                for node in subnodes:
                    #from pudb import set_trace; set_trace()
                    i = QtGui.QTreeWidgetItem(parent, [node.find('{http://purl.org/dc/elements/1.1/}title').text])
                    i.__id = 'book-'+node.attrib['id']
                    i.setChildIndicatorPolicy(i.DontShowIndicator)
            

    def on_catalog_itemExpanded(self, item):
        level = 0
        i = item
        while i:
            level += 1
            i = i.parent()
        if item.childCount()==0:
            self.addBranch(item, level)

    def on_catalog_itemActivated(self, item, column):
        if item.__id.startswith('book-'):
            self.web.load(QtCore.QUrl('%s/%s/%s'%(url,'books/view',item.__id[5:])))
        
def main():
    app = QtGui.QApplication(sys.argv)
    window=Catalog()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

