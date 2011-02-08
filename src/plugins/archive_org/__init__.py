from feedparser import parse
from PyQt4 import QtGui, QtCore, QtWebKit, uic
import sys, os, urllib
from models import *
from pprint import pprint
from math import ceil
from pluginmgr import BookStore
try:
    from elementtree.ElementTree import XML
except:
    from xml.etree.ElementTree import XML

# This gets the main catalog from Archive.org.

EBOOK_EXTENSIONS=['epub','mobi','pdf']

class Catalog(BookStore):

    title = "Archive.org: Free and Public Domain Books"
    itemText = "Archive.org"
    
    def __init__(self):
        BookStore.__init__(self)
        self.w = None
        self.cover_cache={}

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
            self.openUrl(QtCore.QUrl('http://bookserver.archive.org/catalog/'))
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
        url = "http://bookserver.archive.org/catalog/opensearch?"+urllib.urlencode(dict(q=terms))
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
            meta_url = url[:-len(extension)-1]+'_meta.xml'
            data = urllib.urlopen(meta_url).read()
            root_elem = XML(data)
            title = root_elem.find('title').text
            authors = root_elem.findall('creator')
            book_id = root_elem.find('identifier').text
            tags = root_elem.find('subject')
            if tags:
                tags = tags.text.split(';')
            else:
                tags = []
            self.setStatusMessage.emit(u"Downloading: "+title)
            book = Book.get_by(title = title)
            if not book:
                _tags = []
                # FIXME: it doesn't work. No idea why.
                #for tag in tags:
                    #t = Tag.get_by(name = "subject", value = tag.strip())
                    #if not t:
                        #t = Tag(name = "subject", value = tag.strip())
                    #_tags.append(t)
                    #print _tags
                ident = Identifier(key="Archive.org_ID", value=book_id)
                a_list = []
                for a in authors:
                    name = a.text or ""
                    if not name:
                        continue
                    author = Author.get_by (name = name)
                    if not author:
                        author = Author(name = name)
                        a_list.append(author)
                book = Book (
                    title = title,
                    authors = a_list,
                    identifiers = [ident],
                    tags = _tags,
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
                cover_url = [l.href for l in entry.links if l.rel==u'http://opds-spec.org/image'][0]
                # Find acquisition links
                acq_links = []
                for l in entry.links:
                    if l.rel==u'http://opds-spec.org/acquisition':
                        acq_links.append(l.href)
                        self.cover_cache[l.href]=cover_url
                acq_fragment = []
                for l in acq_links:
                    acq_fragment.append('<a href="%s">%s</a>'%(l, l.split('.')[-1]))
                acq_fragment='&nbsp;|&nbsp;'.join(acq_fragment)

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
