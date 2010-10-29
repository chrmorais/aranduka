from PyQt4.QtGui import QDialog
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtGui import QPixmap
from PyQt4.QtGui import QLabel
from PyQt4.QtCore import Qt

class AboutDialog(QDialog):
    
    def __init__(self):
        QDialog.__init__(self)
        self.setModal(True)
        self.setWindowTitle('About Aranduka')
        v_box = QVBoxLayout(self)
        
        pixmap = QPixmap('/home/ramiro/aranduka/src/aranduka-logo.png')
        labIcon = QLabel('')
        labIcon.setScaledContents(True)
        labIcon.setPixmap(pixmap.scaled(400,150))
        hbox = QHBoxLayout()
        hbox.addWidget(labIcon)
        v_box.addLayout(hbox)
        v_box.addWidget(QLabel("""Like Calibre but easy..."""))
        v_box.addWidget(QLabel('Version: UNDER DEVELOPMENT'))
        v_box.addWidget(QLabel('Website: <a href="http://aranduka.googlecode.com">http://aranduka.googlecode.com</a>'))