from PyQt4 import QtCore, QtGui
from pluginmgr import Tool
import models
from templite import Templite

from bottle import route, run, response
import bottle
import os
bottle.debug = True

class Plugin(Tool):

    def action(self):
        self.action = QtGui.QAction("Publish Catalog", None)
        self.action.triggered.connect(self.publish)
        return self.action

    def publish(self):

        # FIXME: move to another process or something
        
        app = bottle.default_app() # or bottle.app() since 0.7
        app.catchall = False
        @route('/')
        def index():
            """Creates a OPDS catalog from the book database"""
            template = Templite(TPL)
            books = []

            for book in models.Book.query.order_by("title").all():
                epub_fn = None
                pdf_fn = None
                mobi_fn = None
                exts = book.available_formats()
                print "EXTS:", exts
                if '.epub' in exts:
                    epub_fn = "/book/%s.epub"%book.id
                if '.mobi' in exts:
                    epub_fn = "/book/%s.mobi"%book.id
                if '.pdf' in exts:
                    epub_fn = "/book/%s.pdf"%book.id

                books.append([
                    book.title,
                    book.id,
                    u','.join([a.name for a in book.authors]),
                    book.comments,
                    epub_fn,
                    pdf_fn,
                    mobi_fn,
                ])
            response.content_type='application/atom+xml'
            return template.render(books = books)

        @route('/cover/:id')
        def cover(id):
            """Returns the cover of a book"""
            book = models.Book.get_by(id=int(id))
            fname = book.cover()
            f = open(fname).read()
            response.content_type='image/jpeg'
            return (f)

        @route('/book/:name')
        def book(name):
            """Returns the book matching name in id and type"""

            mimetypes = {
                ".pdf": "application/pdf",
                ".epub": "application/epub+zip",
                ".mobi": "application/x-mobipocket-ebook",
            }

            id,extension=os.path.splitext(name)
            book = models.Book.get_by(id=id)
            files = book.files_for_format(extension)
            fname = files[0]
            f = open(fname).read()
            # FIXME: use correct content-types
            response.content_type=mimetypes[extension]
            return (f)


        run(host='localhost', port=8080)


TPL = r"""<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom"
      xmlns:dc="http://purl.org/dc/terms/"
      xmlns:opds="http://opds-spec.org/2010/catalog">
  <id>urn:uuid:433a5d6a-0b8c-4933-af65-4ca4f02763eb</id>

  <link rel="self"
        href="/"
        type="application/atom+xml;type=feed;profile=opds-catalog"/>

  <title>Aranduka Catalog</title>
  <updated>2010-01-10T10:01:11Z</updated>
  <author>
    <name>Aranduka</name>
    <uri>http://aranduka.googlecode.com</uri>
  </author>

${ for book in books: }$
  <entry>
    <title>${book[0]}$</title>
    <id>${book[1]}$</id>
    <updated>2010-01-10T10:01:11Z</updated>
    <author>
      <name>${book[2]}$</name>
    </author>
    <summary>${book[3]}$</summary>
    <link type="image/png"
          rel="http://opds-spec.org/cover"
          href="/cover/${book[1]}$"/>
    <link type="image/gif"
          rel="http://opds-spec.org/thumbnail"
          href="/cover/${book[1]}$"/>

    ${
        if book[4]:
            emit('<link type="application/epub+zip" rel="http://opds-spec.org/acquisition" href="%s"/>'%book[4])
        if book[5]:
            emit('<link type="application/pdf" rel="http://opds-spec.org/acquisition" href="%s"/>'%book[5])
        if book[6]:
            emit('<link type="application/x-mobipocket-ebook" rel="http://opds-spec.org/acquisition" href="%s"/>'%book[6])
    }$
 </entry>
${:end-for}$

</feed>
"""


