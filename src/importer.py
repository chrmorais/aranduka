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

def main():
    if len(sys.argv) < 2:
        print "Usage: python importer.py path1 ... pathn\n\npathX can be a folder or file name."

    for p in sys.argv[1:]:
        p = clean_name(p)
        # First try the clean name as-is
        print p
        data = get_metadata('TITLE ' + p)
        if data:
            pprint(data)
        else:
            #TODO Keep trying in other ways
            print 'No data'

if __name__ == "__main__":
    main()
