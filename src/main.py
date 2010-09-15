"""The user interface for our app"""

import os,sys
import models, importer

# Import Qt modules
from PyQt4 import QtCore, QtGui, uic
from progress import progress
from book_editor import BookEditor

class Main(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        uifile = os.path.join(
            os.path.abspath(
                os.path.dirname(__file__)),'main.ui')
        uic.loadUi(uifile, self)
        self.ui = self

        self._layout = QtGui.QVBoxLayout()
        self.details.setLayout(self._layout)
        self.book_editor = BookEditor(None)
        self.book_editor.back.clicked.connect(self.show_shelves)
        self._layout.addWidget(self.book_editor)
        self.loadBooks()
        print "Finished initializing main window"

    def on_books_itemActivated(self, item):
        self.book_editor.load_data(item.book.id)
        self.stack.setCurrentIndex(1)
        self.last_splitter_sizes=self.main_splitter.sizes()
        self.main_splitter.setSizes([0,self.main_splitter.size().width()])

    def show_shelves(self):
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
