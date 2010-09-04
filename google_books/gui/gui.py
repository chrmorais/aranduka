#!/usr/bin/env python
# -*- coding: latin -*-

import sys, urllib2
from PyQt4 import QtCore, QtGui, uic
from gdata.books.service import BookService
servicio = BookService()

app = QtGui.QApplication(sys.argv)
form_class, base_class = uic.loadUiType('interface.ui')

class GBooks(QtGui.QMainWindow, form_class):
    def __init__(self, *args):
        super(GBooks, self).__init__(*args)
        self.setupUi(self)

    def validaISBN(self,isbn):  
        """
        Validar codigo ISBN
        """
        #TODO: deberia tambien filtrar caracteres no numericos

        return isbn.replace("-","") #Por ahora, lo mas sencillo

    def buscarLibro(self):
        """
        Busca un libro por ISBN en GoogleBooks y devuelve un dict con todos los datos.
        """
        isbn = self.validaISBN(str(self.isbnEdit.text()))
        resultado = servicio.search('ISBN' + isbn)
        if resultado.entry:
            return resultado.entry[0].to_dict()

    def on_actionBuscarLibro_triggered(self, checked = None):
        if checked == None: return
        datos = self.buscarLibro()
        identifiers = dict(datos['identifiers'])
        print datos['identifiers']
        print identifiers
        if datos:
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
            print 'No encontre ese ISBN :('


if __name__ == '__main__':
    ventana = GBooks()
    ventana.show()
    sys.exit(app.exec_())
