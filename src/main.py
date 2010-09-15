"""The user interface for our app"""

import os,sys
import models, importer

# Import Qt modules
from PyQt4 import QtCore, QtGui, uic
from progress import progress
from book_editor import BookEditor

import feedbooks

class Main(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        uifile = os.path.join(
            os.path.abspath(
                os.path.dirname(__file__)),'main.ui')
        uic.loadUi(uifile, self)
        self.ui = self

        self.feedbooksStore = feedbooks.Catalog(self.stores)

        self._layout = QtGui.QVBoxLayout()
        self.details.setLayout(self._layout)
        self.book_editor = BookEditor(None)
        self.book_editor.back.clicked.connect(self.show_shelves)
        self._layout.addWidget(self.book_editor)
        self.loadBooks()
        print "Finished initializing main window"

    def on_stores_itemExpanded(self, item):
        item.handler.on_catalog_itemExpanded(item)

    def on_books_customContextMenuRequested(self, point):
        menu = QtGui.QMenu()
        menu.addAction(self.actionEdit_Book)
        menu.addAction(self.actionOpen_Book)
        menu.addAction(self.actionDelete_Book)
        menu.exec_(self.books.mapToGlobal(point))

    @QtCore.pyqtSlot()
    def on_actionOpen_Book_triggered(self):
        item = self.books.currentItem()
        if not item:
            return
        if item.book.files:
            url = QtCore.QUrl.fromLocalFile(item.book.files[0].file_name)
            print "Opening:", url
            QtGui.QDesktopServices.openUrl(url)

    def on_books_itemActivated(self, item):
        self.book_editor.load_data(item.book.id)
        self.stack.setCurrentIndex(1)
        self.last_splitter_sizes=self.main_splitter.sizes()
        self.main_splitter.setSizes([0,self.main_splitter.size().width()])

    def show_shelves(self):
        self.updateItem(self.books.currentItem())
        self.stack.setCurrentIndex(0)
        self.main_splitter.setSizes(self.last_splitter_sizes)

    @QtCore.pyqtSlot()
    def on_actionImport_Files_triggered(self):
        fname = unicode(QtGui.QFileDialog.getExistingDirectory(self, "Import Folder"))
        if not fname: return
        # Get a list of all files to be imported
        flist = []
        for data in os.walk(fname, followlinks = True):
            for f in data[2]:
                flist.append(os.path.join(data[0],f))
        for f in progress(flist, "Importing Files","Stop"):
            status = importer.import_file(f)
            print status
        # Reload books
        self.loadBooks()

    def loadBooks(self):
        """Get all books from the DB and show them"""
        nocover = QtGui.QIcon("nocover.png")
        self.books.clear()
        for b in models.Book.query.all():
            icon = nocover
            cname = os.path.join("covers",str(b.id)+".jpg")
            if os.path.isfile(cname):
                try:
                    icon =  QtGui.QIcon(cname)
                except:
                    pass
            item = QtGui.QListWidgetItem(icon, b.title, self.books)
            item.book = b
            
    def updateItem(self, item):
        """Updates one item with the data for its book"""

        # Make sure we are updated from the DB
        item.book = models.Book.get_by(id = item.book.id)
        cname = os.path.join("covers",str(item.book.id)+".jpg")
        item.setText(item.book.title)
        if os.path.isfile(cname):
            try:
                icon =  QtGui.QIcon(cname)
                item.setIcon(icon)
            except:
                pass
        

def main():
    # Init the database before doing anything else
    models.initDB()

    # Again, this is boilerplate, it's going to be the same on
    # almost every app you write
    app = QtGui.QApplication(sys.argv)
    window=Main()
    window.show()
    # It's exec_ because exec is a reserved word in Python
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
