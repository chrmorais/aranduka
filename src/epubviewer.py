from PyQt4 import QtNetwork, QtCore, QtGui, uic
import os, sys
import zipfile
from elementtree.ElementTree import XML



class Main(QtGui.QMainWindow):
    def __init__(self, fname):
        QtGui.QMainWindow.__init__(self)

        uifile = os.path.join(
            os.path.abspath(
                os.path.dirname(__file__)),'epubviewer.ui')
        uic.loadUi(uifile, self)
        self.ui = self

        # This is done according to this:
        # http://stackoverflow.com/questions/1388467/reading-epub-format

        print "Opening:", fname
        self.book = zipfile.ZipFile(fname, "r")
        f = self.book.open('META-INF/container.xml')
        self.container = XML(f.read())
        f.close()
        roots = self.container.findall('.//{urn:oasis:names:tc:opendocument:xmlns:container}rootfile')
        self.roots = []
        for r in roots:
            self.roots.append(r.attrib['full-path'])
        opf = self.book.open(self.roots[0])
        self.basepath = os.path.dirname(self.roots[0])+"/"
        if self.basepath == '/':
            self.basepath=""
            
        data = opf.read()
        self.opf=XML(data)
        opf.close()
        self.manifest = self.opf.find('{http://www.idpf.org/2007/opf}manifest')
        self.manifest_dict = {}
        for elem in self.manifest.findall('{http://www.idpf.org/2007/opf}item'):
            self.manifest_dict[elem.attrib['id']]=self.basepath+elem.attrib['href']

        self.spine = self.opf.find('{http://www.idpf.org/2007/opf}spine')

        self.toc_id = self.spine.attrib['toc']
        self.toc_fn = self.manifest_dict[self.toc_id]
        f = self.book.open(self.toc_fn)
        data = f.read()
        self.toc = XML(data)
        self.navmap = self.toc.find('{http://www.daisy.org/z3986/2005/ncx/}navMap')
        # FIXME: support nested navpoints
        self.navpoints = self.navmap.findall('.//{http://www.daisy.org/z3986/2005/ncx/}navPoint')
        self.tocentries = []
        for np in self.navpoints:
            label = np.find('{http://www.daisy.org/z3986/2005/ncx/}navLabel').find('{http://www.daisy.org/z3986/2005/ncx/}text').text
            content = np.find('{http://www.daisy.org/z3986/2005/ncx/}content').attrib['src']
            if label and content:
                self.tocentries.append([label, content])

        for l,c in self.tocentries:
            item = QtGui.QListWidgetItem(l)
            item.contents = c
            self.chapters.addItem(item)

        self.itemrefs = self.spine.findall('{http://www.idpf.org/2007/opf}itemref')
        self.spinerefs = [
                self.manifest_dict[item.attrib['idref']] for item in self.itemrefs
            ]
        print self.spinerefs
            
        self.old_manager = self.view.page().networkAccessManager()
        self.new_manager = NetworkAccessManager(self.old_manager, self)
        self.view.page().setNetworkAccessManager(self.new_manager)

        self.openPath(self.spinerefs[0])
        
    def on_chapters_itemClicked(self, item):
        self.openPath(item.contents)

    def getData(self, path):
        path = "%s%s"%(self.basepath,path)
        f = self.book.open(path)
        data = f.read()
        f.close()
        return data

    def openPath(self, path, fragment=None):
        print "Opening:", path
        if "#" in path:
            path, fragment = path.split('#',1)
        xml = self.getData(path)
        self.view.page().mainFrame().setHtml(xml,QtCore.QUrl("epub://book/"))
        if fragment:
            pass
            # FIXME: figure out how to jump to the anchor

    def linkClicked(self, url):
        if url.isRelative(): #They all should be
            frag = unicode(url.fragment())
            path = unicode(url.path())
            self.openPath(path, frag)

    def unsupported(self, *args):
        print "UNSUP:", args

class DownloadReply(QtNetwork.QNetworkReply):

    def __init__(self, parent, url, operation, w):
        self._w = w
        print"DR:", url, url.path()
        QtNetwork.QNetworkReply.__init__(self, parent)
        self.content = self._w.getData(unicode(url.path())[1:])
        self.offset = 0

        self.setHeader(QtNetwork.QNetworkRequest.ContentTypeHeader, QtCore.QVariant("application/binary"))
        self.setHeader(QtNetwork.QNetworkRequest.ContentLengthHeader, QtCore.QVariant(len(self.content)))
        QtCore.QTimer.singleShot(0, self, QtCore.SIGNAL("readyRead()"))
        QtCore.QTimer.singleShot(0, self, QtCore.SIGNAL("finished()"))
        self.open(self.ReadOnly | self.Unbuffered)
        self.setUrl(url)

    def abort(self):
        pass

    def bytesAvailable(self):
        return len(self.content) - self.offset

    def isSequential(self):
        return True

    def readData(self, maxSize):
        print "readData"
        if self.offset < len(self.content):
            end = min(self.offset + maxSize, len(self.content))
            data = self.content[self.offset:end]
            self.offset = end
            return data

class NetworkAccessManager(QtNetwork.QNetworkAccessManager):

    def __init__(self, old_manager, w):
        self._w = w
        QtNetwork.QNetworkAccessManager.__init__(self)
        self.old_manager = old_manager
        self.setCache(old_manager.cache())
        self.setCookieJar(old_manager.cookieJar())
        self.setProxy(old_manager.proxy())
        self.setProxyFactory(old_manager.proxyFactory())

    def createRequest(self, operation, request, data):

        if request.url().scheme() != "epub":
            return QNetworkAccessManager.createRequest(self, operation, request, data)

        if operation == self.GetOperation:
            # Handle download:// URLs separately by creating custom
            # QNetworkReply objects.
            reply = DownloadReply(self, request.url(), self.GetOperation, self._w)
            return reply
        else:
            return QNetworkAccessManager.createRequest(self, operation, request, data)



def main():
    # Again, this is boilerplate, it's going to be the same on
    # almost every app you write
    app = QtGui.QApplication(sys.argv)
    window=Main(sys.argv[1])
    window.show()
    # It's exec_ because exec is a reserved word in Python
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
