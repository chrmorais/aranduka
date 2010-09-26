from PyQt4 import QtNetwork, QtCore, QtGui, uic
import os, sys
from epubparser import EpubDocument

class Main(QtGui.QMainWindow):
    def __init__(self, fname):
        QtGui.QMainWindow.__init__(self)

        self.epub = EpubDocument(fname)
        
        uifile = os.path.join(
            os.path.abspath(
                os.path.dirname(__file__)),'epubviewer.ui')
        uic.loadUi(uifile, self)
        self.ui = self
        self.addAction(self.actionPageDown)


        for l,c in self.epub.tocentries:
            item = QtGui.QListWidgetItem(l)
            item.contents = c
            self.chapters.addItem(item)


        self.old_manager = self.view.page().networkAccessManager()
        self.new_manager = NetworkAccessManager(self.old_manager, self)
        self.view.page().setNetworkAccessManager(self.new_manager)

        self.openPath(self.epub.spinerefs[0])
        
    @QtCore.pyqtSlot()
    def on_actionPageDown_triggered(self):
        frame = self.view.page().mainFrame()
        if frame.scrollBarMaximum(QtCore.Qt.Vertical) == \
            frame.scrollPosition().y():
                # Find where on the spine we are
                curSpineRef= unicode(frame.url().toString())[12:]
                curIdx = self.epub.spinerefs.index(curSpineRef)
                if curIdx < len(self.spinerefs):
                    self.openPath(self.epub.spinerefs[curIdx+1])
        else:
            frame.scroll(0,self.view.height())
        
    def on_chapters_itemClicked(self, item):
        self.openPath(item.contents)


    def openPath(self, path, fragment=None):
        print "Opening:", path
        if "#" in path:
            path, fragment = path.split('#',1)
        xml = self.epub.getData(path)
        self.view.page().mainFrame().setHtml(xml,QtCore.QUrl("epub://book/"+path))
        if fragment:
            pass
            # FIXME: figure out how to jump to the anchor

    def linkClicked(self, url):
        if url.isRelative(): #They all should be
            frag = unicode(url.fragment())
            path = unicode(url.path())
            self.openPath(path, frag)

class DownloadReply(QtNetwork.QNetworkReply):

    def __init__(self, parent, url, operation, w):
        self._w = w
        print"DR:", url, url.path()
        QtNetwork.QNetworkReply.__init__(self, parent)
        self.content = self._w.epub.getData(unicode(url.path())[1:])
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
            return QtNetwork.QNetworkAccessManager.createRequest(self, operation, request, data)

        if operation == self.GetOperation:
            # Handle download:// URLs separately by creating custom
            # QNetworkReply objects.
            reply = DownloadReply(self, request.url(), self.GetOperation, self._w)
            return reply
        else:
            return QtNetwork.QNetworkAccessManager.createRequest(self, operation, request, data)



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
