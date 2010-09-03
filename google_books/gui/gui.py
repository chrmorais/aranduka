#!/usr/bin/env python
# -*- coding: latin -*-

import sys
from PyQt4 import QtCore, QtGui, uic
from gdata.books.service import BookService
servicio = BookService()

app = QtGui.QApplication(sys.argv)
form_class, base_class = uic.loadUiType('interface.ui')

class GBooks(QtGui.QMainWindow, form_class):
    def __init__(self, *args):
        super(GBooks, self).__init__(*args)
        self.setupUi(self)
        
    def buscarLibro():
        """
        Busca un libro por ISBN en GoogleBooks y devuelve un dict con todos los datos.
        """
        isbn = str(self.isbnEdit.text())
        resultado = servicio.search('ISBN' + isbn)
        if resultado.entry:
            return resultado.entry[0].to_dict()

    def on_actionBuscarLibro_triggered(self, checked = None):
        if checked == None: return
        datos = buscarLibro()
        if resultado:
            self.tituloLibro.setText(datos['title'])
            self.fechaLibro.setText(datos['date'])
            self.generosLibro.setText(', '.join(datos['subjects']))
            self.autoresLibro.setText(', '.join(datos['authors']))
            self.descripcionLibro.setText(datos['description'])
            
            #Merengue para bajar la thumbnail porque QPixmap
            #no levanta desde una url :(
            #urlImg = QtCore.QUrl(datos['thumbnail'])
            #http = QtCore.QHttp( urlImg.host() )
            #tmpFile = QtCore.QTemporaryFile()
            #http.get(urlImg.path(),tmpFile)
            #self.tapaLibro.setPixmap(QtGui.QPixmap(tmpFile.fileName()))
            #http.close()
            #tmpFile.close()
        else:
            print 'No encotre ese ISBN :('


if __name__ == '__main__':
    ventana = GBooks()
    ventana.show()
    sys.exit(app.exec_())
