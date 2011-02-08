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

# This gets the main catalog from ManyBooks.net.

EBOOK_EXTENSIONS=['epub','mobi','pdf']

class Catalog(BookStore):

    title = "ManyBooks.net: Free and Public Domain Books"
    itemText = "ManyBooks.net"
    
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
            self.openUrl(QtCore.QUrl('http://manybooks.net/opds/'))
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
        url = "http://manybooks.net/opds/search.php?"+urllib.urlencode(dict(q=terms))
        self.crumbs=[self.crumbs[0],["Search: %s"%terms, url]]
        self.openUrl(QtCore.QUrl(url))

    def openUrl(self, url):
        if isinstance(url, QtCore.QUrl):
            url = url.toString()
        url = unicode(url)
        extension = url.split('.')[-1]
        if extension in EBOOK_EXTENSIONS:
            # It's a book, get metadata, file and download
            # Metadata is cached
            title = self.title_cache[url]
            _author = self.author_cache[url]
            book_id = self.id_cache[url]
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
            fname = os.path.abspath(os.path.join("ebooks", str(book.id) + '.' + extension))
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
        # Disable updates to prevent flickering
        self.w.store_web.setUpdatesEnabled(False)
        self.w.store_web.page().mainFrame().load(QtCore.QUrl(url))
        self.setStatusMessage.emit(u"Loading: "+url)
        self.w.store_web.page().loadFinished.connect(self.parseBranch)
        return
        
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
        print "Parsed branch in: %s seconds"%(time.time()-t1)
        title = data.feed.get('title','')
        html = ["<h1>%s</h1>"%title]
        if url.split('/')[-1].isdigit(): # It's a pageNumber
            pn = int(url.split('/')[-1])+1
            crumb = [data.feed.title.split("books",1)[-1]+"[%d]"%pn, url]
        else:
            crumb = [data.feed.title.split("-")[-1].strip(), url]
        try:
            r=self.crumbs.index(crumb)
            self.crumbs=self.crumbs[:r+1]
        except ValueError:
            self.crumbs.append(crumb)
        self.showCrumbs()

        self.cover_cache={}
        self.id_cache={}
        self.author_cache={}
        
        for entry in data.entries:
            pass
            # iurl = entry.links[0].href
            # if entry.links[0].type == u'application/atom+xml':
                # # A category
                # item = """
                # <dd>
                    # <a href="%s">%s</a>: %s
                # </dd>
                # """%(
                    # iurl,
                    # entry.title,
                    # entry.get('subtitle',''),
                    # )
            # else: # A book
                # cover_url = [l.href for l in entry.links if l.rel==u'http://opds-spec.org/cover']
                # if cover_url:
                    # cover_url = cover_url[0]
                # else:
                    # cover_url = 'broken.jpeg'
                # # Find acquisition links
                # acq_links = []
                # for l in entry.links:
                    # if l.rel==u'http://opds-spec.org/acquisition':
                        # acq_links.append(l.href)
                        # self.cover_cache[l.href]=cover_url
                        # self.id_cache[l.href]=entry.get('id')
                        # self.author_cache[l.href]=entry.author
                        # self.title_cache[l.href]=entry.title
                # acq_fragment = []
                # for l in acq_links:
                    # acq_fragment.append('<a href="%s">%s</a>'%(l, l.split('.')[-1]))
                # acq_fragment='&nbsp;|&nbsp;'.join(acq_fragment)

                # if acq_fragment:
                    # # A book entry

                    # item = """
                    # <table><tr>
                        # <td style="height: 80px; width: 80px;">
                        # <img src=%s style="height: 64px;">
                        # <td>
                            # %s</br>
                            # Download: %s
                    # </table>
                    # """%(
                        # cover_url,
                        # entry.title,
                        # acq_fragment,
                        # )

                # else:
                    # # A search result
                    # item = """
                    # <table><tr>
                        # <td>
                            # <a href="%s">%s</a></br>
                            # By: %s
                    # </table>
                    # """%(
                        # entry.links[0].href,
                        # entry.title,
                        # entry.author,
                        # )

            # html.append(item)

        # # Maybe it's paginated
        # # If it has previous
        # html.append('<div>')
        # for l in data.feed.links:
            # if l.rel == u'previous':
                # html.append('<a href="%s">Previous Page</a>'%l.href)
        # for l in data.feed.links:
            # if l.rel == u'next':
                # html.append('<a href="%s">Next Page</a>'%l.href)
        # html.append('</div>')
            
        # html='\n'.join(html)
        t1 = time.time()
        html = self.template.render(
            title = title,
            books = books,
            links = links,
            url = url,
            totPages = totPages,
            curPage = int(curPage)
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
