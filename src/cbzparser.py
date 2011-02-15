import os
import utils
import zipfile
from PyQt4 import QtGui

class CBZDocument(object):
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

