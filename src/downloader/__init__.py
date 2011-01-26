from PyQt4 import QtGui, QtCore, QtNetwork
import sys

class Downloads(QtGui.QDialog):

    def __init__(self,parent=None):
        super(Downloads,self).__init__(parent)        
        self.bars={}
        
        self.layout = QtGui.QVBoxLayout()
        self.setLayout(self.layout)
        self.manager = QtNetwork.QNetworkAccessManager(self)
        self.avgBar = QtGui.QProgressBar()
        self.layout.addWidget(self.avgBar)
        
    def fetch(self, url):
        if url in self.bars:
            print "Already downloading:", url
            return
        print "Downloading:", url
        address = QtCore.QUrl(url)
        reply = self.manager.get(QtNetwork.QNetworkRequest(address))
        reply.downloadProgress.connect(self.progress)
        bar = QtGui.QProgressBar()
        self.layout.addWidget(bar)
        self.bars[url]=[url, bar, reply]
                
    def progress(self, received, total):
        url = unicode(self.sender().url().toString())
        print "progress:", url
        _, bar, reply = self.bars[url]
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
