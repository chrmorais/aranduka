import os
from utils import SCRIPTPATH
from PyQt4.QtGui import QDialog
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtGui import QPixmap
from PyQt4.QtGui import QLabel
from PyQt4.QtCore import Qt
from PyQt4.QtCore import QSize

class AboutDialog(QDialog):

    def url (self):
        return 'http://aranduka.googlecode.com'

    def version (self):
        return self.tr('UNDER DEVELOPMENT')

    def __init__(self):
        QDialog.__init__(self,None,Qt.Dialog)
        self.setModal(True)
        self.setWindowTitle(self.tr('About Aranduka'))
        self.setMaximumSize(QSize(0,0)) #So there's no maximize button.
        v_box = QVBoxLayout(self)
        logo = os.path.join(SCRIPTPATH,'aranduka-logo.png')
        pixmap = QPixmap(logo)
        labIcon = QLabel('')
        labIcon.setScaledContents(True)
        labIcon.setPixmap(pixmap.scaled(400,150))
        hbox = QHBoxLayout()
        hbox.addWidget(labIcon)
        v_box.addLayout(hbox)
        v_box.addWidget(QLabel(unicode(self.tr("""Like Calibre but easy..."""))))
        v_box.addWidget(QLabel(unicode(self.tr('Version: %s')) % self.version()))
        v_box.addWidget(QLabel(unicode(self.tr('Website: <a href="%s">%s</a>')) % \
                               (self.url(), self.url())))
