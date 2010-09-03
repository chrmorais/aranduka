import collections
import gdata.books.service

BookMetadata = collections.namedtuple('BookMetadata', 'title thumbnail date subjects authors description')

SERVICES = {'google_books':'Google Books', 'service_x':'Service X'}

google_books = gdata.books.service.BookService()

def get_metadata(query, service='google_books'):
    '''Get book metadata from the web.'''
    if service == 'google_books':
        result = google_books.search(query)
        if result.entry:
            data = result.entry[0].to_dict()
            return BookMetadata(title=data['title'],
                                thumbnail=data.get('thumbnail',''),
                                date=data['date'],
                                subjects=data.get('subjects',[]),
                                authors=data.get('authors',[]),
                                description=data.get('description',''))
        else:
            return None
    elif service == 'service_x':
        return None



