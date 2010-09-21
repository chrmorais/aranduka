"""If a book is a feedbooks download, then this plugin will
"convert" the book to other formats by downloading them"""

from pluginmgr import Converter
import sys, os, urllib, urllib2
from models import File, session

SUPPORTED = ['epub','pdf','mobi']

def extract_id (book):
    """Returns the book's feedbooks ID or None"""
    for i in book.identifiers:
        if i.key == "FEEDBOOKS_ID":
            return i.value
    return None

class FBConverter(Converter):

    name = "FeedBooks"

    def __init__(self):
        print "INIT: feedbooks_converter"

    def can_convert(self, book):
        """Given a book object, return the list of formats to
        which it can be converted"""
        i = extract_id(book)
        if i:
            return SUPPORTED
        else:
            return []

    def convert(self, book, dest_format):
        """Convert that book to that destination format"""
        # Get the file
        book_id = extract_id(book)
        fname = os.path.abspath(os.path.join("ebooks", str(book.id) + '.' + dest_format))
        url="http://www.feedbooks.com/book/%s.%s"%(book_id, dest_format)

        try:
            print "Fetching: ", url
            u=urllib2.urlopen(url)
            data = u.read()
            u.close()
            f = open(fname,'wb')
            f.write(data)
            f.close()
        except urllib2.HTTPError:
            pass
        f = File(file_name = fname)
        book.files.append(f)
        session.commit()
        