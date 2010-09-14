"""The user interface for our app"""

import os,sys
import models, importer

# Import Qt modules
from PyQt4 import QtCore, QtGui, uic
from progress import progress

class Main(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        uifile = os.path.join(
            os.path.abspath(
                os.path.dirname(__file__)),'main.ui')
        uic.loadUi(uifile, self)
        self.ui = self
        self.loadBooks()

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
