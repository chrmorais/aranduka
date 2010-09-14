import collections, datetime
import gdata.books.service

BookMetadata = collections.namedtuple('BookMetadata', 'title thumbnail date subjects authors description identifiers')

SERVICES = {'google_books':'Google Books', 'service_x':'Service X'}

google_books = gdata.books.service.BookService()

def get_metadata(query, service='google_books'):
    '''Get book metadata from the web.'''
    if service == 'google_books':
        result = google_books.search(query)
        if result.entry:
            data = [x.to_dict() for x in result.entry]
            return [BookMetadata(title=x['title'],
                                thumbnail=x.get('thumbnail',''),
                                date=x.get('date',datetime.date(1970,1,1)),
                                subjects=x.get('subjects',[]),
                                authors=x.get('authors',[]),
                                identifiers=x.get('identifiers',()),
                                description=x.get('description',''))
                    for x in data ]
        else:
            return None
    elif service == 'service_x':
        return None



