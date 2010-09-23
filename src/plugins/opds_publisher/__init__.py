from PyQt4 import QtCore, QtGui
from pluginmgr import Tool
import models
from templite import Templite
import processing

from bottle import route, run, response
import bottle
bottle.debug = True

class Plugin(Tool):

    def action(self):
        self.action = QtGui.QAction("Publish Catalog", None)
        self.action.triggered.connect(self.publish)
        print self.opds()
        return self.action




TPL = """
<?xml version="1.0" encoding="UTF-8"?>
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
      <uri>http://opds-spec.org/authors/1285</uri>
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

    

if __name__ == "__main__":
    models.initDB()
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
            for f in book.files:
                if f.file_name.endswith('.epub'):
                    epub_fn = "/book/%s.epub"%book.id
                elif f.file_name.endswith('.pdf'):
                    epub_fn = "/book/%s.pdf"%book.id
                elif f.file_name.endswith('.mobi'):
                    epub_fn = "/book/%s.mobi"%book.id

            books.append([
                book.title,
                book.id,
                u','.join([a.name for a in book.authors]),
                book.comments,
                epub_fn,
                pdf_fn,
                mobi_fn,
            ])
        return template.render(books = books)

    @route('/cover/:id')
    def cover(id):
        """Returns the cover of a book"""
        fname = '../../covers/%s.jpg'%id
        f = open(fname).read()
        response.content_type='image/jpeg'
        return (f)

    @route('/book/:name')
    def book(name):
        """Returns the book matching name in id and type"""
        id,extension=name.split('.')
        book = models.Book.get_by(id=id)
        for f in book.files:
            if f.file_name.endswith(extension):
                f = open(f.file_name).read()
                response.content_type='application/octet-string'
                return (f)


    run(host='localhost', port=8080)
