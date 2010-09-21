"""If a book is a feedbooks download, then this plugin will
"convert" the book to other formats by downloading them"""

from pluginmgr import Converter

class Catalog(BookStore):

    def __init__(self):
        print "INIT: feedbooks_converter"
