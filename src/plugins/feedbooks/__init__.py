from feedparser import parse
from PySide import QtGui, QtCore, QtWebKit
import sys, os, urllib
from models import *
from pprint import pprint
from math import ceil
from pluginmgr import BookStore
from templite import Templite
import codecs
import urlparse
import time

# This gets the main catalog from feedbooks.

EBOOK_EXTENSIONS=['epub','mobi','pdf']


# FIXME: these classes should move to an accessible place for all plugins
class BookInfoWrapper(QtCore.QObject):
    def __init__(self, bookdata):
        QtCore.QObject.__init__(self)
        self._data = bookdata.entries[0]

    def _title(self):
        return self._data.get("title")

    def _subtitle(self):
        return self._data.get("subtitle")

    def _rights(self):
        return self._data.get("rights")

    @QtCore.Signal
    def changed(self): pass

    title = QtCore.Property(unicode, _title, notify=changed)
    subtitle = QtCore.Property(unicode, _title, notify=changed)
    rights = QtCore.Property(unicode, _rights, notify=changed)


class ItemModel(QtCore.QAbstractListModel):
    COLUMNS=('item',)
    def __init__(self, items):
        QtCore.QAbstractListModel.__init__(self)
        self._items = items
        self.setRoleNames(dict(enumerate(ItemModel.COLUMNS)))
        
    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._items)
        
    def data(self, index, role):
        if index.isValid() and role == ItemModel.COLUMNS.index('item'):
            return self._items[index.row()]
        return None

class ItemWrapper(QtCore.QObject):
    def __init__(self, **data):
        QtCore.QObject.__init__(self)
        self._data = data

    def _icon(self):
        return self._data['icon']

    def _title(self):
        return self._data['title']

    def _subtitle(self):
        return self._data['subtitle']

    def _url(self):
        return self._data['url']

    @QtCore.Signal
    def changed(self): pass

    icon = QtCore.Property(unicode, _icon, notify=changed)
    title = QtCore.Property(unicode, _title, notify=changed)
    subtitle = QtCore.Property(unicode, _subtitle, notify=changed)
    url = QtCore.Property(unicode, _url, notify=changed)


class Catalog(BookStore):

    title = "FeedBooks.com"
    url = 'http://www.feedbooks.com/catalog.atom'
    icon = 'http://www.feedbooks.com/favicon.ico'
    
    def __init__(self):
        BookStore.__init__(self)

    def search (self, terms):
        url = "http://www.feedbooks.com/search.atom?"+urllib.urlencode(dict(query=terms))
        self.crumbs=[self.crumbs[0],["Search: %s"%terms, url]]
        self.openUrl(QtCore.QUrl(url))

    def fixURL(self, url):
        if url.startswith('/'):
            url=urlparse.urljoin('http://feedbooks.com',url)
        return url

    @QtCore.Slot(unicode)
    def isDetailsURL(self, url):
        return url.split('/')[-1].split('.')[0].isdigit()

    @QtCore.Slot(unicode)
    def modelForURL(self, url):
        # FIXME: make unblocking

        url = unicode(url)
        # This happens for catalogs by language
        if url.startswith('/'):
            url=urlparse.urljoin('http://feedbooks.com',url)
        extension = url.split('.')[-1]
        print "Opening:",url

        if self.isDetailsURL(url):
            data = urllib2.urlopen(url).read()
            print "Parsing the details page:", url
            t1 = time.time()
            data = parse(data)
            print "Parsed branch in: %s seconds"%(time.time()-t1)
            return BookInfoWrapper(data)

        if extension in EBOOK_EXTENSIONS:
            # It's a book, get metadata, file and download
            book_id = url.split('/')[-1].split('.')[0]
            bookdata = parse("http://www.feedbooks.com/book/%s.atom"%book_id)
            if bookdata.status == 404:
                bookdata = parse("http://www.feedbooks.com/userbook/%s.atom"%book_id)

            bookdata = bookdata.entries[0]
            title = bookdata.title
            self.setStatusMessage.emit(u"Downloading: "+title)
            book = Book.get_by(title = title)
            if not book:
                # Let's create a lot of data
                tags = []
                for tag in bookdata.get('tags',[]):
                    t = Tag.get_by(name = tag.label)
                    if not t:
                        t = Tag(name = tag.label)
                    tags.append(t)
                ident = Identifier(key="FEEDBOOKS_ID", value=book_id)
                author = Author.get_by (name = bookdata.author)
                if not author:
                    author = Author(name = bookdata.author)
                book = Book (
                    title = title,
                    authors = [author],
                    tags = tags,
                    identifiers = [ident]
                )
            session.commit()

            # Get the file
            book.fetch_file(url, extension)
            book.fetch_cover("http://www.feedbooks.com/book/%s.jpg"%book_id)

        data = urllib2.urlopen(url).read()
        print "Parsing the branch:", url
        t1 = time.time()
        data = parse(data)
        print "Parsed branch in: %s seconds"%(time.time()-t1)
        title = data.feed.get('title','')
        #if 'page=' in url: # A page
            #print "DELETING LAST CRUMB" 
            #if 'page=' in self.crumbs[-1][1]: 
                ##last one was also a page
                #del self.crumbs[-1]
        #if title:
            #crumb = [title.split("|")[0].split("/")[-1].strip(), url]
            #try:
                #r=self.crumbs.index(crumb)
                #self.crumbs=self.crumbs[:r+1]
            #except ValueError:
                #self.crumbs.append(crumb)
        #self.showCrumbs()
        books = []
        links = []        
        for entry in data.entries:
            # Find acquisition links
            acq_links = [l.href for l in entry.links if l.rel=='http://opds-spec.org/acquisition']

            if acq_links: # Can be acquired
                books.append(entry)
            else:
                links.append(entry)

        totPages = int(ceil(float(data.feed.get('opensearch_totalresults', 1))/int(data.feed.get('opensearch_itemsperpage', 1))))
        curPage = int(urlparse.parse_qs(urlparse.urlparse(url).query).get('page',[1])[-1])
        
        t1 = time.time()

        
        #html = self.template.render(
            #title = title,
            #books = books,
            #links = links,
            #url = url,
            #totPages = totPages,
            #curPage = int(curPage)
            #)

        items = []
        for link in links:
            title = link.title
            subtitle = link.get('subtitle','')
            if '<' not in subtitle:
                    subtitle = subtitle.replace('\n','<p>')
            url = link.links[0].href
            if len(link.links) > 1:
                icon_url = link.links[1].href
            else:
                icon_url = 'ADDMISSING.jpg'            
            if url:
                items.append(ItemWrapper(icon=icon_url, title=title, subtitle=subtitle, url=self.fixURL(url)))
            
        for book in books:
            icon_url = ""
            title = book.title
            author = book.author
            acq_links = []
            non_acq_links = []
            subtitle = u'by '+ author
            for l in book.links:
                #Non-acquisition links
                print l.type
                if l.rel == "alternate" and l.type == "application/atom+xml;type=entry":
                    url = l.href
                if l.rel == "http://opds-spec.org/image/thumbnail":
                    icon_url = l.href
            #for l in book.links:
                ##acquisition links
                #if l.rel == "http://opds-spec.org/acquisition":
                    #acq_links.append('<a href="%s">%s</a>'%(l.href, l.href.split('.')[-1]))

            print icon_url
            print title
            if url:
                items.append(ItemWrapper(icon=icon_url, title=title, subtitle=subtitle, url=self.fixURL(url)))
        print "Rendered in: %s seconds"%(time.time()-t1)
        return ItemModel(items)


