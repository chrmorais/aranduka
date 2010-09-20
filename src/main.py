"""The user interface for our app"""

import os,sys
import models, importer

# Import Qt modules
from PyQt4 import QtCore, QtGui, uic
from progress import progress
from book_editor import BookEditor

import feedbooks
import titles

class Main(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        uifile = os.path.join(
            os.path.abspath(
                os.path.dirname(__file__)),'main.ui')
        uic.loadUi(uifile, self)
        self.ui = self
        self.last_splitter_sizes = None
        self.store_handler = None

        item = QtGui.QTreeWidgetItem(["Titles"])
        item.is_shelves = True
        item.handler = titles.Catalog
        self.treeWidget.addTopLevelItem(item)
        self.on_treeWidget_itemClicked(item)
        self.shelves_handler.loadBooks()

        item = QtGui.QTreeWidgetItem(["Feedbooks"])
        item.is_store = True
        item.handler = feedbooks.Catalog
        self.treeWidget.addTopLevelItem(item)

        self._layout = QtGui.QVBoxLayout()
        self.details.setLayout(self._layout)
        self.book_editor = BookEditor(None)
        self.book_editor.back.clicked.connect(self.show_shelves)
        self._layout.addWidget(self.book_editor)
        self.back_from_store.clicked.connect(self.show_shelves_from_store)
        print "Finished initializing main window"

    def on_treeWidget_itemClicked(self, item):
        if hasattr(item, 'is_store'):
            self.stack.setCurrentIndex(2)
            self.store_handler=item.handler(self)
        elif hasattr(item, 'is_shelves'):
            self.stack.setCurrentIndex(0)
            self.shelves_handler=item.handler(self)

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
        if self.store_handler:
            del(self.store_handler)
            self.store_handler = None
        self.updateItem(self.books.currentItem())
        self.stack.setCurrentIndex(0)
        if self.last_splitter_sizes:
            self.main_splitter.setSizes(self.last_splitter_sizes)

    def show_shelves_from_store(self):
        self.shelves_handler.loadBooks()
        self.show_shelves()


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
        self.shelves_handler.loadBooks()

    @QtCore.pyqtSlot()
    def on_actionImport_File_triggered(self):
        fname = unicode(QtGui.QFileDialog.getOpenFileName(self, "Import File"))
        if not fname: return
        status = importer.import_file(fname)
        self.shelves_handler.loadBooks()
            
    def updateItem(self, item):
        """Updates one item with the data for its book"""

        # Make sure we are updated from the DB
	if not item:
	    return
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
