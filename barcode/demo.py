import os

p=os.popen('/usr/bin/zbarcam','r')
while True:
    code = p.readline()
    print 'Gor barcode:', code
    isbn = code.split(':')[1]
    os.system('chromium http://www.goodreads.com/search/search?q=%s'%isbn)