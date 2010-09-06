#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, urllib2

from gdata.books.service import BookService
from PyQt4 import QtCore, QtGui, uic

from utils import valida_ISBN


servicio = BookService()


app = QtGui.QApplication(sys.argv)
form_class, base_class = uic.loadUiType('interface.ui')


class GBooks(QtGui.QMainWindow, form_class):
    def __init__(self, *args):
        super(GBooks, self).__init__(*args)
        self.setupUi(self)

    def buscarLibro(self):
        """
        Busca un libro por ISBN en GoogleBooks y devuelve un dict con todos los datos o -1 si no valido el ISBN.
        """
        isbn = valida_ISBN(str(self.isbnEdit.text()))
        if isbn:
            resultado = servicio.search('ISBN' + isbn)
            if resultado.entry:
                return resultado.entry[0].to_dict()
        else:
            return -1

    def on_actionBuscarLibro_triggered(self, checked = None):
        if checked == None: return

        datos = self.buscarLibro()

        if datos == -1:
            QtGui.QMessageBox.critical(self,
                                       self.trUtf8("Error"),
                                       self.trUtf8("Por favor revise el ISBN, parece ser erróneo."),
                                       QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Ok)
                                       )

        elif datos:

            #Vaciar imagen siempre
            thumb = QtGui.QPixmap("sintapa.png")
            self.tapaLibro.setPixmap(thumb)

            identifiers = dict(datos['identifiers'])
            print datos['identifiers']
            print identifiers
            self.tituloLibro.setText(datos['title'])
            self.fechaLibro.setText(datos['date'])
            self.generosLibro.setText(', '.join(datos['subjects']))
            self.autoresLibro.setText(', '.join(datos['authors']))
            self.descripcionLibro.setText(datos['description'])

            #Merengue para bajar la thumbnail porque QPixmap
            #no levanta desde una url :(

            thumbdata = urllib2.urlopen('http://covers.openlibrary.org/b/isbn/%s-M.jpg'%identifiers['ISBN']).read()
            thumb = QtGui.QPixmap()
            # FIXME: en realidad habría que guardarlo
            thumb.loadFromData(thumbdata)
            self.tapaLibro.setPixmap(thumb)

        else:
            self.tituloLibro.setText('')
            self.fechaLibro.setText('')
            self.generosLibro.setText('')
            self.autoresLibro.setText('')
            self.descripcionLibro.setText('')

if __name__ == '__main__':
    ventana = GBooks()
    ventana.show()
    sys.exit(app.exec_())
