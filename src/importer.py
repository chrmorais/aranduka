import os, sys

from create_schema import createDataBase
import models
from metadata import get_metadata
from pprint import pprint

def clean_name (fname):
    "Clean a file name so it works better for a google query"
    fname = os.path.basename(fname)
    fname = fname.lower()
    fname = fname.replace('_',' ')
    fname = '.'.join(fname.split('.')[:-1])
    return fname

def import_file(fname):
    """Given a filename, tries to import it into
    the database with metadata from Google"""
    
    p = clean_name(fname)
    # First try the clean name as-is
    print p
    data = get_metadata('TITLE ' + p)
    if data:
        b = models.Book(
            title = data.title,
        )
        f = models.File(file_name=fname, book=b)
        models.session.commit()
    else:
        #TODO Keep trying in other ways
        print 'No data'

def import_folder(dname):
    """Given a folder, imports all files recursively"""
    
    for data in os.walk(dname, followlinks = True):
        for fname in data[2]:
            fullpath = os.path.join(data[0],fname)
            import_file(fullpath)

def main():
    if len(sys.argv) < 2:
        print "Usage: python importer.py path1 ... pathX\n\npathX can be a folder or file name."

    createDataBase()

    for p in sys.argv[1:]:
        if os.path.isfile(p):
            import_file(p)
        elif os.path.isdir(p):
            import_folder(p)

if __name__ == "__main__":
    main()
