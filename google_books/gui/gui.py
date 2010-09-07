#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, urllib2

from gdata.books.service import BookService
from PyQt4 import QtCore, QtGui, uic

from utils import validate_ISBN


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
        isbn = validate_ISBN(str(self.isbnEdit.text()))
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
            #print datos['identifiers']

            if 'title' in datos:
               self.tituloLibro.setText(datos['title'].decode('utf-8'))
            if 'date' in datos:
               self.fechaLibro.setText(datos['date'].decode('utf-8'))
            if 'subjects' in datos:
               self.generosLibro.setText(', '.join(datos['subjects']).decode('utf-8'))
            if 'authors' in datos:
               self.autoresLibro.setText(', '.join(datos['authors']).decode('utf-8'))
            if 'description' in datos:
               self.descripcionLibro.setText(datos['description'].decode('utf-8'))

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
            # El ISBN es válido pero GBooks no lo tiene, ej: 950-665-191-4
            self.tituloLibro.setText('')
            self.fechaLibro.setText('')
            self.generosLibro.setText('')
            self.autoresLibro.setText('')
            self.descripcionLibro.setText('')
            QtGui.QMessageBox.critical(self,
                                       self.trUtf8("Error"),
                                       self.trUtf8("El ISBN parece ser válido, pero no se encontró libro con el número indicado."),
                                       QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Ok)
                                       )

if __name__ == '__main__':
    ventana = GBooks()
    ventana.show()
    sys.exit(app.exec_())
