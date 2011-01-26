#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, urllib2, ui

from gdata.books.service import BookService
from PyQt4 import QtCore, QtGui, uic

import models
from utils import validate_ISBN, SCRIPTPATH
from metadata import BookMetadata
from pluginmgr import manager, isPluginEnabled

class IdentifierDialog(QtGui.QDialog):
    def __init__(self, id_key, id_value, *args):
        QtGui.QDialog.__init__(self,*args)
        uifile = ui.path('identifier.ui')
        uic.loadUi(uifile, self)
        self.ui = self
        self._query = None
        self.id_key.setText(id_key)
        self.id_value.setText(id_value)

class TagDialog(QtGui.QDialog):
    def __init__(self, tag_name, *args):
        QtGui.QDialog.__init__(self,*args)
        uifile = ui.path('tag.ui')
        uic.loadUi(uifile, self)
        self.ui = self
        self._query = None
        for t in models.Tag.query.all():
            self.tag_name.addItem(t.name, t.name)
        self.tag_name.setEditText(tag_name)

class GuessDialog(QtGui.QDialog):
    def __init__(self, guesser, book, *args):
        QtGui.QDialog.__init__(self,*args)
        uifile = ui.path('guess.ui')
        uic.loadUi(uifile, self)
        self.ui = self
        self.setWindowTitle('Guess book information')
        self._query = None
        self.md=[]
        self.currentMD=None
        self.book = book
        self.guesser = guesser
        self.title.setText("Title: %s"%book.title)
        self.author.setText("Author: %s"%(u', '.join([a.name for a in book.authors])))
        ident = models.Identifier.get_by(key='ISBN',book=book)
        if ident:
            self.isbn.setText('ISBN: %s'%ident.value)
            self._isbn=ident.value
        else:
            self.isbn.hide()

    def on_bookList_currentRowChanged(self, row):
        self.currentMD=self.md[row]
        print "Selected: ",unicode(self.bookList.item(row).text())

    @QtCore.pyqtSlot()
    def on_guess_clicked(self):
        # Try to guess based on the reliable data
        query = {'title': None, \
                 'authors': None, \
                 'isbn': None}
        self.bookList.clear()
        if self.title.isChecked():
            query['title'] = self.book.title
        if self.author.isChecked():
            query['authors'] = u', '.join([a.name for a in self.book.authors])
        if self.isbn.isChecked():
            query['isbn'] = self._isbn

        if query['title'] is None and \
           query['authors'] is None and \
           query['isbn'] is None:
           return

        self._query = BookMetadata(title=query['title'],
                                   thumbnail=None,
                                   date=None,
                                   subjects=None,
                                   authors=query['authors'],
                                   identifiers=[query['isbn']],
                                   description=None)
        if self._query:
            try:
                self.md = self.guesser.guess(self._query) or []
            except Exception, e:
                print "Guesser exception: %s"%str(e)
                QtGui.QMessageBox.warning(self, \
                                          u'Failed to load data', \
                                          str(e))
                return

            if self.md:
                for candidate in self.md:
                    authors = candidate.authors
                    if isinstance(authors, list):
                        authors = u', '.join(authors)
                    self.bookList.addItem(u'%s by %s'%(candidate.title, authors))
            else:
                print "No matches found for the selected criteria"
                QtGui.QMessageBox.information(self, \
                                              u'No results', \
                                              u'No results found matching your criteria')


class BookEditor(QtGui.QWidget):
    
    updateBook = QtCore.pyqtSignal(models.Book)
    
    def __init__(self, book_id = None, *args):
        QtGui.QWidget.__init__(self,*args)
        uifile = ui.path('book_editor.ui')
        uic.loadUi(uifile, self)
        self.ui = self
        if book_id is not None:
            self.load_data(book_id)

    def load_data(self, book_id):
        self.book = models.Book.get_by(id=book_id)
        if not self.book:
            # Called with invalid book ID
            print "Wrong book ID"
        self.title.setText(self.book.title)
        self.authors.setText('|'.join([a.name for a in self.book.authors]))
        self.ids.clear()
        for i in self.book.identifiers:
            self.ids.addItem("%s: %s"%(i.key,i.value))

        self.fileList.clear()
        for f in self.book.files:
            self.fileList.addItem(f.file_name)

        self.tags.clear()
        for t in self.book.tags:
            self.tags.addItem(t.name)

        cname = self.book.cover()
        self.cover.setPixmap(QtGui.QPixmap(cname).scaledToHeight(200,QtCore.Qt.SmoothTransformation))

        self.guesser_dict={}
        self.guessers.clear()
        # Fill the guessers combo with appropiate names
        for plugin in manager.getPluginsOfCategory("Guesser"):
            if isPluginEnabled(plugin.name) and plugin.plugin_object.can_guess(self.book):
                self.guessers.addItem(plugin.plugin_object.name)
                self.guesser_dict[plugin.plugin_object.name] = plugin.plugin_object

    @QtCore.pyqtSlot()
    def on_guess_clicked(self):
        name = unicode(self.guessers.currentText())

        # Display the Guess Dialog
        dlg = GuessDialog(self.guesser_dict[name], self.book)
        r = dlg.exec_()
        if not r == dlg.Accepted:
            md = None
        elif dlg.currentMD:
            md =  dlg.currentMD

        if md is None:
            return
        else:
            # A candidate was chosen, update data
            self.title.setText(md.title)
            self.authors.setText('|'.join(md.authors))
            # FIXME: maybe there are identifier conflicts?
            items = [unicode(self.ids.itemText(i)) for i in range(self.ids.count())]
            if md.identifiers is not None:
                for k,v in md.identifiers:
                    items.append("%s: %s"%(k,v))
            items = list(set(items))
            items.sort()
            self.ids.clear()
            self.ids.addItems(items)
            self.on_save_clicked()
            self.load_data(self.book.id)
            self.book.fetch_cover()
            self.load_data(self.book.id)

    @QtCore.pyqtSlot()
    def on_save_clicked(self):
        # Save the data first
        self.book.title = unicode(self.title.text())

        self.book.authors = []
        authors = unicode(self.authors.text()).split('|')
        for a in authors:
            author = models.Author.get_by(name = a)
            if not author:
                print "Creating author:", a
                author = models.Author(name = a)
            self.book.authors.append(author)
        models.Author.sanitize()

        for ident in self.book.identifiers:
            ident.delete()
        for i in range(self.ids.count()):
            t = unicode(self.ids.itemText(i))
            k, v = t.split(': ',1)
            i = models.Identifier(key = k, value = v, book = self.book)

        for old_file in self.book.files:
            old_file.delete()
        for file_name in [unicode(self.fileList.item(i).text()) for i in range(self.fileList.count())]:
            f = models.File(file_name=file_name, book=self.book)

        self.book.tags = []
        for tag_name in [unicode(self.tags.item(i).text()) for i in range(self.tags.count())]:
            t = models.Tag.get_by(name=tag_name)
            if not t:
                t = models.Tag(name=tag_name, value=tag_name)
            self.book.tags.append(t)

        models.session.commit()
        self.updateBook.emit(self.book)

    @QtCore.pyqtSlot()
    def on_add_file_clicked(self):
        file_name = unicode(QtGui.QFileDialog.getOpenFileName(self, 'Add File'))
        if file_name and not self.fileList.findItems(file_name, QtCore.Qt.MatchExactly):
            self.fileList.addItem(file_name)

    @QtCore.pyqtSlot()
    def on_remove_file_clicked(self):
        self.fileList.takeItem(self.fileList.currentRow())

    @QtCore.pyqtSlot()
    def on_add_id_clicked(self):
        dlg = IdentifierDialog('', '', self)
        r = dlg.exec_()
        if not r == dlg.Accepted:
            return
        self.ids.addItem("%s: %s"%(dlg.id_key.text(), dlg.id_value.text()))

    @QtCore.pyqtSlot()
    def on_remove_id_clicked(self):
        self.ids.removeItem(self.ids.currentIndex())

    @QtCore.pyqtSlot()
    def on_edit_id_clicked(self):
        k, v = self.ids.currentText().split(": ",1)
        dlg = IdentifierDialog(k, v, self)
        r = dlg.exec_()
        if not r == dlg.Accepted:
            return
        self.ids.setItemText(self.ids.currentIndex(), "%s: %s"%(
            dlg.id_key.text(), dlg.id_value.text()))

    @QtCore.pyqtSlot()
    def on_add_tag_clicked(self):
        dlg = TagDialog('', self)
        r = dlg.exec_()
        if not r == dlg.Accepted:
            return
        self.tags.addItem(dlg.tag_name.currentText())

    @QtCore.pyqtSlot()
    def on_remove_tag_clicked(self):
        self.tags.takeItem(self.tags.currentRow())

    def findBook(self):
        """
        Busca un libro por ISBN en GoogleBooks y devuelve un dict con todos los datos o -1 si no valido el ISBN.
        """
        isbn = validate_ISBN(str(self.isbnEdit.text()))
        if isbn:
            result = service.search('ISBN' + isbn)
            if result.entry:
                return result.entry[0].to_dict()
        else:
            return -1

    def on_actionfindBook_triggered(self, checked = None):
        if checked == None: return

        datos = self.findBook()

        if datos == -1:
            QtGui.QMessageBox.critical(self,
                                       self.trUtf8("Error"),
                                       self.trUtf8("Por favor revise el ISBN, parece ser erróneo."),
                                       QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Ok)
                                       )

        elif datos:

            #Vaciar imagen siempre
            thumb = QtGui.QPixmap(os.path.join(SCRIPTPATH,"nocover.png"))
            self.tapaLibro.setPixmap(thumb)

            identifiers = dict(datos['identifiers'])
            #print datos['identifiers']

            if 'title' in datos:
               self.txt_1.setText(datos['title'].decode('utf-8'))
            if 'date' in datos:
               self.dte_1.setDateTime(QtCore.QDateTime.fromString(datos['date'],'yyyy-mm-dd'))
            if 'subjects' in datos:
               self.txt_2.setText(', '.join(datos['subjects']).decode('utf-8'))
            if 'authors' in datos:
               self.txt_3.setText(', '.join(datos['authors']).decode('utf-8'))
            if 'description' in datos:
               self.txp_1.appendPlainText(datos['description'].decode('utf-8'))

            #Merengue para bajar la thumbnail porque QPixmap
            #no levanta desde una url :(
            
            # TODO
            # Si no tenemos la tapa en covers.openlibrary, deberia leerlo desde google.books.
            # El dato clave estaría en datos['thumbnail']

            thumbdata = urllib2.urlopen('http://covers.openlibrary.org/b/isbn/%s-M.jpg'%identifiers['ISBN']).read()
            
            thumb = QtGui.QPixmap()
            # FIXME: en realidad habrí­a que guardarlo
            thumb.loadFromData(thumbdata)
            self.tapaLibro.setPixmap(thumb)

        else:
            # El ISBN es válido pero BookEditor no lo tiene, ej: 950-665-191-4
            self.txt_1.setText('')
            #self.fechaLibro.setText('')
            self.txt_2.setText('')
            self.txt_3.setText('')
            self.txp_1.appendPlainText('')
            QtGui.QMessageBox.critical(self,
                                       self.trUtf8("Error"),
                                       self.trUtf8("El ISBN parece ser válido, pero no se encontró libro con el número indicado."),
                                       QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Ok)
                                       )

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    models.initDB()
    if len(sys.argv) == 1:
        # use a default book
        ventana = BookEditor(models.Book.get_by().id)
    else:
        ventana = BookEditor(int(sys.argv[1]))
    ventana.show()
    sys.exit(app.exec_())
