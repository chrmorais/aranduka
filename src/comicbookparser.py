import os
import utils
import zipfile
import UnRAR2
from PyQt4 import QtGui


class CBDocument(object):
    """A class that parses and provides
    data about a ComicBooks files"""

    def __init__(self, fname):
    
        print "Opening:", fname
        if fname.lower().endswith('cbz'):
            self.format = 'cbz'
            try:
                print "Trying to open the Zip (CBZ) file."
                self.book = zipfile.ZipFile(fname, "r")
            except zipfile.BadZipfile, e:
                raise ValueError("Invalid format")

            self.tocentries = self.book.namelist()

        elif fname.lower().endswith('cbr'):
            self.format = 'cbr'
            try:
                print "Trying to open the RAR (CBR) file."
                self.book = UnRAR2.RarFile(fname)
            except UnRAR2.rar_exceptions.InvalidRARArchive, e:
                raise ValueError("Invalid format")

            self.tocentries = [info.filename for info in self.book.infoiter() if not info.isdir]

        else:
            print "DEBUG: Oops! We can recognise that file format."

        self.tocentries.sort()
            
    def getData(self, path):
        """Return the contents of a file in the document"""

        print "GetData:", path

        if self.format == 'cbz':
            try:
                f = self.book.open(path)
            except KeyError: #File missing in the zip
                return []
            data = f.read()
            f.close()
            return data

        elif self.format == 'cbr':
            try:
                # This is a hack, because when we have files in dirs
                # pyunrar2 doesn't return the data correctly.
                filename = os.path.split(path)[1]
                return self.book.read_files('*' + filename)[0][1]

            except UnRAR2.rar_exceptions.FileOpenError: #File missing in the rar
                return []

        else:
            return []
        
    def fetchCover(self, basename=""):
        # find first image. there are folders inside some files
        for entry in self.tocentries:
            if(self.isImage(entry)):
                if self.format == 'cbz':
                    image = self.book.read(entry)
                if self.format == 'cbr':
                    print "Using", entry, "as cover."
                    filename = os.path.split(entry)[1]
                    image = self.book.read_files('*' + filename)[0][1]
                break

        # this is taken from the fetch_cover method on models
        oname = os.path.join(utils.COVERPATH, str(basename) +".jpg")
        imageqt = QtGui.QImage.fromData(image)
        coverqt = imageqt.scaled(128,128, 1, 1)
        coverqt.save(oname)
        
    def isImage(self, name):
        list = name.split(".")
        extension = list[-1].lower()
        if extension == "jpg" or extension == "png":
            return True
        else:
            return False 

class CBRDocument(object):
    """A class that parses and provides
    data about a CBZ file"""

    def __init__(self, fname):
    
        print "Opening:", fname
        try:
            self.book = zipfile.ZipFile(fname, "r")
        except zipfile.BadZipfile, e:
            raise ValueError("Invalid format")
            
        self.tocentries = self.book.namelist()
        self.tocentries.sort()

    def getData(self, path):
        """Return the contents of a file in the document"""

        print "GD:", path
        try:
            f = self.book.open(path)
        except KeyError: #File missing in the zip
            return []
        data = f.read()
        f.close()
        return data
        
    def fetchCover(self, basename=""):
        # find first image. there are folders inside some files
        for entry in self.tocentries:
            if(self.isImage(entry)):
                #self.book.extract(entry)
                image = self.book.read(entry)
                break

        # this is taken from the fetch_cover method on models
        oname = os.path.join(utils.COVERPATH, str(basename) +".jpg")
        imageqt = QtGui.QImage.fromData(image)
        coverqt = imageqt.scaled(128,128, 1, 1)
        coverqt.save(oname)
        
    def isImage(self, name):
        list = name.split(".")
        extension = list[-1].lower()
        if extension == "jpg" or extension == "png":
            return True
        else:
            return False 

