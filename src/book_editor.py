#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, urllib2

from gdata.books.service import BookService
from PyQt4 import QtCore, QtGui, uic

import models
from utils import validate_ISBN
from metadata import get_metadata

service = BookService()

class GuessDialog(QtGui.QDialog):
    def __init__(self, book, *args):
        QtGui.QDialog.__init__(self,*args)
        uifile = os.path.join(
            os.path.abspath(
                os.path.dirname(__file__)),'guess.ui')
        uic.loadUi(uifile, self)
        self.ui = self
        self._query = None

        self.md=[]
        self.currentMD=None
        self.book = book
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
        q=''
        if self.title.isChecked():
            q+='TITLE %s '%self.book.title
        if self.author.isChecked():
            q+='AUTHOR %s '%u', '.join([a.name for a in self.book.authors])
        if self.isbn.isChecked():
            q+='ISBN %s'%self._isbn
        self._query = q
        if self._query:
            self.md = get_metadata(self._query)
        for candidate in self.md:
            authors = ', '.join(candidate.authors)
            self.bookList.addItem("%s by %s"%(candidate.title, authors))

class BookEditor(QtGui.QWidget):
    def __init__(self, book_id = None, *args):
        QtGui.QWidget.__init__(self,*args)
        uifile = os.path.join(
            os.path.abspath(
                os.path.dirname(__file__)),'book_editor.ui')
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
        self.id_keys.clear()
        self.id_values.clear()
        for i in self.book.identifiers:
            self.id_keys.addItem(i.key)
            self.id_values.addItem(i.value)

        self.fileList.clear()
        for f in self.book.files:
            self.fileList.addItem(f.file_name)

        cname = os.path.join("covers",str(self.book.id)+".jpg")
        if os.path.isfile(cname):
            self.cover.setPixmap(QtGui.QPixmap(cname))
        else:
            self.cover.setPixmap(QtGui.QPixmap("nocover.png"))

    @QtCore.pyqtSlot()
    def on_guess_clicked(self):
        dlg = GuessDialog(self.book, self)
        r = dlg.exec_()
        if not r == dlg.Accepted:
            return
        if dlg.currentMD:
            md = dlg.currentMD
            # A candidate was chosen, update data
            self.title.setText(md.title)
            self.authors.setText('|'.join(md.authors))
            self.id_keys.clear()
            self.id_values.clear()
            for k,v in md.identifiers:
                self.id_keys.addItem(k)
                self.id_values.addItem(v)
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
        for ident in self.book.identifiers:
            ident.delete()
        for i in range(self.id_keys.count()):
            k = unicode(self.id_keys.itemText(i))
            v = unicode(self.id_values.itemText(i))
            i = models.Identifier(key = k, value = v, book = self.book)
        # TODO: save the rest of the data
        models.session.commit()

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
            thumb = QtGui.QPixmap("nocover.png")
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
    ventana = BookEditor(int(sys.argv[1]))
    ventana.show()
    sys.exit(app.exec_())
