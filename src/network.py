from PySide import QtNetwork, QtCore, QtGui, QtDeclarative

class NMFactory(QtDeclarative.QDeclarativeNetworkAccessManagerFactory):

    def __init__(self,*args):
        QtDeclarative.QDeclarativeNetworkAccessManagerFactory.__init__(self, *args)

    def create(self, *args):
        self.new_manager = NetworkAccessManager()
        return self.new_manager

class NetworkAccessManager(QtNetwork.QNetworkAccessManager):

    def __init__(self):
        self._w = None
        QtNetwork.QNetworkAccessManager.__init__(self)

    def createRequest(self, operation, request, data):
        if request.url().host() not in ["epub.epub"]:
            return QtNetwork.QNetworkAccessManager.createRequest(self, operation, request, data)

        if operation == self.GetOperation and not unicode(request.url().toString()).lower().endswith('css'):
            reply = DownloadReply(self, request.url(), self.GetOperation, self._w)
            return reply
        else:
            return QtNetwork.QNetworkAccessManager.createRequest(self, operation, request, data)


class DownloadReply(QtNetwork.QNetworkReply):
    
    def __init__(self, parent, url, operation, w):
        self._w = w
        QtNetwork.QNetworkReply.__init__(self, parent)
        self.content = self._w.getData(unicode(url.path())[1:])
        self.open(self.ReadOnly | self.Unbuffered)
        self.setUrl(url)
        QtCore.QTimer.singleShot(0, self.readyRead.emit)
        QtCore.QTimer.singleShot(1, self.finished.emit)

    def abort(self):
        pass

    def bytesAvailable(self):
        return len(self.content) + QtCore.QIODevice.bytesAvailable(self)

    def disconnectNotify(self, *args):
        QtNetwork.QNetworkReply.disconnectNotify(self, *args)

    def readData(self, size):
        size = min(size, len(self.content))
        data, self.content = self.content[:size], self.content[size:]
        return data
