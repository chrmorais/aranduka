from feedparser import parse
from PyQt4 import QtGui, QtCore, QtWebKit, uic
import sys, os, urllib
from models import *
from pprint import pprint
from math import ceil
from pluginmgr import BookStore
import codecs
import time
from templite import Templite
import urlparse

# This gets the main catalog from arXiv.

EBOOK_EXTENSIONS=['epub','mobi','pdf']

class Catalog(BookStore):

    title = "arXiv.org"
    itemText = "arXiv.org"
    
    def __init__(self):
        print "INIT: ManyBooks.net"
        BookStore.__init__(self)
        self.widget = None
        self.w = None
        self.cover_cache={}
        self.author_cache={}
        self.id_cache={}
        self.title_cache={}
        
    def setWidget (self, widget):
        tplfile = os.path.join(
            os.path.abspath(
                os.path.dirname(__file__)),'category.tmpl')

        tplfile = codecs.open(tplfile,'r','utf-8')
        self.template = Templite(tplfile.read())
        tplfile.close()
        self.widget = widget

    def operate(self):
        "Show the store"
        if not self.widget:
            print "Call setWidget first"
            return
        self.widget.title.setText(self.title)
        if not self.w:
            uifile = os.path.join(
                os.path.abspath(
                    os.path.dirname(__file__)),'store.ui')
            self.w = uic.loadUi(uifile)
            self.pageNumber = self.widget.stack.addWidget(self.w)
            self.crumbs=[]
            self.openUrl(QtCore.QUrl('http://arxiv-opds.heroku.com/catalog.atom'))
            self.w.store_web.page().setLinkDelegationPolicy(QtWebKit.QWebPage.DelegateExternalLinks)
            self.w.store_web.page().linkClicked.connect(self.openUrl)
            self.w.crumbs.linkActivated.connect(self.openUrl)
            self.w.store_web.loadStarted.connect(self.loadStarted)
            self.w.store_web.loadProgress.connect(self.loadProgress)
            self.w.store_web.loadFinished.connect(self.loadFinished)
           
        self.widget.stack.setCurrentIndex(self.pageNumber)
        
    showGrid = operate
    showList = operate
        
    def search (self, terms):
        url = "http://arxiv-opds.heroku.com/search.php?"+urllib.urlencode(dict(q=terms))
        self.crumbs=[self.crumbs[0],["Search: %s"%terms, url]]
        self.openUrl(QtCore.QUrl(url))

    def openUrl(self, url):
        print "openURL:", url
        if isinstance(url, QtCore.QUrl):
            url = url.toString()
        url = unicode(url)
        if not url.startswith('http'):
            url=urlparse.urljoin('http://arxiv-opds.heroku.com/',url)        
        extension = url.split('.')[-1]
        if extension in EBOOK_EXTENSIONS:
            # It's a book, get metadata, file and download
            # Metadata is cached
            title = self.title_cache[url]
            _author = self.author_cache[url]
            book_id = self.id_cache[url]
            self.setStatusMessage.emit(u"Downloading: "+title)
            book = Book.get_by(title = title)
            book_tid = url.split('/')[-2]
            if not book:
                ident_urn = Identifier(key="ManyBooks.net_ID", value=book_id)
                ident_tid = Identifier(key="ManyBooks.net_TID", value=book_tid)
                author = Author.get_by (name = _author)
                if not author:
                    author = Author(name = _author)
                book = Book (
                    title = title,
                    authors = [author],
                    identifiers = [ident_urn, ident_tid],
                )
            session.commit()
            
            # Get the file
            book.fetch_file(url, extension)
            cover_url = self.cover_cache.get(url,None)
            if cover_url:
                book.fetch_cover(cover_url)
            
        else:
            self.showBranch(url)

    def showCrumbs(self):
        ctext = []
        for c in self.crumbs[-4:]:
            ctext.append('<a href="%s">%s</a>'%(c[1],c[0]))
        ctext = "&nbsp;>&nbsp;".join(ctext)
        self.w.crumbs.setText(ctext)

    def showBranch(self, url):
        """Trigger download of the branch, then trigger
        parseBranch when it's downloaded"""
        print "Showing:", url
        self.w.store_web.page().mainFrame().load(QtCore.QUrl(url))
        if '.atom' in url:
            # Disable updates to prevent flickering
            self.w.store_web.setUpdatesEnabled(False)
            self.setStatusMessage.emit(u"Loading: "+url)
            self.w.store_web.page().loadFinished.connect(self.parseBranch)
        
    @QtCore.pyqtSlot()
    def parseBranch(self):
        """Replaces the content of the web page (which is assumed to be
        an Atom feed from ManyBooks) with the generated HTML.        
        """
        self.w.store_web.page().loadFinished.disconnect(self.parseBranch)
        url = unicode(self.w.store_web.page().mainFrame().requestedUrl().toString())
        print "Parsing the branch:", url
        t1 = time.time()
        data = parse(unicode(self.w.store_web.page().mainFrame().toHtml()).encode('utf-8'))
        
        nextPage = ''
        prevPage = ''
        for l in data.feed.get('links',[]):
            print "LINK:", l
            if l.rel == 'next':
                nextPage = '<a href="%s">Next Page</a>'%l.href
            elif l.rel == 'prev':
                prevPage = '<a href="%s">Previous Page</a>'%l.href
        
        title = data.feed.get('title',data.feed.get('subtitle','###'))
        if '?n=' in url: # It's paginated
            pnum = int(url.split('=')[-1])/10+1
            title = title+'(%s)'%pnum
            if '?n=' in self.crumbs[-1][1]:
                # Don't show two numbered pages in a row
                del(self.crumbs[-1])
            
        crumb = [title, url]
        if crumb in self.crumbs:
            self.crumbs = self.crumbs[:self.crumbs.index(crumb)+1]
        else:
            self.crumbs.append(crumb)
        self.showCrumbs()

        self.cover_cache={}
        self.id_cache={}
        self.author_cache={}
        
        books = []
        links = []        
        for entry in data.entries:
            # Find acquisition links
            acq_links = [l.href for l in entry.get('links',[]) if l.rel in['http://opds-spec.org/acquisition',"http://opds-spec.org/acquisition/open-access"]]

            if acq_links:
                # A book
                cover_url = [l.href for l in entry.links if l.rel==u'http://opds-spec.org/cover']
                if cover_url:
                    cover_url = cover_url[0]
                books.append(entry)
                for href in acq_links:
                    self.cover_cache[href]=cover_url
                    self.id_cache[href]=entry.get('id')
                    self.author_cache[href]=entry.author
                    self.title_cache[href]=entry.title
            else:
                # A category
                links.append(entry)
                
        t1 = time.time()
        html = self.template.render(
            title = title,
            books = books,
            links = links,
            url = url,
            nextPage = nextPage,
            prevPage = prevPage
            )
        print "Rendered in: %s seconds"%(time.time()-t1)
        # open('x.html','w+').write(html)        
        self.w.store_web.setHtml(html)
        self.w.store_web.setUpdatesEnabled(True)

    def on_catalog_itemExpanded(self, item):
        if item.childCount()==0:
            self.addBranch(item, item.url)

    def on_catalog_itemActivated(self, item, column):
        url=item.url
        if url.split('/')[-1].isdigit():
            # It's a book
            self.web.load(QtCore.QUrl(url))
