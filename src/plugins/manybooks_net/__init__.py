from feedparser import parse
from PyQt4 import QtGui, QtCore, QtWebKit, uic
import sys, os, urllib
from models import *
from pprint import pprint
from math import ceil
from pluginmgr import BookStore

# This gets the main catalog from ManyBooks.net.

EBOOK_EXTENSIONS=['epub','mobi','pdf']

class Catalog(BookStore):

    title = "ManyBooks.net: Free and Public Domain Books"
    
    def __init__(self):
        print "INIT: ManyBooks.net"
        self.widget = None
        self.w = None
        self.cover_cache={}
        self.author_cache={}
        self.id_cache={}
        self.title_cache={}
        
    def setWidget (self, widget):
        self.widget = widget

    def treeItem(self):
        """Returns a QTreeWidgetItem representing this
        plugin"""
        return QtGui.QTreeWidgetItem(["ManyBooks.net"])

    def operate(self):
        "Show the store"
        if not self.widget:
            print "Call setWidget first"
            return
        self.widget.title.setText(self.title)
        if not self.w:
            uifile = os.path.join(
                os.path.abspath(
                    os.path.dirname(__file__)),'feedbooks_store.ui')
            self.w = uic.loadUi(uifile)
            self.pageNumber = self.widget.stack.addWidget(self.w)
            self.crumbs=[]
            self.openUrl(QtCore.QUrl('http://manybooks.net/opds/'))
            self.w.store_web.page().setLinkDelegationPolicy(QtWebKit.QWebPage.DelegateExternalLinks)
            self.w.store_web.page().linkClicked.connect(self.openUrl)
            self.w.crumbs.linkActivated.connect(self.openUrl)
            
        self.widget.stack.setCurrentIndex(self.pageNumber)
        
    showGrid = operate
    showList = operate

    @QtCore.pyqtSlot()
    def doSearch(self, *args):
        self.search(unicode(self.widget.searchWidget.text.text()))
        
    def search (self, terms):
        url = "http://manybooks.net/opds/search.php?"+urllib.urlencode(dict(q=terms))
        self.crumbs=[self.crumbs[0],["Search: %s"%terms, url]]
        self.openUrl(QtCore.QUrl(url))

    def openUrl(self, url):
        print "CRUMBS:", self.crumbs
        if isinstance(url, QtCore.QUrl):
            url = url.toString()
        url = unicode(url)
        extension = url.split('.')[-1]
        print "Opening:",url
        if extension in EBOOK_EXTENSIONS:
            # It's a book, get metadata, file and download
            # Metadata is cached
            title = self.title_cache[url]
            _author = self.author_cache[url]
            book_id = self.id_cache[url]
            book = Book.get_by(title = title)
            if not book:
                ident = Identifier(key="ManyBooks.net_ID", value=book_id)
                author = Author.get_by (name = _author)
                if not author:
                    author = Author(name = _author)
                book = Book (
                    title = title,
                    authors = [author],
                    identifiers = [ident],
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
        print "Showing:", url
        data = parse(url)
        html = ["<h1>%s</h1>"%data.feed.title]
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
            iurl = entry.links[0].href
            if entry.links[0].type == u'application/atom+xml':
                # A category
                item = """
                <dd>
                    <a href="%s">%s</a>: %s
                </dd>
                """%(
                    iurl,
                    entry.title,
                    entry.get('subtitle',''),
                    )
            else: # A book
                cover_url = [l.href for l in entry.links if l.rel==u'http://opds-spec.org/cover']
                if cover_url:
                    cover_url = cover_url[0]
                else:
                    cover_url = 'broken.jpeg'
                # Find acquisition links
                acq_links = []
                for l in entry.links:
                    if l.rel==u'http://opds-spec.org/acquisition':
                        acq_links.append(l.href)
                        self.cover_cache[l.href]=cover_url
                        self.id_cache[l.href]=entry.get('id')
                        self.author_cache[l.href]=entry.author
                        self.title_cache[l.href]=entry.title
                        print entry.title, entry.author
                acq_fragment = []
                for l in acq_links:
                    acq_fragment.append('<a href="%s">%s</a>'%(l, l.split('.')[-1]))
                acq_fragment='&nbsp;|&nbsp;'.join(acq_fragment)

                if acq_fragment:
                    # A book entry

                    item = """
                    <table><tr>
                        <td style="height: 80px; width: 80px;">
                        <img src=%s style="height: 64px;">
                        <td>
                            %s</br>
                            Download: %s
                    </table>
                    """%(
                        cover_url,
                        entry.title,
                        acq_fragment,
                        )

                else:
                    # A search result
                    item = """
                    <table><tr>
                        <td>
                            <a href="%s">%s</a></br>
                            By: %s
                    </table>
                    """%(
                        entry.links[0].href,
                        entry.title,
                        entry.author,
                        )

            html.append(item)

        # Maybe it's paginated
        # If it has previous
        html.append('<div>')
        for l in data.feed.links:
            if l.rel == u'previous':
                html.append('<a href="%s">Previous Page</a>'%l.href)
        for l in data.feed.links:
            if l.rel == u'next':
                html.append('<a href="%s">Next Page</a>'%l.href)
        html.append('</div>')
            
        html='\n'.join(html)
        self.w.store_web.setHtml(html)

    def on_catalog_itemExpanded(self, item):
        if item.childCount()==0:
            self.addBranch(item, item.url)

    def on_catalog_itemActivated(self, item, column):
        url=item.url
        if url.split('/')[-1].isdigit():
            # It's a book
            self.web.load(QtCore.QUrl(url))
