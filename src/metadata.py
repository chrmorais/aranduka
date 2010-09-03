import collections
import gdata.books.service
import sys

BookMetadata = collections.namedtuple('BookMetadata', 'title thumbnail date subjects authors description')

SERVICES = {'google_books':'Google Books', 'service_x':'Service X'}

google_books = gdata.books.service.BookService()

def get_metadata(query, service='google_books'):
    '''Get book metadata from the web.'''
    if service == 'google_books':
        result = google_books.search(query)
        if result.entry:
            datos = result.entry[0].to_dict()
            return BookMetadata(title=datos['title'],
                                thumbnail=datos['thumbnail'],
                                date=datos['date'],
                                subjects=datos['subjects'],
                                authors=datos['authors'],
                                description=datos['description'])
        else:
            return None
    elif service == 'service_x':
        return None



