import os, sys, time, re
from PyQt4 import QtCore, QtGui, uic

import models
from metadata import get_metadata
from pprint import pprint

VALID_EXTENSIONS = ['fb2','mobi','pdf','txt','lit','html','htm']

def clean_name (fname):
    "Clean a file name so it works better for a google query"
    fname = os.path.basename(fname)
    fname = fname.lower()
    fname = fname.replace('_',' ')
    fname = '.'.join(fname.split('.')[:-1])
    # FIXME: here we should use the system's encoding, but that's not
    # a sure thing to work, either.
    return fname.decode('latin1')

def import_file(fname):
    """Given a filename, tries to import it into
    the database with metadata from Google.

    Return value is as file_status
    """

    def try_import(fname, p):
        metadata=[]
        try:
            print "Fetching: ",p
            metadata = get_metadata(p) or []
            print "Candidates:", [d.title for d in metadata]
            time.sleep(2)
        except Exception, e:
            print e
        for data in metadata:
            # Does it look valid?
            if data.title.lower() in p:
                # FIXME: should check by other identifier?
                b = models.Book.get_by(title = data.title)
                if not b:
                    # TODO: add more metadata
                    b = models.Book(
                        title = data.title,
                    )
                print "Accepted: ", data.title
                f = models.File(file_name=fname, book=b)
                models.session.commit()
                return 1
        return 0

    print fname
    extension = fname.split('.')[-1].lower()
    if extension not in VALID_EXTENSIONS:
        print "Not an ebook"
        return 
    f = models.File.get_by(file_name = fname)
    if f:
        # Already imported
        return file_status(fname)
        
    # First try the clean name as-is
    p = clean_name(fname)
    r1 = try_import(fname, 'TITLE '+p)
    if r1:
        return r1

    # Try removing 'tags'
    p2 = re.sub('[\(\[].*[\)\]]',' ',p)
    r1 = try_import(fname, 'TITLE '+p2)
    if r1:
        return r1
    # Try separating pieces
    p3 = p2.replace('-',' - ')
    r1 = try_import(fname, 'TITLE '+p3)
    if r1:
        return r1
    
    #TODO Keep trying in other ways
    
    print 'Importing as-is'
    b = models.Book.get_by(title = p)
    f = models.File(file_name=fname, book=b)
    models.session.commit()
    return 2

def file_status(fname):
    """Given a full path, it checks if it has been imported into
    the library.

    It returns:

    0 -- it has not been imported
    1 -- it has been imported and metadata has been added
    2 -- it has been imported but metadata seems insufficient
    """
    f = models.File.get_by(file_name = fname.decode('latin1'))
    if not f:
        return 0
    # FIXME really check that metadata is insufficient
    elif not f.book or f.book.title == clean_name(fname) and not f.book.author:
        return 2
    return 1

class Main(QtGui.QDialog):
    """Main dialog"""
    def __init__(self, *args):
        QtGui.QDialog.__init__(self)

        # Cargamos la interfaz desde el archivo .ui
        uifile = os.path.join(
            os.path.abspath(
                os.path.dirname(__file__)),'importer.ui')
        uic.loadUi(uifile, self)

        # Get a list of all files to be imported
        flist = []
        for dname in sys.argv[1:]:
            for data in os.walk(dname, followlinks = True):
                for fname in data[2]:
                    flist.append(os.path.join(data[0],fname))

        for f in flist:
            extension = f.split('.')[-1].lower()
            if extension not in VALID_EXTENSIONS:
                continue
            item = QtGui.QListWidgetItem(os.path.basename(f))
            item.imported = False
            item.fullpath = f
            item.status = file_status(f)
            if item.status == 0:
                item.setBackground(QtGui.QColor("pink"))
            elif item.status == 1:
                item.setBackground(QtGui.QColor("lightgreen"))
            else:
                item.setBackground(QtGui.QColor("yellow"))
            self.files.addItem(item)
            
        self.files.sortItems()

    def on_start_clicked(self):
        for row in xrange(0, self.files.count()):
            item = self.files.item(row)
            if item.status == 0:
                item.status = import_file(item.fullpath)
                # FIXME DRY
                if item.status == 0:
                    item.setBackground(QtGui.QColor("pink"))
                elif item.status == 1:
                    item.setBackground(QtGui.QColor("lightgreen"))
                else:
                    item.setBackground(QtGui.QColor("yellow"))
            QtCore.QCoreApplication.instance().processEvents()

def main():
    if len(sys.argv) < 2:
        print "Usage: python importer.py path1 ... pathX\n\npathX can be a folder or file name."

    models.initDB()
    app = QtGui.QApplication(sys.argv)
    w = Main(sys.argv[1:])
    w.show()
    app.exec_()

if __name__ == "__main__":
    main()
