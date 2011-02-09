#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, ui

from PyQt4 import QtCore, QtGui, uic

import models
from metadata import BookMetadata

from templite import Templite
import time

class AboutBook(QtGui.QWidget):
    
    updateBook = QtCore.pyqtSignal(models.Book)
    
    def __init__(self, book_id = None, *args):
        QtGui.QWidget.__init__(self,*args)
        uifile = ui.path('about_book.ui')
        uic.loadUi(uifile, self)
        self.ui = self
        self.about_web_view.page().setLinkDelegationPolicy(self.about_web_view.page().DelegateAllLinks)
#        self.about_web_view.linkClicked.connect(self.updateWithCandidate)

        if book_id is not None:
            self.load_data(book_id)

    def load_data(self, book_id):
        self.book = models.Book.get_by(id=book_id)
        if not self.book:
            # Called with invalid book ID
            print "Wrong book ID"
        tpl = u"""
        <html>
        <body>
        <div style="min-height: 128px; border: solid 3px lightgrey; padding: 15px; border-radius: 15px; margin: 6px; -webkit-transition: all 500ms linear;" 
             onmouseover="this.style.border='solid 3px lightgreen'; this.style.backgroundColor='lightgreen'; document.getElementById('submit-'0').style.opacity=1.0;" 
             onmouseout="this.style.border='solid 3px lightgrey'; this.style.backgroundColor='white'; document.getElementById('submit-0').style.opacity=1.0;" >
            <img style="float: left; margin-right: 4px; max-height: 180px" src="file://${thumb}$">
            <div style="text-align: right; margin-top: 12px;">
                <b>${title}$</b><br>
                by ${', '.join([a.name for a in authors]) or ""}$<br>
                ${for identifier in identifiers:}$
                    <small>${identifier[0]}$: ${identifier[1]}$</small><br>
                ${:end-for}$
                <br>Tags for this book<br>
                ${for tag in tags:}$
                    <small>${tag}$</small><br>
                ${:end-for}$
                <br>Files for this book<br>
                ${for fname in files:}$
                    <small><a href="${fname}$">${fname}$</a></small><br>
                ${:end-for}$
            </div>
        </div>
        </body>
        </html>
        """
        self.template = Templite(tpl)
        t1 = time.time()
        html = self.template.render(
            title = self.book.title,
            authors = self.book.authors,
            identifiers = [[identifier.key, identifier.value] for identifier in self.book.identifiers],
#            identifiers = self.book.identifiers,
            files = [fname.file_name for fname in self.book.files],
            tags = [tag.name for tag in self.book.tags],
            thumb = self.book.cover(),
            )
        print "Rendered in: %s seconds"%(time.time()-t1)
        print html
        self.about_web_view.page().mainFrame().setHtml(html)
        self.about_web_view.setUpdatesEnabled(True)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    models.initDB()
    if len(sys.argv) == 1:
        # use a default book
        ventana = AboutBook(models.Book.get_by().id)
    else:
        ventana = AboutBook(int(sys.argv[1]))
    ventana.show()
    sys.exit(app.exec_())
