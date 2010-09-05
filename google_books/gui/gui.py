#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
        Validar codigo ISBN. Devuelve el ISBN ó 0 si no es válido.
        """
        #TODO: deberia validar el ISBN con la cuenta

        #isbn.replace("-","") #Por ahora, lo mas sencillo

        isbn = ''.join(c for c in isbn if c.isdigit())

        #Intento de validación de ISBN según artículo de Paenza en Pag.12
        #ref: http://www.pagina12.com.ar/diario/contratapa/13-113285-2008-10-14.html
        #Aparentemente se podría corregir el error pero me dio fiaca..:)
        total = 0
        if len(isbn) == 10:
            for i,n in enumerate(isbn):
                total = total + (i+1) * int(n)
            if total % 11 == 0:
                return isbn
            else:
                return 0
        #El chequeo para ISBN de 13 digitos sale de:
        #ref: http://en.wikipedia.org/wiki/International_Standard_Book_Number#ISBN-13
        elif len(isbn) == 13:
            i = 1
            for n in isbn[:-1]:
                total = total + i * int(n)
                if i == 1: i = 3
                else: i = 1
            check = 10 - ( total % 10 )
            if check == int(isbn[-1]):
                return isbn
            else:
                return 0
        else:
            #Deberíamos devolver otro código de error acá?
            print "El ISBN Tiene que ser de 10 o 13 dígitos unicamente"
            return 0
                        

    def buscarLibro(self):
        """
        Busca un libro por ISBN en GoogleBooks y devuelve un dict con todos los datos o -1 si no valido el ISBN.
        """
        isbn = self.validaISBN(str(self.isbnEdit.text()))
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
