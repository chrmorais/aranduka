from PyQt4 import QtGui, QtCore, QtNetwork
import os, sys

class Downloads(QtGui.QWidget):

    setStatusMessage = QtCore.pyqtSignal("PyQt_PyObject")
    
    def __init__(self,parent=None):
        super(Downloads,self).__init__(parent)
        self.label1 = QtGui.QLabel("Total:", self)
        self.avgBar = QtGui.QProgressBar(self)
        self.bars={}        
        self.layout = QtGui.QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.label1)
        self.layout.addWidget(self.avgBar)
        self.manager = QtNetwork.QNetworkAccessManager(self)
        self.setVisible(False)
        
    def fetch(self, url, destination):
        if url in self.bars:
            print "Already downloading:", url
            return
        print "Downloading:", url
        address = QtCore.QUrl(url)
        reply = self.manager.get(QtNetwork.QNetworkRequest(address))
        reply.downloadProgress.connect(self.progress)
        reply.finished.connect(self.finished)
        bar = QtGui.QProgressBar()
        desc = QtGui.QLabel()
        name = os.path.basename(destination)
        if len(name) > 30:
            name = name[:27]+'...'
        desc.setText(name)
        self.layout.insertWidget(0,bar)
        self.layout.insertWidget(0,desc)
        self.bars[url]=[url, bar, reply, destination, desc]
        if len(self.bars) > 1:
            for bar in self.bars: 
                self.bars[bar][1].setVisible(True)
                self.bars[bar][4].setVisible(True)
                
    def finished(self):
        reply = self.sender()
        url = unicode(reply.url().toString())
        _, bar, _, fname, status = self.bars[url]
        redirURL = unicode(reply.attribute(QtNetwork.QNetworkRequest.RedirectionTargetAttribute).toString())
        del self.bars[url]
        bar.deleteLater()
        status.deleteLater()
        if len(self.bars) < 2:
            for bar in self.bars: 
                self.bars[bar][1].setVisible(False)
                self.bars[bar][4].setVisible(False)
            
        if redirURL and redirURL != url:
            # Need to redirect
            print "Following redirect to:", redirURL
            self.fetch (redirURL, fname)
        else:
            data = str(reply.readAll())
            f = open(fname,'wb')
            f.write(data)
            f.close()
            print "Finished downloading:", url
        
        
    def progress(self, received, total):
        url = unicode(self.sender().url().toString())
        print "progress:", url
        _, bar, reply, fname, status = self.bars[url]
        bar.setMaximum(total)
        bar.setValue(received)
        
        # Calculate average bar
        tot = 0
        val = 0
        for u in self.bars:
            bar = self.bars[u][1]
            if bar.maximum() == -1:
                tot += 100000 # Yes, this is evil
            else:
                tot += bar.maximum()
            val += bar.value()
        print tot, val
        self.avgBar.setMaximum(tot)
        self.avgBar.setValue(val)
        if tot==0 or tot==val:
            self.setVisible(False)
            self.setStatusMessage.emit(u"")
        else:
            self.setVisible(True)

def main():
    app = QtGui.QApplication(sys.argv)
    window=Downloads()
    window.show()
    window.fetch("http://www.kde.org")
    window.fetch("http://www.gnome.org")
    window.fetch("http://www.ubuntu.com")
    sys.exit(app.exec_())
    
        
if __name__ == "__main__":
    main()
