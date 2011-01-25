import os, sys, urllib2
import datetime
import gdata.books.service
from metadata import BookMetadata
from pluginmgr import Guesser

google_books = gdata.books.service.BookService()

class GoogleGuesser(Guesser):
    name = "Google Books"

    def can_guess(self, book):
        return True

    def _translateQuery (self, query):
        q = ''
        if query.title is not None:
            q += 'TITLE %s '%query.title
        if query.authors is not None:
            q += 'AUTHOR %s '%query.authors
        if query.identifiers is not None:
            q += 'ISBN %s '%query.identifiers
        return q

    def guess(self, query):
        result = google_books.search(self._translateQuery(query))
        if result.entry:
            data = [x.to_dict() for x in result.entry]
            return [BookMetadata(title=x.get('title','No Title').decode('utf-8'),
                                thumbnail=x.get('thumbnail',''),
                                date=x.get('date',datetime.date(1970,1,1)),
                                subjects=x.get('subjects',[]),
                                authors=x.get('authors',[]),
                                identifiers=x.get('identifiers',()),
                                description=x.get('description',''))
                    for x in data ]
        else:
            return None
