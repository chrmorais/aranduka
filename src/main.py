"""The user interface for our app"""

import os,sys
import models, config, ui

# Import Qt modules
from PyQt4 import QtCore, QtGui, uic, QtWebKit
from progress import progress
from book_editor import BookEditor
import rc_icons
from pluginmgr import manager, isPluginEnabled
from pluginconf import PluginSettings
from about import AboutDialog
from epubviewer import Main as EpubViewer
from cbzviewer import Main as CbzViewer
import downloader

class SearchWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        uifile = ui.path('searchwidget.ui')
        uic.loadUi(uifile, self)
        self.ui = self

class Main(QtGui.QMainWindow):
    updateShelves = QtCore.pyqtSignal()
    updateBook = QtCore.pyqtSignal(models.Book)
    
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        uifile = ui.path('main.ui')
        uic.loadUi(uifile, self)
        self.ui = self
        self.viewers=[]

        self.currentBook = None

        # Set default stylesheet for all web views in the app
        wksettings = QtWebKit.QWebSettings.globalSettings()
        # FIXME: this doesn't work
        wksettings.setMaximumPagesInCache(0)
        ssurl = QtCore.QUrl().fromLocalFile(os.path.join(os.path.dirname(__file__), 'master.css'))
        wksettings.setUserStyleSheetUrl(ssurl)
        
        
        # View types toggles
        self.viewGroup = QtGui.QButtonGroup(self)
        self.viewGroup.setExclusive(True)
        self.viewGroup.addButton(self.gridMode)
        self.viewGroup.addButton(self.listMode)
        self.viewGroup.buttonClicked.connect(self.viewModeChanged)
        self.gridMode.setChecked(True)

        # Search Bar
        self.searchBar = QtGui.QToolBar()
        self.addToolBar(QtCore.Qt.BottomToolBarArea, self.searchBar)
        self.searchWidget = SearchWidget()
        self.searchBar.addWidget(self.searchWidget)
        self.searchBar.hide()
        self.searchWidget.closeBar.clicked.connect(self.searchBar.hide)
        self.searchButton.toggled.connect(self.searchBar.setVisible)
        self.searchButton.toggled.connect(self.searchWidget.text.setFocus)
        
        self._layout = QtGui.QVBoxLayout()
        self.details.setLayout(self._layout)
        self.book_editor = BookEditor(None)
        self.book_editor.cancel.clicked.connect(self.viewModeChanged)
        self.book_editor.save.clicked.connect(self.viewModeChanged)
        self.book_editor.updateBook.connect(self.updateBook)
        self._layout.addWidget(self.book_editor)
        print "Finished initializing main window"

        self.loadPlugins()
        geom = config.getValue("general", "geometry",None)
        if geom is not None:
            self.restoreGeometry(geom.decode('base64'))

        downloader.downloader = downloader.Downloads()
        downloader.downloader.setStatusMessage.connect(self.setStatusMessage)
        self.statusBar.addPermanentWidget(downloader.downloader)
        self.progBar = QtGui.QProgressBar()
        self.progBar.setMaximumWidth(100)
        self.statusBar.addPermanentWidget(self.progBar)
        self.progBar.setVisible(False)
        
    def closeEvent(self, event):
        config.setValue("general","geometry",str(self.saveGeometry()).encode('base64'))
        QtGui.QMainWindow.closeEvent(self, event)
        

    def loadPlugins(self):
        # FIXME: separate by category so you can load just one

        # Plugins
        manager.locatePlugins()
        manager.loadPlugins()

        enabled_plugins = set(config.getValue("general","enabledPlugins", [None]))
        if enabled_plugins == set([None]):
            enabled_plugins = set()
            #Never configured... enable everything! (will change later ;-)
            for c in manager.getCategories():
                for p in manager.getPluginsOfCategory(c):
                    enabled_plugins.add(p.name)

        self.treeWidget.clear()

        for plugin in manager.getPluginsOfCategory("ShelfView"):
            # Ways to fill the shelves
            if plugin.name not in enabled_plugins:
                continue
            item = plugin.plugin_object.treeItem()
            item.handler = plugin.plugin_object
            item.title = plugin.plugin_object.title
            plugin.plugin_object.setWidget(self)
            self.treeWidget.addTopLevelItem(item)
            if item.handler.itemText == "Titles":
                self.on_treeWidget_itemClicked(item)
                self.treeWidget.setCurrentItem(item)

        for plugin in manager.getPluginsOfCategory("BookStore"):
            # Ways to acquire books
            if plugin.name not in enabled_plugins:
                continue

            # Hook progress report signals
            plugin.plugin_object.loadStarted.connect(self.loadStarted)
            plugin.plugin_object.loadFinished.connect(self.loadFinished)
            plugin.plugin_object.loadProgress.connect(self.loadProgress)
            plugin.plugin_object.setStatusMessage.connect(self.setStatusMessage)
            
            # Add to the Store list
            item = plugin.plugin_object.treeItem()
            item.handler = plugin.plugin_object
            item.title = plugin.plugin_object.title
            plugin.plugin_object.setWidget(self)
            self.treeWidget.addTopLevelItem(item)

        self.menuDevices.clear()

        for plugin in manager.getPluginsOfCategory("Device"):
            if plugin.name not in enabled_plugins:
                continue
            dev_menu = QtGui.QMenu(plugin.plugin_object.name, self)
            print "Adding menu:", plugin.plugin_object.name
            for a in plugin.plugin_object.deviceActions():
                print a
                dev_menu.addAction(a)
            dev_menu.addSeparator()
            dev_menu.addAction(plugin.plugin_object.actionNew())
            self.menuDevices.addMenu(dev_menu)

    @QtCore.pyqtSlot()
    def loadStarted(self):
        self.progBar.setVisible(True)
    @QtCore.pyqtSlot()
    def loadFinished(self):
        self.progBar.setVisible(False)
        self.statusBar.clearMessage()
    @QtCore.pyqtSlot("int")
    def loadProgress(self, p):
        self.progBar.setVisible(True)
        self.progBar.setValue(p)
        if p == 100:
            self.statusBar.clearMessage()
    @QtCore.pyqtSlot("PyQt_PyObject")
    def setStatusMessage(self, msg):
        self.statusBar.showMessage(msg)

            
    @QtCore.pyqtSlot()
    def on_actionPlugins_triggered(self):
        dlg = PluginSettings(self)
        dlg.exec_()

    @QtCore.pyqtSlot()
    def on_menuTools_aboutToShow(self):
        self.menuTools.clear()
        for plugin in manager.getPluginsOfCategory("Tool"):
            if isPluginEnabled(plugin.name):
                self.menuTools.addAction(plugin.plugin_object.action())

    @QtCore.pyqtSlot()
    def on_menuImport_aboutToShow(self):
        self.menuImport.clear()
        for plugin in manager.getPluginsOfCategory("Importer"):
            if isPluginEnabled(plugin.name):
                for a in plugin.plugin_object.actions():
                    self.menuImport.addAction(a)
        
    def viewModeChanged(self):
        item = self.treeWidget.currentItem()
        if not item: return
        self.on_treeWidget_itemClicked(item)

    def on_treeWidget_itemClicked(self, item):
        try:
            self.searchWidget.doSearch.clicked.disconnect()
        except TypeError: # Happens when there's no connections
            pass
        # Show only the right action buttons
        self.gridMode.setVisible(item.handler.has_grid)
        self.listMode.setVisible(item.handler.has_list)
        self.searchButton.setVisible(item.handler.has_search)
        
        self.searchWidget.doSearch.clicked.connect(item.handler.doSearch)
        if self.gridMode.isChecked():
            item.handler.showGrid(currentBook = self.currentBook)
        else:
            item.handler.showList(currentBook = self.currentBook)

    def on_actionFind_triggered(self):
        self.searchBar.show()
        self.searchWidget.text.setFocus(True)
        
    def openCBZ(self, fname):
        try:
            viewer = CbzViewer(fname)
        except ValueError, e:
            QtGui.QMessageBox.critical(self, \
                                      u'Failed to open CBZ file', \
                                      u'The document you are trying to open is not a valid CBZ file.')
            return
        self.viewers.append(viewer)
        viewer.show()

    def openEpub(self, fname):
        try:
            viewer = EpubViewer(fname)
        except ValueError, e:
            QtGui.QMessageBox.critical(self, \
                                      u'Failed to open ePub file', \
                                      u'The document you are trying to open is not a valid ePub file.')
            return
        self.viewers.append(viewer)
        viewer.show()
        
    def bookContextMenuRequested(self, book, point):
        """Given a book, and a place in the screen,
        shows a proper context menu for it"""

        self.currentBook = book
        menu = QtGui.QMenu()
        menu.addAction(self.actionEdit_Book)
        menu.addAction(self.actionDelete_Book)

        # Create menu with files for this book
        open_menu = QtGui.QMenu("Open")
        formats = book.available_formats()
        if len(formats) == 1:
            # A single file
            f = book.files[0]
            url = QtCore.QUrl.fromLocalFile(f.file_name)
            if f.file_name.endswith('epub'):
                action = menu.addAction("Open %s"%os.path.basename(f.file_name),
                    lambda f = f: self.openEpub(f.file_name))
            elif f.file_name.endswith('cbz'):
                action = menu.addAction("Open %s"%os.path.basename(f.file_name),
                    lambda f = f: self.openCBZ(f.file_name))
            else:
                action = menu.addAction("Open %s"%os.path.basename(f.file_name),
                    lambda f = f: QtGui.QDesktopServices.openUrl(url))
                    
            # Issue 20: don't show files that are not there
            # FIXME: add more validation
            try:
                f_info = os.stat(f.file_name)
            except:
                f_info = None
            if f_info is None or f_info.st_size == 0:
                action.setEnabled(False)
            
        elif formats:
            for f in book.files:
                url = QtCore.QUrl.fromLocalFile(f.file_name)
                if f.file_name.endswith('epub'):
                    action = menu.addAction("Open %s"%os.path.basename(f.file_name),
                        lambda f = f: self.openEpub(f.file_name))
                else:
                    action = menu.addAction("Open %s"%os.path.basename(f.file_name),
                        lambda f = f: QtGui.QDesktopServices.openUrl(url))
                open_menu.addAction(action)
            menu.addMenu(open_menu)

        # Check what converters apply
        converters = []
        for plugin in manager.getPluginsOfCategory("Converter"):
            if isPluginEnabled(plugin.name):
                r = plugin.plugin_object.can_convert(book)
                if r:
                    converters.append([plugin.plugin_object, r])

        if converters:
            # So, we can convert
            convert_menu = QtGui.QMenu("Convert")
            for plugin, formats in converters:
                for f in formats:
                    convert_menu.addAction("%s via %s"%(f, plugin.name),
                        lambda f = f : plugin.convert(book, f))

            menu.addMenu(convert_menu)
            
        menu.exec_(point)

    @QtCore.pyqtSlot()
    def on_actionOpen_Book_triggered(self):
        if not self.currentBook:
            return
        if self.currentBook.files:
            url = QtCore.QUrl.fromLocalFile(self.currentBook.files[0].file_name)
            print "Opening:", url
            QtGui.QDesktopServices.openUrl(url)

    @QtCore.pyqtSlot()
    def on_actionEdit_Book_triggered(self):
        if not self.currentBook:
            return
        self.book_editor.load_data(self.currentBook.id)
        self.title.setText(u'Editing properties of "%s"'%self.currentBook.title)
        self.stack.setCurrentIndex(1)

    @QtCore.pyqtSlot()
    def on_actionDelete_Book_triggered(self):
        if not self.currentBook:
            return
        rsp = QtGui.QMessageBox.question(self, \
                                   'Confirm delete', \
                                   'Are you sure you want to delete the book "%s"?'%\
                                   self.currentBook.title, \
                                   QtGui.QMessageBox.Cancel, QtGui.QMessageBox.Ok)
        if rsp == QtGui.QMessageBox.Ok:
            # Delete the book files
            print "Deleting book: %s"%self.currentBook.title
            self.currentBook.delete()
            models.session.commit()
            self.currentBook = None
            self.viewModeChanged()
            
    def on_books_itemActivated(self, item):
        self.currentBook = item.book
        self.on_actionEdit_Book_triggered()

    @QtCore.pyqtSlot()
    def on_actionAbout_triggered(self):
        about = AboutDialog()
        about.exec_()
                    

def main():
    # Init the database before doing anything else
    models.initDB()

    # Again, this is boilerplate, it's going to be the same on
    # almost every app you write
    app = QtGui.QApplication(sys.argv)
    window=Main()
    window.show()
    # It's exec_ because exec is a reserved word in Python
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
